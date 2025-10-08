from __future__ import annotations
import csv
import time
from typing import Callable, Optional, Tuple

# psutil is optional; if missing, we degrade gracefully
try:
    import psutil
except Exception:
    psutil = None  # type: ignore


class PerfMonitor:
    """Lightweight frame monitor: fps (EMA), cpu%, rss MB, optional on-screen overlay."""
    def __init__(self, sample_hz: float = 2.0, ema_alpha: float = 0.2) -> None:
        self.ema_alpha = float(ema_alpha)
        self.fps: float = 0.0
        self.cpu_pct: float = 0.0
        self.rss_mb: float = 0.0
        self._last_cpu_sample = 0.0
        self._cpu_interval = 1.0 / max(0.1, sample_hz)

        self._t_last = time.perf_counter()

        self._proc = psutil.Process() if psutil else None
        if self._proc:
            # Prime psutil’s sampling
            try:
                self._proc.cpu_percent(None)
            except Exception:
                pass

        # pygame things are only touched lazily inside draw_overlay()
        self._font = None  # created lazily

    def tick(self, dt: Optional[float] = None) -> None:
        """Call once per frame. Pass dt if you have it; else it computes from perf_counter."""
        now = time.perf_counter()
        if dt is None:
            dt = now - self._t_last
        self._t_last = now

        if dt > 0:
            inst_fps = 1.0 / dt
            self.fps = (self.ema_alpha * inst_fps) + ((1 - self.ema_alpha) * self.fps)

        # sample cpu/rss sparsely
        if self._proc and (now - self._last_cpu_sample) >= self._cpu_interval:
            try:
                self.cpu_pct = float(self._proc.cpu_percent(0.0))
                rss = self._proc.memory_info().rss
                self.rss_mb = rss / (1024 * 1024)
            except Exception:
                pass
            self._last_cpu_sample = now

    def draw_overlay(self, screen, *, extra: str = "") -> None:
        """Optional: draw a small text overlay. Safe if pygame is available."""
        try:
            import pygame
        except Exception:
            return  # pygame not available in headless

        if not pygame.get_init():
            return

        if self._font is None:
            try:
                self._font = pygame.font.SysFont("consolas", 16)
            except Exception:
                return

        text = f"FPS {self.fps:3.1f}, CPU {self.cpu_pct:2.0f}%, RSS {self.rss_mb:3.1f} MB"
        if extra:
            text += f" | {extra}"
        try:
            surf = self._font.render(text, True, (255, 255, 255))
            screen.blit(surf, (5, 40))
        except Exception:
            pass


class NullMonitor:
    """No-op replacement with the same interface."""
    def __init__(self, *_, **__): 
        self.fps = 0.0
        self.cpu_pct = 0.0
        self.rss_mb = 0.0
    def tick(self, dt: Optional[float] = None) -> None: 
        pass
    def draw_overlay(self, screen, *, extra: str = "") -> None: 
        pass


class PerfCSVLogger:
    """Write FPS, CPU%, RSS, and cache stats to CSV every N seconds."""
    def __init__(self, path: str = "perf_log.csv", sample_sec: float = 1.0) -> None:
        self.sample_sec = float(sample_sec)
        self._f = open(path, "w", newline="")
        self._w = csv.writer(self._f)
        self._w.writerow(["t_sec","fps","cpu_pct","rss_mb","cache_count","cache_mb"])
        self._t0 = time.perf_counter()
        self._next = self._t0

    def maybe_write(
        self,
        monitor: PerfMonitor | NullMonitor,
        *,
        cache_stats: Optional[Callable[[], Tuple[int, int]]] = None,
    ) -> None:
        now = time.perf_counter()
        if now < self._next:
            return

        count, bytes_ = (0, 0)
        if cache_stats:
            try:
                count, bytes_ = cache_stats()
            except Exception:
                pass

        row = [
            now - self._t0,
            getattr(monitor, "fps", 0.0),
            getattr(monitor, "cpu_pct", 0.0),
            getattr(monitor, "rss_mb", 0.0),
            count,
            bytes_ / (1024 * 1024),
        ]
        self._w.writerow(row)
        self._f.flush()
        self._next = now + self.sample_sec

    def close(self) -> None:
        try:
            self._f.close()
        except Exception:
            pass


class NullCSVLogger:
    def __init__(self, *_, **__): pass
    def maybe_write(self, *_, **__): pass
    def close(self) -> None: pass
