from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from game.core.state import Status
from game.core.settings import H, SCORE_ARRAY, ONEUP_SCORE, TILE_SIZE
from game.systems.number import Number

if TYPE_CHECKING:
    from game.entities.koopa import Koopa
    from game.entities.mario import Mario
    from game.levels.map import Map


class Entity(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, dir: int, mario: Mario, map: Map):
        pygame.sprite.Sprite.__init__(self)
                
        # The coordinate for map and the location of Mario are different.
        # Entity location coordinate        
        self._rawrect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        # Entity coordinate for Map
        self.rect = self._rawrect
        
        # Get a map
        self._map: Map = map
        
        # X axle move distance
        self._dir: int = dir
        self._walkidx: int = 0
        
        # Y axle move
        self._vy: int = 0
        
        # Get mario 
        self._mario: Mario = mario

        # Status
        self._status = Status.NORMAL

        # Counter for collapse
        self._collapsecount: int = 0

    @property
    def status(self):
        """Get the status"""
        return self._status
    
    @status.setter
    def status(self, value):
        self._status = value
    
    @property
    def rawrect(self):
        return self._rawrect
    
    @property
    def dir(self):
        return self._dir
        
    def handle_projectile_contact(self) -> None:
        """
        Resolve collision with any Mario-owned projectile-like object.
        
        Iterate over 'mario.arriles including fireballs and koopa kicked).
        If one overlaps this entity, puts this entity into a Flying state, 
        chooses a horizontal direction away from the hitter, 
        and applies an upward impulse. 
        If the hitter implements 'on_projectile_contact' function, 
        delegate post-hit effects to it.
        
        Returns:
            None
        """
        # Koopa kick flying
        for marioarrly in self._mario.arrlies:
            if self._rawrect.colliderect(marioarrly.rawrect):
                self._status = Status.FLYING
                    
                # Decide the direction to fly
                self._dir = 3 if self._rawrect.centerx > marioarrly.rawrect.centerx else -3
                self._vy = -8
                
                # Execute on_projectile_contact function derived from Koopa and Fire objects
                if hasattr(marioarrly, 'on_projectile_contact'):
                    marioarrly.on_projectile_contact(self)
    
    def flying(self) -> None:
        """
        Let entity fly after Koopa kick hits and change the status to DEAD
        """
        self._rawrect.x += self._dir
        self._rawrect.y += self._vy
        self._vy += 1
            
        if self._rawrect.y >= H:
            # Disapear
            self._status = Status.DEAD
    
    def _handle_mario_hit(self) -> None:
        # If Mario hits Koopa
        if self._mario.vy > 0:
            # Squash
            self._status = Status.DEADING
                                
            # Mario jump action
            self._mario.status = Status.TREADING
            self._mario.vy = -5
            # Display score
            score = SCORE_ARRAY[self._mario.continuous_counter] if not self._mario.continuous_counter >= len(SCORE_ARRAY) else ONEUP_SCORE
            self._map.group.add(Number(self.rect.x, self.rect.y, score))
            self._map.add_score(score)
            self._mario.continuous_counter += 1
        else:
            # If Mario is invisible, then return.
            if self._mario.isinvisible and not self._mario.hasstar:
                return
            
            if self._mario.hasstar:
                self._status = Status.FLYING
                # Display score to be defeated by Star Mario
                self._map.group.add(Number(self.rect.x, self.rect.y, SCORE_ARRAY[1]))
                self._map.add_score(SCORE_ARRAY[1])
                return
            
            if self._mario.status != Status.TREADING:
                if self._mario.isbig:
                    self._mario.status = Status.SHRINKING
                    if self._mario.isfire:
                        self._mario.isfire = False
                else:
                    self._mario.status = Status.DEADING
            