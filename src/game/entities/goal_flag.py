from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from game.core.state import Status
from game.core.settings import GOAL_FALL_SPEED, GOAL_BOTTOM_Y, SCORE_ARRAY, TILE_SIZE
from game.systems.number import Number
from game.entities.entity import Entity
from game.core import assets

if TYPE_CHECKING:
    from game.entities.mario import Mario
    from game.levels.map import Map
    

class GoalFlag(Entity):
    HEIGHT_RANGE: int = 200  # Cover the goal pole from the top to bottom
    
    IMAGE_FILES: tuple[str, ...] = ('./img/goal_flag.jpg',)
    _IMAGES: tuple[pygame.Surface, ...] | None = None

    @classmethod
    def images(cls) -> tuple[pygame.Surface, ...]:
        """
        Load the images specified in IMAGE_FILES and store them in memory.
        """
        if cls._IMAGES is None:
            cls._IMAGES = assets.get_images(cls.IMAGE_FILES)
        return cls._IMAGES
    
    def __init__(self, x: int, y: int, dir: int, mario: Mario, map: Map):
        self.__imgs: tuple = self.images()
        self.image = self.__imgs[0]
        
        super().__init__(x, y, dir, mario, map)
    
    def update(self):
        if self._status == Status.GOAL:
            self._rawrect.y += GOAL_FALL_SPEED
            if self._rawrect.y > GOAL_BOTTOM_Y:
                self._rawrect.y = GOAL_BOTTOM_Y
            
        else:
            # Collision check with Mario
            if pygame.Rect(self._rawrect.x + TILE_SIZE, self._rawrect.y, self._rawrect.width, self.HEIGHT_RANGE).colliderect(self._mario.rawrect):
                self._status = Status.GOAL
                self._mario.status = Status.GOAL
                
                # Adjust Mario position to the goal pole    
                self._mario.rawrect.x = self._rawrect.x
                
                # Set score based on the goal position 
                if self._mario.rawrect.y <= 80:
                    score_idx = 8  # 5000
                elif self._mario.rawrect.y <= 110:
                    score_idx = 6  # 2000
                elif self._mario.rawrect.y <= 140:
                    score_idx = 5  # 1000
                elif self._mario.rawrect.y <= 170:
                    score_idx = 3  # 500
                elif self._mario.rawrect.y <= 200:
                    score_idx = 1  # 200
                else:
                    score_idx = 0  # 100
                
                # Score shows up next to the bottom of the goal pole
                score_number = Number(self._mario.rawrect.x + TILE_SIZE, GOAL_BOTTOM_Y, SCORE_ARRAY[score_idx], self._map)
                score_number.status = Status.GOAL
                self._map.group.add(score_number)
                self._map.add_score(SCORE_ARRAY[score_idx])
                
                # Set timer to goal time
                self._map.goal_time = int(self._map.timer)
                   
        self.rect.topleft = (self._map.get_drawxentity(self._rawrect), self._rawrect.y)
