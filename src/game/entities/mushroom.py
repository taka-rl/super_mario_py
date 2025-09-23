from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from entities.entity import Entity
from systems.number import Number
from core.state import Status
from core.settings import H, ONEUP_SCORE

if TYPE_CHECKING:
    from entities.mario import Mario
    from levels.map import Map
    

class Mushroom(Entity):    
    def __init__(self, x: int, y: int, dir: int, mario: Mario, map: Map, oneup=False):
        self.__imgs = [
            pygame.image.load('./img/kinoko.jpg'),
            pygame.image.load('./img/fireflower.jpg'),
            pygame.image.load('./img/1upkinoko.jpg'),
            ]
        self.image = self.__imgs[0]
        self._rawrect = pygame.Rect(x, y, 20, 20)
        
        self.__isflower: bool = False
        self.__isoneup: bool = oneup
        
        super().__init__(x, y, dir, mario, map)
    
    def update(self):
        # Not update if Mario is dead or growing or shrinking, or Game is paused
        if self._mario.status in [Status.DEADING, Status.GROWING, Status.SHRINKING, Status.PAUSE]:
            return
        
        # If Mario hit Mushroom box
        if self._status == Status.NORMAL:
            x, y = self._rawrect.x // 20, self._rawrect.y // 20
            if self._map.ispushedblock((y, x)):
                self._map.sound.play_sound_asnync(self._map.sound.play_item)
                self._status = Status.TREADING
                self._rawrect.y -= 5
                self.__isflower = not self.__isoneup and self._mario.isbig
            self.image.set_alpha(0)
        
        # Fall handling
        if self._rawrect.y > H:
            self._status = Status.DEAD
        
        # Mushroom is showing up
        elif self._status == Status.TREADING:
            self._walkidx += 1
            if self._walkidx == 4:
                self.image.set_alpha(255)
                
            if self._walkidx <= 15:
                self._rawrect.y -= 1
            # Once mushroom appears, then it stops
            if self._walkidx == 18:
                self._status = Status.FLYING
        
        # Mushroom is moving horizontally
        elif self._status == Status.FLYING:
            # If Mario is big, it plays as a flower, if not mushroom.
            if not self.__isflower:
                # X axle move
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
                        self._vy = 0
                    else:
                        # jump
                        self._vy = 1
            
            # Collision check with Mario
            if self._rawrect.colliderect(self._mario.rawrect):
                if self.__isoneup:
                    self._map.sound.play_sound_asnync(self._map.sound.play_oneup)
                    self._map.group.add(Number(self.rect.x, self.rect.y, ONEUP_SCORE))
                    self._status = Status.DEAD
                    # increment life stocks
                    self._map.increment_life_stocks()
                    # TODO: Add 1UP to self._map.value

                else:
                    if not self._mario.isfire:                    
                        self._mario.status = Status.GROWING
                        self._map.sound.play_sound_asnync(self._map.sound.play_power)
                        if self.__isflower:
                            self._mario.isfire = True
                    self._map.group.add(Number(self.rect.x, self.rect.y, 1000))
                    self._map.add_score(1000)
                    self._status = Status.DEAD
                            
        self.image = self.__imgs[2 if self.__isoneup else 0 if not self._mario.isbig else 1]
        self.rect = pygame.Rect(self._map.get_drawxentity(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)
        