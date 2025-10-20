from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from game.core.state import Status
from game.core.settings import TILE_SIZE
from game.levels.goal_manager import GoalManager
from game.entities.entity import Entity
from game.core import assets

if TYPE_CHECKING:
    from game.entities.mario import Mario
    from game.levels.map import Map


class CastleFlag(Entity):
    POS_Y: int = 140  # Castle Flag position on Y axle

    IMAGE_FILES: tuple[str, ...] = ('./img/castle_flag.jpg',)
    _IMAGES: tuple[pygame.Surface, ...] | None = None

    @classmethod
    def images(cls) -> tuple[pygame.Surface, ...]:
        """
        Load the images specified in IMAGE_FILES and store them in memory.
        """
        if cls._IMAGES is None:
            cls._IMAGES = assets.get_images(cls.IMAGE_FILES)
        return cls._IMAGES
        
    def __init__(self, x: int, y: int, dir: int, mario: Mario, map: Map, goal_manager: GoalManager):
        self._imgs: tuple = self.images()
        self.image = self._imgs[0].copy()
        
        self._rawrect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                
        self.__goal_manager = goal_manager
        self.__goal_manager.castle_flag = self
        
        super().__init__(x, y, dir, mario, map)
    
    def update(self):
        # Mario reaches the goal, then change its status to GOAL
        if self._mario.status == Status.GOAL:
            self._status = Status.GOAL
        else:
            # Image is invisible except goal
            self.image.set_alpha(0)   
        self.rect = pygame.Rect(self._map.get_drawxentity(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)
    
    def rise(self):
        # Not execute when its status is not GOAL
        if self._status != Status.GOAL:
            return
        
        if self._rawrect.y <= self.POS_Y:
            # Hold position, stay visible
            self._rawrect.y = self.POS_Y
            self.image.set_alpha(255)
        else:
            self._rawrect.y -= 2
            