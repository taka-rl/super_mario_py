from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from entities.entity import Entity
from core.state import Status, GoalStatus

if TYPE_CHECKING:
    from levels.map import Map
    from levels.goal_manager import GoalManager
    from entities.mario import Mario


class Fireworks(Entity):    
    def __init__(self, x: int, y: int, dir: int, mario: Mario, map: Map, goal_manager: GoalManager):
        self._imgs: list = [pygame.image.load('./img/explode.jpg')]
        self.image = self._imgs[0]
        
        self._rawrect = pygame.Rect(x, y, 10, 10)
        
        self.__goal_manager: GoalManager = goal_manager
        self.__goal_manager.fireworks = self
        self.__counter: int = 0
        
        super().__init__(x, y, dir, mario, map)

    def update(self):
        # Mario reaches the goal, then change its status to GOAL
        if self._mario.status == Status.GOAL:
            self._status = Status.GOAL

        else:
            # Image is invisible except goal
            self.image.set_alpha(0)

        if self.__goal_manager.phase == GoalStatus.FIREWORKS:
            self.image.set_alpha(255)
            # Delete fireworks
            if self.__counter == 30:
                self._status = Status.DEAD
                self.__counter = 0
            self.__counter += 1
            
        self.rect = pygame.Rect(self._map.get_drawxentity(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)
