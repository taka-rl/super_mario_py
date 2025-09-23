from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from entities.entity import Entity
from core.state import Status
from core.settings import H, TILE_SIZE

if TYPE_CHECKING:
    from entities.mario import Mario
    from levels.map import Map
    

class Goomba(Entity):
    WALK_SPEED = 6
    
    def __init__(self, x: int, y: int, dir: int, mario: Mario, map: Map):
        # Load goomba images        
        self.__imgs: list = [
            pygame.image.load('./img/goomba.jpg'),
            pygame.image.load('./img/goomba_death.jpg'),
        ]

        self.image = self.__imgs[0]
        super().__init__(x, y, dir, mario, map)

    
    def update(self):
        # Not update if Mario is dead or growing or shrinking or Game is paused
        if self._mario.status in [Status.DEADING, Status.GROWING, Status.SHRINKING, Status.PAUSE]:
            return

        # Fall handling
        if self._rawrect.y > H:
            self._status = Status.DEAD
        
        if self._status == Status.DEADING:
            self.image = self.__imgs[1]
            # Update rect for Splite
            self.rect = pygame.Rect(self._map.get_drawxentity(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)
            self._collapsecount += 1
            if self._collapsecount == 30:
                self._status = Status.DEAD
            return
        
        if self._status == Status.DEAD:
            pass
        
        # Flying if Koopa kick hits goomba
        if self._status == Status.FLYING:
            super().flying()
            # self._rect = self._map.get_drawxenemy(self._rawrect), self._rawrect.top
            self.image = pygame.transform.flip(self.__imgs[0], False, True)
        
        if self._status == Status.NORMAL:
            # X axle move
            self._rawrect.x += self._dir
            
            # X axle collision check
            if self._map.chk_collision(self._rawrect):
                self._rawrect.x = (self._rawrect.x // TILE_SIZE + (1 if self._dir < 0 else 0)) * TILE_SIZE
                self._dir *= -1
                    
            # Y axle move
            self._vy += 1
            self._rawrect.y += self._vy
                
            # Y axle collision check
            if yx := self._map.chk_collision(self._rawrect):
                self._rawrect.y = (self._rawrect.y // TILE_SIZE + (1 if self._vy < 0 else 0)) * TILE_SIZE
                # If a block is pushedW
                if self._map.ispushedblock(yx):
                    self._status = Status.FLYING
                    self._dir = 3 if self._rawrect.centerx > self._mario.rawrect.centerx else -3
                    self._vy = -8
                    
                    self.image = pygame.transform.flip(self.__imgs[0], False, True)
                    # Update rect for Splite
                    self.rect = pygame.Rect(self._map.get_drawxentity(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)
                    return
                
                if self._vy > 0:
                    self._vy = 0
                else:
                    # jump
                    self._vy = 1

            self._walkidx += 1
            if self._walkidx == self.WALK_SPEED:
                self._walkidx = 0
            
            self.image = pygame.transform.flip(self.__imgs[0], self._walkidx < self.WALK_SPEED // 2, False)
            
            # Collision check
            if self._rawrect.colliderect(self._mario.rawrect):
                super()._handle_mario_hit()
            
            # Koopa kick flying
            super().kickHit()
        
        # Update rect for Splite
        self.rect = pygame.Rect(self._map.get_drawxentity(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)
