import argparse
import pygame
import os

from game.core.settings import W, H
from game.core import assets


def main() -> None:
    """Main game loop."""
    from game.app import GameApp

    # Initialize pygame
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=1)
    pygame.init()
    win, clock = pygame.display.set_mode((W, H)), pygame.time.Clock()

    # Create GameApp instance
    game_app = GameApp(win, clock)

    # Event loop
    while game_app.running:
        # Handle events
        events = pygame.event.get()

        # Pass events to game app
        game_app.event_handle(events)

        # Step the game state
        game_app.step()

        # Update the display
        pygame.display.flip()

        # Frame rate
        game_app.tick(30)
    
    # End pygame
    pygame.quit()


def measure_main(args=None) -> None:
    """
    Measure the main game loop of CPU and memory usages.
    
    args: 
        argparse.Namespace or None
        If None, parse from sys.argv.
        If args.perf_csv is set, log performance data into the specified CSV file
        If args.replay is set, replay input events from the specified file.
    """
    from tools.measurements.measure_app import MeasureGameApp
    from tools.measurements.metrics import PerfMonitor, PerfCSVLogger


    args = _parse_args() if args is None else args
    args.perf = True

    # Initialize pygame
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=1)
    pygame.init()
    win = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Super Mario (Perf Mode)")
    
    # Create clock rate
    clock = pygame.time.Clock()

    # Optional cache stat providers from core.assets
    cache_stats_fn = getattr(assets, "cache_stats", None)     # -> (count:int, bytes:int)
    monitor = PerfMonitor(sample_hz=2.0)                       # CPU/RSS every ~0.5s, FPS (EMA)
    logger = PerfCSVLogger(args.perf_csv, sample_sec=1.0)     # CSV row per second
    
    # --- Measure the initialization phase ---
    measure_app = MeasureGameApp(win, clock, monitor, logger, cache_stats_fn=cache_stats_fn)
    measure_app.log_init()
        
    # Event loop
    while measure_app.running:
                    
        # Handle events
        events = pygame.event.get()
        measure_app.event_handle(events)

        # Step the game state
        measure_app.step()

        # --- Measure regular periodic perf row (every 1s) ---
        measure_app.measure_regular_step(args.fps)
        
        # Update the display
        pygame.display.flip()
        
    # End pygame
    pygame.quit()
    logger.close()


def _parse_args(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--perf", action="store_true",
                   help="Enable perf HUD + CSV logging.")
    p.add_argument("--perf-csv", default="perf_log.csv",
                   help="CSV output path (perf mode only).")
    p.add_argument("--fps", type=int, default=30,
                   help="Target FPS cap.")
    return p.parse_args(argv)


if __name__ == '__main__':
    args = _parse_args()
    perf_flag = args.perf or os.getenv("PERF", "0") == "1"
    (measure_main if perf_flag else main)(args)
