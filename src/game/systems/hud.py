import pygame
from game.core.settings import WHITE


class HeadUpDisplay:
    def __init__(self) -> None:
        self.__font = pygame.font.SysFont("Arial", size=18)
        
    def __create_text_surface(self, word: str, char_color=WHITE) -> pygame.font:
        """
        Create a text surface.
        Args:
            chars (str): Strings to be displayed for the text surface
            char_color (tuple): String color is white as default
                    
        Returns:
            pygame.font: text surface        
        
        """ 
        return self.__font.render(word, True, char_color)
        
    def __display_word(self, win: pygame.display, word: str, x: int, y: int) -> None:
        """Display chars in the window."""
        text_surface = self.__create_text_surface(word)
        win.blit(text_surface, (x, y))
    
    def draw(self, win: pygame.display, score: int, timer: float, coin: int, world: str):
        # Draw heads-up display on the window
        self.__display_word(win, 'MARIO', 30, 10)
        self.__display_word(win, 'WORLD', 180, 10)
        self.__display_word(win, world[5:], 190, 25)
        self.__display_word(win, 'TIME', 260, 10)
        self.__display_word(win, '{:06d}'.format(score), 30, 25)
        self.__display_word(win, 'C x ' + '{:02d}'.format(coin), 100, 25)
        self.__display_word(win, "{:03d}".format(int(timer)), 270, 25)
    
    def draw_game_start(self, win: pygame.display, world: str, life_stocks: int):
        """Draw game start on the window before game starts."""
        # WORLD X-X
        self.__display_word(win, world[:5], 130, 110)
        self.__display_word(win, world[5:], 180, 110)
        
        # Mario image x life stocks
        self.__display_word(win, ' x ', 160, 140)
        self.__display_word(win, str(life_stocks), 180, 140)

    def draw_game_over(self, win: pygame.display):
        """Draw game over on the window."""
        self.__display_word(win, 'GAMEOVER', 120, 140)
    
    def draw_pause(self, win: pygame.display) -> None:
        """Draw Pause on the window"""
        self.__display_word(win, 'PAUSE', 120, 140)
        