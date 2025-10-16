import pygame

from game.core.state import Status
from game.systems.sound import Sound
from game.systems.hud import HeadUpDisplay
from game.entities.mario import Mario
from game.levels.map import Map
from game.levels.goal_manager import GoalManager


class GameApp:
    """
    Main application class for the game. Handles game loop, events, updates, and rendering.
    
    Attributes:
        win (pygame.Surface): The main display surface.
        clock (pygame.time.Clock): Clock object to manage frame rate.
        group (pygame.sprite.Group): Group of foreground sprites.
        group_bg (pygame.sprite.Group): Group of background sprites.
        mario (Mario): The main player character.
        map (Map): The game map.
        goal_manager (GoalManager): Manages goal-related animations and logic.
        running (bool): Flag to control the main game loop.
    Methods:
        __init__(self, win: pygame.Surface, clock: pygame.time.Clock): Initializes the game application.
        _draw(self) -> None: Draws all game elements on the display surface.
        _update(self) -> None: Updates all game elements.
        _event_handle(self, events: list[pygame.event.Event]) -> None: Handles all events.
        tick(self, fps: int=30) -> None: Controls the frame rate of the game.
        step(self) -> None: Executes one step of the game loop.
    
    """

    def __init__(self, win: pygame.Surface, clock: pygame.time.Clock):
        self._win = win
        self._clock = clock
        self.running = True
        self._group, self._group_bg, self._mario, self._map, self._goal_manager = self._init()

    @property
    def win(self) -> pygame.Surface:
        return self._win
    
    @property
    def mario(self) -> Mario:
        return self._mario
    
    def _init(self):
        """Initialize all game elements"""
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

    def _draw(self) -> None:
        """Draw all game elements"""
        self._map.fill(self._win)
        self._group_bg.draw(self._win)
        self._map.draw(self._win, self._mario.rawrect)
        self._group.draw(self._win)
        self._mario.draw(self._win)

    def _update(self) -> None:
        """Update all game elements"""
        self._group_bg.update()
        self._group.update()
        self._mario.update()
    
    def event_handle(self, events: list[pygame.event.Event]) -> None:
        """
        Handle all events.
        
        Args:
            events (list[pygame.event.Event]): List of pygame events
        
        Returns:
            None
        """
        for e in events:
            if e.type == pygame.QUIT:
                self.running = False

            elif e.type == pygame.KEYDOWN:
                # Release a fire ball
                if e.key == pygame.K_LSHIFT and self._mario.isfire:
                    self._mario.fire()

                # Game is paused when "p" is pushed
                elif e.key == pygame.K_p and self._mario.status == Status.NORMAL:
                    self._mario.status = Status.PAUSE
                elif e.key == pygame.K_p and self._mario.status == Status.PAUSE:
                    self._mario.status = Status.NORMAL
    
    def tick(self, fps: int=30) -> None:
        """
        Control the frame rate of the game.
        
        Args:
            fps (int): Target frames per second. Default is 30.
        
        Returns:
            None
        """
        self._clock.tick(fps)

    def step(self) -> None:
        """
        Execute one step of the game loop.
        
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
            self._group, self._group_bg, self._mario, self._map, self._goal_manager = self._init()
            return 
        
        # Mario is dead and the life stocks is not 0
        elif self._mario.status == Status.DEAD:
            self._group, self._group_bg = self._mario.init_dead()
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
    
        # Draw
        self._draw()
