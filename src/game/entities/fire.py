from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from game.entities.entity import Entity
from game.systems.number import Number
from game.core.state import Status
from game.core.settings import W, H, SMALL_TILE_SIZE, TILE_SIZE, SCORE_ARRAY

if TYPE_CHECKING:
    from game.entities.mario import Mario
    from game.levels.map import Map


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
                self._rawrect.y = (self._rawrect.y // TILE_SIZE + (1 if self._vy < 0 else 0)) * TILE_SIZE
                                    
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

    def on_projectile_contact(self, enemy: Entity) -> None:
        """
        Respond to hitting an enemy as a fireball.
        
        Marks this fireball as dying, removes it from Mario's active projectiles,
        and awards the base fireball score at the enemy's position.

        Args:
            enemy: The entity that was struck (already entering knockback).
        
        Returns:
            None
        """
        self._status = Status.DEADING
        self._mario.arrlies.remove(self)
        
        # Display score for Fira ball
        self._map.group.add(Number(enemy.rect.x, enemy.rect.y, SCORE_ARRAY[1]))
        self._map.add_score(SCORE_ARRAY[1])
        