from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from entities.entity import Entity
from core.state import Status

if TYPE_CHECKING:
    from entities.mario import Mario
    from levels.map import Map


class Star(Entity):
    def __init__(self, x: int, y: int, dir: int, mario: Mario, map: Map):
        self.__imgs: list = [pygame.image.load('./img/star.jpg')]
        self.image = self.__imgs[0]
        
        self._rawrect = pygame.Rect(x, y, 20, 20)
        super().__init__(x, y, dir, mario, map)
    
    def update(self):
        # Not update if Mario is dead or growing or shrinking or Game is paused
        if self._mario.status in [Status.DEADING, Status.GROWING, Status.SHRINKING, Status.PAUSE]:
            return
        
        if self._status == Status.NORMAL:
            x, y = self._rawrect.x // 20, self._rawrect.y // 20
            
            if self._map.ispushedblock((y, x)):
                self._status = Status.TREADING
                self._rawrect.y -= 5
            self.image.set_alpha(0)
        elif self._status == Status.TREADING:
            self._walkidx += 1
            if self._walkidx == 4:
                self.image.set_alpha(255)
            if self._walkidx <= 15:
                self._rawrect.y -= 1
            if self._walkidx == 18:
                self._vy = -10
                self._status = Status.FLYING
        elif self._status == Status.FLYING:
            self._rawrect.x += self._dir
            
             # X axle collision check
            if self._map.chk_collision(self._rawrect):
                self._rawrect.x = (self._rawrect.x // 20 + (1 if self._dir < 0 else 0)) * 20
                self._dir *= -1

            # Y axle move
            self._vy += 1
            self._rawrect.y += self._vy
                
            # Y axle collision check
            if self._map.chk_collision(self._rawrect):
                self._rawrect.y = (self._rawrect.y // 20 + (1 if self._vy < 0 else 0)) * 20
                                
                if self._vy > 0:
                    self._vy = -10
                else:
                    # jump
                    self._vy = 0
        
            # Collision check with Mario
            if self._rawrect.colliderect(self._mario.rawrect):
                # Disappear star
                self._status = Status.DEAD
                
                # Prepare for a star mario
                self._mario.hasstar = True
                self._mario.isinvisible = True
                self._mario.invisiblecounter = 240  # 8 seconds
        
        self.rect = pygame.Rect(self._map.get_drawxentity(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)
