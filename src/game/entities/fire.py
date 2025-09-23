from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from entities.entity import Entity
from core.state import Status
from core.settings import W, H, SMALL_TILE_SIZE

if TYPE_CHECKING:
    from entities.mario import Mario
    from levels.map import Map


class Fire(Entity):
    def __init__(self, x: int, y: int, dir: int, mario: Mario, map: Map):
        self._imgs: list = [
            pygame.image.load('./img/fireball.jpg'),
            pygame.image.load('./img/explode.jpg'),
        ]
        self.image = self._imgs[0]
        
        self._rawrect = pygame.Rect(x, y, SMALL_TILE_SIZE, SMALL_TILE_SIZE)
        super().__init__(x, y, dir, mario, map)
    
    def update(self):
        # Not update if Mario is dead or growing or shrinking or Game is paused
        if self._mario.status in [Status.DEADING, Status.GROWING, Status.SHRINKING, Status.PAUSE]:
            return
        
        if self._status == Status.NORMAL:
            # X axle move
            self._rawrect.x += self._dir
                    
            # X axle collision check
            if self._map.chk_collision(self._rawrect):
                self._status = Status.DEAD
                if self in self._mario.arrlies:
                    self._mario.arrlies.remove(self)
                return
            
            # Disappear fire balls when hitting walls/pipes
            if self._rawrect.x < self._map.nowx or self._rawrect.x > self._map.nowx + W:
                self._status = Status.DEAD
                if self in self._mario.arrlies:
                    self._mario.arrlies.remove(self)
                return
            
            # Disappear fire balls for fall handing
            if self._rawrect.y > H:
                self._status = Status.DEAD
                if self in self._mario.arrlies:
                    self._mario.arrlies.remove(self)
                return

            # Y axle move
            self._vy += 1
            self._rawrect.y += self._vy
            
            # Y axle collision check
            if self._map.chk_collision(self._rawrect):
                self._rawrect.y = (self._rawrect.y // 20 + (1 if self._vy < 0 else 0)) * 20
                                    
                if self._vy > 0:
                    self._vy = -5
                else:
                    # jump
                    self._vy = 0
            
            # Add fire ball image animation here
            self.image = pygame.transform.rotate(self._imgs[0], (self._walkidx % 4) * 90)
            self._walkidx += 1
        elif self._status == Status.DEADING:
            # Change to explosion image
            if self._collapsecount < 4:
                self.image = self._imgs[1]
            else:
                self._status = Status.DEAD
                return
            
            self._collapsecount += 1
            
        self.rect = pygame.Rect(self._map.get_drawxentity(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)
