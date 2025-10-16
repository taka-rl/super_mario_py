from __future__ import annotations
import time
import pygame
from typing import Callable, Optional

from game.app import GameApp
from game.core.state import Status
from tools.measurements.metrics import PerfMonitor, PerfCSVLogger


class MeasureGameApp(GameApp):
    """
    A perf-instrumented GameApp. It defers heavy transitions to itself and logs timings.
    Lives in tools/, so game/ never imports tools/.
    """
    def __init__(self, win: pygame.Surface, clock: pygame.time.Clock,
                 monitor: PerfMonitor, logger: PerfCSVLogger, *,
                 cache_stats_fn: Optional[Callable[[], tuple[int, int]]] = None,):
        self._monitor = monitor
        self._logger = logger
        self._cache_stats_fn = cache_stats_fn
        self._phase = "play"
        
        t0 = time.perf_counter()
        super().__init__(win, clock)
        self._init_ms = (time.perf_counter() - t0) * 1000.0

    def _extra(self, **extra):
        if callable(self._cache_stats_fn):
            count, bytes_ = self._cache_stats_fn()
            extra.setdefault("cache_count", count)
            extra.setdefault("cache_mb", (bytes_ / (1024 * 1024)) if bytes_ else 0.0)
        return extra

    def log_init(self) -> None:
        """Log the end of the init phase."""
        self._logger.event("init_done", self._monitor, phase="init_startup", 
                           extra=self._extra(init_ms=self._init_ms))    
   
    def start(self): self.t0 = time.perf_counter()
    
    def measure_regular_step(self, fps: int) -> None:
        """
        Measure and log regular periodic performance data.
        This method should be called once per frame in the main game loop.
            
        It updates the performance monitor with the time delta since the last call,
        draws the performance overlay on the game window, and logs performance data
        to the CSV logger if enough time has passed.
        
        Args:
            fps (int): The target frames per second for the game loop.
        """
        # --- Measure regular periodic perf row (every 1s) ---
        dt = self._clock.tick(fps) / 1000.0
        self._monitor.tick(dt)
        self._monitor.draw_overlay(self._win)
        self._logger.maybe_write(self._monitor, phase=self.phase,
                           cache_stats=self._cache_stats_fn if callable(self._cache_stats_fn) else None)
        
    def step(self):
        """
        Execute one step of the game loop, with perf logging.

        This includes updating game state, managing goal animations,
        and drawing the current frame. It also handles transitions for game over,
        restarting the game, and removing dead entities.
        If the game is cleared, it stops the game loop.

        Returns:
            None
        """
        # Updates
        self._update()

        # Goal animation
        if self._mario.status == Status.GOAL:
            if not self._goal_manager.isactive:
                self._goal_manager.isactive = True
           
            self._goal_manager.update()

        # Temporary end when Game is clear
        if self._mario.status == Status.CLEAR:
            self.running = False
            return
         
        # Game begins again!
        if self._mario.status == Status.INIT:
            # --- Measure the gameover phase ---
            self.phase = "gameover"
            t1 = time.perf_counter()
            self._group, self._group_bg, self._mario, self._map, self._goal_manager = self._init()
            gameover_ms = (time.perf_counter() - t1) * 1000.0

            extra = {"gameover_ms": gameover_ms}
            if callable(self._cache_stats_fn):
                cc, cb = self._cache_stats_fn()
                extra["cache_count"] = cc
                extra["cache_mb"] = (cb / (1024*1024)) if cb else None
            self._logger.event("gameover_done", self._monitor, phase=self.phase, extra=extra)

            self.phase = "play"
            
            return 
        
        # Mario is dead and the life stocks is not 0
        elif self._mario.status == Status.DEAD:
            # --- Measure the reset phase ---
            self.phase = "reset"
            t1 = time.perf_counter()
            self._group, self._group_bg = self._mario.init_dead()
            reset_ms = (time.perf_counter() - t1) * 1000.0

            extra = {"reset_ms": reset_ms}
            if callable(self._cache_stats_fn):
                cc, cb = self._cache_stats_fn()
                extra["cache_count"] = cc
                extra["cache_mb"] = (cb / (1024*1024)) if cb else None
            self._logger.event("reset_done", self._monitor, phase=self.phase, extra=extra)

            self.phase = "play"
        
            return
        
        # The life stocks is 0
        elif self._mario.status == Status.GAMEOVER:
            self._group.empty()
            self._group_bg.empty()
        
        # Remove DEAD status
        for entity in self._group.sprites():
            if entity.status == Status.DEAD:
                self._group.remove(entity)
        
        for entity_bg in self._group_bg.sprites():
            if entity_bg.status == Status.DEAD:
                self._group_bg.remove(entity_bg)

        # Goal animation
        if self._mario.status == Status.GOAL:
            if not self._goal_manager.isactive:
                self._goal_manager.isactive = True

            self._goal_manager.update()

        # Temporary end when Game is clear
        if self._mario.status == Status.CLEAR:
            self.running = False
            return
        
        # Draw
        self._draw()
    
    @property
    def phase(self) -> str:
        return self._phase
    
    @phase.setter
    def phase(self, value: str) -> None:
        self._phase = value
