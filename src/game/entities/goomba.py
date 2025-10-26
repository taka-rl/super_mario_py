from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from game.entities.entity import Entity
from game.core.state import Status
from game.core.settings import H, TILE_SIZE
from game.core import assets

if TYPE_CHECKING:
    from game.entities.mario import Mario
    from game.levels.map import Map
    

class Goomba(Entity):
    WALK_SPEED = 6
    
    IMAGE_FILES: tuple[str, ...] = ('./img/goomba.jpg', './img/goomba_death.jpg',)
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
        # Load goomba images        
        self.__imgs: tuple = self.images()

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
            self.rect.topleft = (self._map.get_drawxentity(self._rawrect), self._rawrect.y)
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
                    self.rect.topleft = (self._map.get_drawxentity(self._rawrect), self._rawrect.y)
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
            super().handle_projectile_contact()
        
        # Update rect for Splite
        self.rect.topleft = (self._map.get_drawxentity(self._rawrect), self._rawrect.y)