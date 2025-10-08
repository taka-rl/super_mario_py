import pygame
from game.core.state import Status
from game.core.settings import GOAL_FALL_SPEED, WHITE


class Number(pygame.sprite.Sprite):   
    def __init__(self, x: int, y: int, score: int|str, map=None):
        pygame.sprite.Sprite.__init__(self)
        
        font_size: int = 14
        self.__font = pygame.font.SysFont("Arial", font_size)
        self.image: pygame.Surface = self.__create_surface(score)
        self.__counter: int = 0
        self.__status = Status.NORMAL
        
        self.__map = map
        if map is None:
            self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        else:
            # This is for the goal animation
            self.__rawrect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
            self.rect = pygame.Rect(self.__map.get_drawxentity(self.__rawrect), self.__rawrect.y, self.__rawrect.width, self.__rawrect.height)
        
    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, value):
        self.__status = value
        
    def __create_surface(self, score):
        """Generate a surface for score"""
        text_surface = self.__font.render(str(score), True, WHITE)
        surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
        surface.blit(text_surface, (0, 0))
        return surface

    def update(self):
        if self.__status == Status.NORMAL:
            # Move up
            self.rect.y -= 1
            # Disappear after 1 second
            if self.__counter == 30:
                self.__status = Status.DEAD
                
        if self.__status == Status.GOAL:
            self.rect = pygame.Rect(self.__map.get_drawxentity(self.__rawrect), self.__rawrect.y, self.__rawrect.width, self.__rawrect.height)
            if self.__counter < 32:
                self.__rawrect.y -= GOAL_FALL_SPEED
        
        self.__counter += 1
