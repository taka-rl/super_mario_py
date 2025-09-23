from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from entities.entity import Entity
from core.settings import SMALL_TILE_SIZE

if TYPE_CHECKING:
    from entities.mario import Mario
    from levels.map import Map


class BrokenBlock(Entity):
    def __init__(self, x: int, y: int, dir: int , vy: int, mario: Mario, map: Map):
        self.__imgs: list = [pygame.image.load('./img/crushed_block.jpg')]
        self.image = self.__imgs[0]
        
        self._rawrect = pygame.Rect(x, y, SMALL_TILE_SIZE, SMALL_TILE_SIZE)
        super().__init__(x, y, dir, mario, map)
        self._vy = vy
        
    def update(self):
        super().flying()
        self.rect = pygame.Rect(self._map.get_drawxentity(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)
