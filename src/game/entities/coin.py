from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from game.core.state import Status
from game.core.settings import TILE_SIZE
from game.systems.number import Number
from game.entities.entity import Entity
from game.core import assets

if TYPE_CHECKING:
    from game.entities.mario import Mario
    from game.levels.map import Map


class Coin(Entity):
    
    # ANIME_IDX = [0, 1, 2, 3]
    
    IMAGE_FILES: tuple[str, ...] = ('./img/coin.jpg',)
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
        self.image = self.__imgs[0].copy()
        
        super().__init__(x, y, dir, mario, map)
    
    def update(self):
        # Not update if Mario is dead or growing or shrinking or Game is paused
        if self._mario.status in [Status.DEADING, Status.GROWING, Status.SHRINKING, Status.PAUSE]:
            return
        
        if self._status == Status.NORMAL:
            x, y = self._rawrect.x // TILE_SIZE, self._rawrect.y // TILE_SIZE
            
            # Block with coins is pushed
            if self._map.ispushedblock((y, x)):
                self._map.sound.play_sound_asnync(self._map.sound.play_coin)
                self._map.add_coin()
                self._status = Status.FLYING
                self._vy = -15
                self._rawrect.y -= TILE_SIZE
                return
            # Coin is invisible
            self.image.set_alpha(0)
        
        elif self._status == Status.FLYING:
            # Reset the invisible and coin appears
            self.image.set_alpha(255)
            self._vy += 2
            self._rawrect.y += self._vy
            if self._vy > 10:
                self._status = Status.DEAD
                self._map.group.add(Number(self.rect.x, self.rect.y, 200))
                self._map.add_score(200)
                return
            
            # TODO: Coin animation
            # self.image = self.__imgs[self.ANIME_IDX[self._walkidx]]
            # self._walkidx += 1
    
        self.rect.topleft = (self._map.get_drawxentity(self._rawrect), self._rawrect.y)
