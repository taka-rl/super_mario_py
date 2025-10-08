import argparse
import pygame
import os

from game.core.state import Status
from game.core.settings import W, H
from game.core import assets 
from game.systems.sound import Sound
from game.systems.hud import HeadUpDisplay
from game.entities.mario import Mario
from game.levels.map import Map
from game.levels.goal_manager import GoalManager


def init():
    # Define Sprite group
    group = pygame.sprite.RenderUpdates()
    group_bg = pygame.sprite.RenderUpdates()
    
    # Map class
    map = Map(group, group_bg, Sound(), HeadUpDisplay(), "World1-1")
    
    # Mario class
    mario = Mario(map, group)
    
    # TODO: Ask a player which World the player wants to play
    goal_manager = GoalManager("World1-1", mario, map)
    
    return group, group_bg, mario, map, goal_manager


def main():
    """main function"""
    
    # TODO: Add a start menu where a player choose a stage
        
    # Initialize pygame
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=1)
    pygame.init()
    
    # Build a display
    win = pygame.display.set_mode((W, H))
    
    # Create clock rate
    clock = pygame.time.Clock()
    
    # Initialize sprite
    group, group_bg, mario, map, goal_manager = init()
    
    # Event loop
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.KEYDOWN:
                # Release a fire ball
                if e.key == pygame.K_LSHIFT and mario.isfire:
                    mario.fire()

                # Game is paused when "p" is pushed
                elif e.key == pygame.K_p and mario.status == Status.NORMAL:
                    mario.status = Status.PAUSE
                elif e.key == pygame.K_p and mario.status == Status.PAUSE:
                    mario.status = Status.NORMAL
        
        # Update the group_bg
        group_bg.update()
        
        # Update the group
        group.update()
        
        # Update Mario
        mario.update()
        
        # Goal animation
        if mario.status == Status.GOAL:
            if not goal_manager.isactive:
                goal_manager.isactive = True
           
            goal_manager.update()

        # Temporary end when Game is clear
        if mario.status == Status.CLEAR:
            running = False
            continue
         
        # Game begins again!
        if mario.status == Status.INIT:
            group, group_bg, mario, map, goal_manager = init()
            continue 
        
        # Mario is dead and the life stocks is not 0
        elif mario.status == Status.DEAD:
            group, group_bg = mario.init_dead()
            continue
        
        # The life stocks is 0
        elif mario.status == Status.GAMEOVER:
            group.empty()
            group_bg.empty()
        
        # Remove DEAD status
        for entity in group.sprites():
            if entity.status == Status.DEAD:
                group.remove(entity)
        
        for entity_bg in group_bg.sprites():
            if entity_bg.status == Status.DEAD:
                group_bg.remove(entity_bg)
    
        # Fill in the background     
        map.fill(win)

        # Draw the group_bg
        group_bg.draw(win)
             
        # Draw map
        map.draw(win, mario.rawrect)
        
        # Draw the group
        group.draw(win)
        
        # Draw Mario
        mario.draw(win)

        # Update the display
        pygame.display.flip()

        # Frame rate
        clock.tick(30)
    
    # End pygame
    pygame.quit()


def measure_main(args=None) -> None:
    """
    Measure the main game loop of CPU and memory usages.
    
    args: 
    """

    if args is None:
        args = _parse_args()
        args.perf = True  # force perf mode for mario-perf

    from tools.metrics import PerfMonitor, PerfCSVLogger

    # Initialize pygame
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=1)
    pygame.init()
    
    # Build a display
    win = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Super Mario (Perf Mode)")

    # Create clock rate
    clock = pygame.time.Clock()

    # Optional cache stat providers from core.assets
    cache_stats_fn = getattr(assets, "cache_stats", None)     # -> (count:int, bytes:int)
    cache_str_fn   = getattr(assets, "cache_stats_str", None) # -> "cache: 12 | 4.3MB"

    monitor = PerfMonitor(sample_hz=2.0)                       # CPU/RSS every ~0.5s, FPS (EMA)
    logger = PerfCSVLogger(args.perf_csv, sample_sec=1.0)     # CSV row per second
    
    # Initialize sprite
    group, group_bg, mario, map, goal_manager = init()
    
    # Event loop
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.KEYDOWN:
                # Release a fire ball
                if e.key == pygame.K_LSHIFT and mario.isfire:
                    mario.fire()

                # Game is paused when "p" is pushed
                elif e.key == pygame.K_p and mario.status == Status.NORMAL:
                    mario.status = Status.PAUSE
                elif e.key == pygame.K_p and mario.status == Status.PAUSE:
                    mario.status = Status.NORMAL

        # Frame timing at the START
        dt = clock.tick(args.fps) / 1000.0

        # Updates
        group_bg.update()
        group.update()
        mario.update()
        
        # Goal animation
        if mario.status == Status.GOAL:
            if not goal_manager.isactive:
                goal_manager.isactive = True
           
            goal_manager.update()

        # Temporary end when Game is clear
        if mario.status == Status.CLEAR:
            running = False
            continue
         
        # Game begins again!
        if mario.status == Status.INIT:
            group, group_bg, mario, map, goal_manager = init()
            continue 
        
        # Mario is dead and the life stocks is not 0
        elif mario.status == Status.DEAD:
            group, group_bg = mario.init_dead()
            continue
        
        # The life stocks is 0
        elif mario.status == Status.GAMEOVER:
            group.empty()
            group_bg.empty()
        
        # Remove DEAD status
        for entity in group.sprites():
            if entity.status == Status.DEAD:
                group.remove(entity)
        
        for entity_bg in group_bg.sprites():
            if entity_bg.status == Status.DEAD:
                group_bg.remove(entity_bg)
    
        # Draw scene
        map.fill(win)
        group_bg.draw(win)
        map.draw(win, mario.rawrect)
        group.draw(win)
        mario.draw(win)

        # Perf instrumentation
        monitor.tick(dt)
        extra = cache_str_fn() if callable(cache_str_fn) else ""
        monitor.draw_overlay(win, extra=extra)
        logger.maybe_write(
            monitor,
            cache_stats=cache_stats_fn if callable(cache_stats_fn) else None,
        )
        
        # Update the display
        pygame.display.flip()

    # End pygame
    pygame.quit()


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
