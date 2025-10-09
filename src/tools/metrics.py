# src/tools/metrics.py
from __future__ import annotations

import csv
import os
import time
from typing import Callable, Optional

import pygame
import psutil


class PerfMonitor:
    """
    Sampling-based performance monitor.
      - fps: EMA FPS (smoothed)
      - cpu: process CPU percent (psutil)
      - rss_mb: process resident memory (MB)
    """

    def __init__(self, sample_hz: float = 2.0, fps_halflife_s: float = 0.5) -> None:
        self._proc = psutil.Process(os.getpid())
        # prime psutil cpu_percent for the first delta-based reading
        try:
            self._proc.cpu_percent(None)
        except Exception:
            pass

        self.sample_period = max(1.0 / sample_hz, 0.05)
        self._next_psutil_t = 0.0

        self.fps: float = 0.0
        self.cpu: float = 0.0
        self.rss_mb: float = 0.0

        self._fps_halflife = max(fps_halflife_s, 1e-3)
        self._font: Optional[pygame.font.Font] = None

    def _fps_alpha(self, dt: float) -> float:
        # EMA alpha from half-life so smoothing is stable across frame rates
        # alpha = 1 - 2^(-dt / halflife)
        return 1.0 - pow(2.0, -dt / self._fps_halflife)

    def tick(self, dt: float) -> None:
        """Call once per frame with seconds since last frame."""
        # FPS smoothing
        if dt > 0:
            inst = 1.0 / dt
            if self.fps <= 0:
                self.fps = inst
            else:
                a = self._fps_alpha(dt)
                self.fps += a * (inst - self.fps)

        # psutil sampling at lower rate
        now = time.time()
        if now >= self._next_psutil_t:
            self._next_psutil_t = now + self.sample_period
            try:
                self.cpu = float(self._proc.cpu_percent(None))
                self.rss_mb = float(self._proc.memory_info().rss) / 1_000_000.0
            except Exception:
                # keep previous values if psutil fails
                pass

    def draw_overlay(self, surface: pygame.Surface, *, extra: str = "") -> None:
        """Draw FPS, CPU and RSS on-screen HUD."""
        if self._font is None:
            try:
                pygame.font.init()
                self._font = pygame.font.SysFont("consolas", 16)
            except Exception:
                return

        txt = f"FPS {self.fps:3.1f} | CPU {self.cpu:3.1f}% | RSS {self.rss_mb:3.1f} MB"
        if extra:
            txt += " | " + extra

        img = self._font.render(txt, True, (240, 240, 240))
        pad = 6
        bg = pygame.Surface((img.get_width() + pad * 2, img.get_height() + pad * 2), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 140))
        surface.blit(bg, (8, 8))
        surface.blit(img, (8 + pad, 8 + pad))


class NullMonitor:
    """No-op replacement if you ever want to disable monitoring."""
    def __init__(self, *_, **__): pass
    def tick(self, *_): pass
    def draw_overlay(self, *_ , **__): pass
    fps = 0.0
    cpu = 0.0
    rss_mb = 0.0


class PerfCSVLogger:
    """
    Periodically writes perf rows (and one-off events) to CSV.

    Columns:
      ts, t_rel_s, event, phase, fps, cpu, rss_mb, cache_count, cache_mb,
      init_ms, reset_ms, gameover_ms
    """

    def __init__(
        self,
        path: str,
        sample_sec: float = 1.0,
        *,
        append: bool = False,
        extra_fieldnames: list[str] | None = None,
    ) -> None:
        self._path = path
        self._sample_sec = max(sample_sec, 0.1)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

        # Start time for relative timestamps
        self._t0 = time.perf_counter()

        base = [
            "ts", "t_rel_s",
            "event", "phase",
            "fps", "cpu", "rss_mb",
            "cache_count", "cache_mb",
            "init_ms", "reset_ms", "gameover_ms",
        ]
        if extra_fieldnames:
            for f in extra_fieldnames:
                if f not in base:
                    base.append(f)
        self._fieldnames = base

        mode = "a" if append and os.path.exists(path) else "w"
        self._fh = open(path, mode, newline="")
        self._writer = csv.DictWriter(self._fh, fieldnames=self._fieldnames, extrasaction="ignore")
        if mode == "w":
            self._writer.writeheader()

        self._next_write_t = 0.0

    def _row_from_monitor(self, monitor: PerfMonitor) -> dict:
        return {
            "ts": time.time(),
            "t_rel_s": time.perf_counter() - self._t0,
            "fps": float(getattr(monitor, "fps", 0.0)),
            "cpu": float(getattr(monitor, "cpu", 0.0)),
            "rss_mb": float(getattr(monitor, "rss_mb", 0.0)),
            "cache_count": 0,
            "cache_mb": 0.0,
            "init_ms": None,
            "reset_ms": None,
            "gameover_ms": None,
        }

    def _apply_cache(self, row: dict, cache_stats: Optional[Callable[[], tuple[int, int]]]) -> None:
        if callable(cache_stats):
            try:
                cnt, bytes_ = cache_stats()
                row["cache_count"] = int(cnt)
                row["cache_mb"] = float(bytes_) / 1_000_000.0
            except Exception:
                pass

    def maybe_write(
        self,
        monitor: PerfMonitor,
        *,
        phase: str = "play",
        cache_stats: Optional[Callable[[], tuple[int, int]]] = None,
        extra: dict | None = None,
    ) -> None:
        """Write a periodic tick row (at most every sample_sec)."""
        now = time.time()
        if now < self._next_write_t:
            return
        self._next_write_t = now + self._sample_sec

        row = self._row_from_monitor(monitor)
        row["event"] = ""
        row["phase"] = phase
        self._apply_cache(row, cache_stats)
        if extra:
            row.update(extra)

        self._writer.writerow(row)
        self._fh.flush()

    def event(
        self,
        name: str,
        monitor: PerfMonitor,
        *,
        phase: str = "",
        cache_stats: Optional[Callable[[], tuple[int, int]]] = None,
        extra: dict | None = None,
    ) -> None:
        """Write a one-off row (e.g., init_done, reset_done, gameover_done)."""
        row = self._row_from_monitor(monitor)
        row["event"] = name
        row["phase"] = phase
        self._apply_cache(row, cache_stats)
        if extra:
            row.update(extra)

        self._writer.writerow(row)
        self._fh.flush()

    def close(self) -> None:
        try:
            self._fh.close()
        except Exception:
            pass


class NullCSVLogger:
    """No-op CSV logger."""
    def __init__(self, *_, **__): pass
    def maybe_write(self, *_, **__): pass
    def event(self, *_, **__): pass
    def close(self): pass

