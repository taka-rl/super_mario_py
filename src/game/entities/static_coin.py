from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from game.entities.entity import Entity
from game.core.state import Status
from game.core.settings import TILE_SIZE

if TYPE_CHECKING:
    from game.entities.mario import Mario
    from game.levels.map import Map


class StaticCoin(Entity):
    def __init__(self, x: int, y: int, dir: int, mario: Mario, map: Map):
        self.__imgs: list = [
            # TODO: Update the image to meet the sub stage background color
            pygame.image.load('./img/coin.jpg'),
        ]
        self.image = self.__imgs[0]
        
        self._rawrect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        super().__init__(x, y, dir, mario, map)
    
    def update(self):
        if self._rawrect.colliderect(self._map.mario.rawrect):
            self._status = Status.DEAD
            self._map.sound.play_sound_asnync(self._map.sound.play_coin)
            self._map.add_coin()
        
        self.rect = pygame.Rect(self._map.get_drawxentity(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)
