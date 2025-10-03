from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from entities.entity import Entity
from systems.number import Number
from core.state import Status
from core.settings import TILE_SIZE, SCORE_ARRAY, ONEUP_SCORE

if TYPE_CHECKING:
    from entities.mario import Mario
    from levels.map import Map


class Koopa(Entity):
    WALK_SPEED = 6
    WALK_ANIME_IDX = [0, 0, 0, 1, 1, 1]
    
    def __init__(self, x: int, y: int, dir: int, mario: Mario, map: Map):
            # Load goomba images        
            self.__imgs: list = [
                pygame.image.load('./img/Koopa_1.jpg'),
                pygame.image.load('./img/Koopa_2.jpg'),
                pygame.image.load('./img/Koopa_death.jpg'),
                pygame.image.load('./img/Koopa_reborn.jpg'),
            ]

            self.image = self.__imgs[0]
            
            super().__init__(x, y, dir, mario, map)
        
    def update(self):
        # Not update if Mario is dead or growing or shrinking or Game is paused 
        if self._mario.status in [Status.DEADING, Status.GROWING, Status.SHRINKING, Status.PAUSE]:
            return
        
        if self._status == Status.DEADING:
            self.image = self.__imgs[2]
            # Update rect for Splite
            self.rect = pygame.Rect(self._map.get_drawxentity(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)
            self._collapsecount += 1
            
            if self._collapsecount >= 60:
                # Add an animation for reborn
                self.image = self.__imgs[3]
                
            # collapsecount is set 100 temporarily
            if self._collapsecount == 100:
                self._status = Status.NORMAL
                self._collapsecount = 0
                
                # move again after reborn
                self._dir = 2 if self._dir > 0 else -2
                
                # Remove Koopa from Mario's arrlies list if reborn
                for _ in range(len(self._mario.arrlies)):
                    if self._rawrect in self._mario.arrlies:
                       self._mario.arrlies.remove(self._rawrect)

        # Flying if Koopa kick hits goomba
        if self._status == Status.FLYING:
            super().flying()
            # self._rect = self._map.get_drawxenemy(self._rawrect), self._rawrect.top
            self.image = pygame.transform.flip(self.__imgs[0], False, True)
        
        if self._status == Status.NORMAL:
            # Koopa kick flying
            super().handle_projectile_contact()

        if self._status == Status.NORMAL or self._status == Status.SLIDING:
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

            if self._status == Status.NORMAL:
                self._walkidx += 1
                if self._walkidx == self.WALK_SPEED:
                    self._walkidx = 0
                    self.image = pygame.transform.flip(self.__imgs[self._walkidx < self.WALK_SPEED // 2], self._dir > 0, False)
            elif self._status == Status.SLIDING:
                # Image for Koopa kick
                self.image = self.__imgs[2]

        if self._status == Status.NORMAL or self._status == Status.SLIDING or self._status == Status.DEADING:
            # Collision check with Mario
            if self._rawrect.colliderect(self._mario.rawrect):
                    
                if self._status == Status.NORMAL:
                    super()._handle_mario_hit()
                                            
                elif self._status == Status.DEADING:
                    self._status = Status.SLIDING
                    # Koopa kick when Mario hits deading Koopa
                    if self._mario.vy > 0:
                        self._mario.status = Status.TREADING
                        self._mario.vy = -5
                    
                    # Decide the direction to slide
                    self._dir = 6 if self._mario.rawrect.centerx < self._rawrect.centerx else -6
                    
                    # add kicked Koopa rawrect into array
                    self._mario.arrlies.append(self)
                    
                elif self._status == Status.SLIDING:
                    super()._handle_mario_hit()
                                    
        # Update rect for Splite
        self.rect = pygame.Rect(self._map.get_drawxentity(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)

    def on_projectile_contact(self, enemy: Entity) -> None:
        """
        Award combo score when this kicked shell hits an enemy.

        Uses Mario's combo counter to compute the score, spawns a popup at the
        enemy's position, increments the counter for chaining, and leaves the
        shell physics unchanged.

        Args:
            enemy: The entity that was struck.
            
        Returns:
            None
        """
        score = SCORE_ARRAY[self._mario.continuous_counter] if not self._mario.continuous_counter >= len(SCORE_ARRAY) else ONEUP_SCORE
        self._map.group.add(Number(enemy.rect.x, enemy.rect.y, score))
        self._map.add_score(score)
        self._mario.continuous_counter += 1
        