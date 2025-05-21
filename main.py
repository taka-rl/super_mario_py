import pygame
from enum import Enum, auto
import time


class Status(Enum):
    NORMAL = auto()
    DEADING = auto()
    DEAD = auto()


# Display size
W, H = 320, 270

# Number of tiles
TILE_X, TILE_Y = 16, 14


class Map():
    NOMOVE_X = 120
    
    def __init__(self):        
        # Define map 
        self.__data = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],            
        ]

        self.__imgs: dict = {
            1: pygame.image.load('./img/ground.jpg'),
            2: pygame.image.load('./img/block.jpg'),
        }    
    
    def draw(self, win: pygame.display, rect: pygame.rect) -> None:
        '''Draw a map'''
        margin = 0
        
        # Mario start position
        if rect.x <= self.NOMOVE_X:
            startx = 0
        else:
            startx = rect.x // 20 - self.NOMOVE_X // 20
            margin = rect.x % 20
        
        for y in range(TILE_Y):
            for x in range(startx, startx + TILE_X + 1):
                map_num = self.__data[y][x]
                if map_num > 0:
                    win.blit(self.__imgs[map_num], ((x - startx) * 20 - margin, y * 20))

    def chk_collision(self, rect: pygame.rect) -> bool:
        '''
        Check for collision between a given rectangular area (rect) and the tiles
        in the game map. The function checks the four tiles surrounding the top-left
        corner of the given rectangle. If any of these tiles contain an obstacle 
        (represented by non-zero values in the map) and the given rectangle collides
        with the corresponding tile's area, the function returns True to indicate 
        a collision. Otherwise, it returns False.
        '''
        
        # Convert the top-left position of the rectangle to the corresponding tile indices
        xidx, yidx = rect.x // 20, rect.y // 20
        
        # Check the 2x2 grid of tiles surrounding the rectangle's top-left corner
        for y in range(2):
            for x in range(2):
                # If the tile contains an obstacle (non-zero value) and the rectangle 
                # collides with the tile's area, return True (collision detected)
                if self.__data[yidx + y][xidx + x] and rect.colliderect(
                    pygame.Rect((xidx + x) * 20, (yidx + y) * 20, 20, 20)):
                    return True
        return False

    def get_drawx(self, rect: pygame.rect):
        if rect.x < self.NOMOVE_X:
            x = rect.x
        else:
            x = self.NOMOVE_X
        return x


class Mario(pygame.sprite.Sprite):
    '''Mario class'''
    
    WALK_ANIME_IDX = [0, 0, 1, 1, 2, 2]
    
    def __init__(self, map):
        pygame.sprite.Sprite.__init__(self)
        
        # Flag for Mario direction
        self.__isleft: bool = False
        
        # idx for walking animation
        self.__walkidx: int = 0

        # Y axle move distance
        self.__vy: int = 0
        
        # Judge if Mario is on ground
        self.__on_ground: bool = False

        # Status
        self.__status = Status.NORMAL

        # Anime counter
        self.__animecounter: int = 0
        
        # Load mario images
        self.__imgs: list = [
            pygame.image.load('./img/mario_1.jpg'),
            pygame.image.load('./img/mario_2.jpg'),
            pygame.image.load('./img/mario_3.jpg'),
            pygame.image.load('./img/mario_death.jpg'),
        ]
        
        self.image = self.__imgs[0]
        
        # The coordinate for map and the location of Mario are different.
        # Mario location coordinate        
        self.__rawrect = pygame.Rect(150, 180, 20, 20)
        # Mario coordinate for Map
        self.rect = self.__rawrect
        
        # Get a map
        self.__map: Map = map
    
    @property
    def vy(self):
        return self.__vy
    
    @vy.setter
    def vy(self, value):
        self.__vy = value
        
    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, value):
        self.__status = value
    
    @property
    def rawrect(self):
        return self.__rawrect
    
    def update(self):
        if self.__status == Status.DEAD:
            pass
            
        if self.__status == Status.DEADING:
            self.image = self.__imgs[3]
            self.__deading()
            return
        
        # Get key status
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.__right()
            
        if keys[pygame.K_LEFT]:
            self.__left()
        
        if keys[pygame.K_SPACE]:
            self.__jump()
                    
        # Move for Y axle
        # if not self.__on_ground:
        self.__rawrect.y += self.__vy
        self.__vy += 1
        
        # Judge hitbox
        if self.__map.chk_collision(self.__rawrect):
            
            # If Mario is moving upward, it lets him go downward
            # vy is bigger than 0 -> 1 to go upward
            self.__rawrect.y = (self.__rawrect.y // 20 + (1 if self.__vy < 0 else 0)) * 20
            
            # Check if Mario is on ground 
            if self.__vy > 0:
                self.__on_ground = True
                self.__vy = 0
            else:
                self._vy = 1
        
        # temporary heigh is set 180 for on_ground
        # if self.__rawrect.y >= 180:
        #     self.__rawrect.y = 180
        #     self.__on_ground = True
        #     self.__vy = 0
        
        # Change the image direction 
        self.image = pygame.transform.flip(self.__imgs[self.WALK_ANIME_IDX[self.__walkidx % 6]], self.__isleft, False)
        
        # Update rect for Splite
        self.rect = pygame.Rect(self.__map.get_drawx(self.__rawrect), self.__rawrect.y, self.__rawrect.width, self.__rawrect.height)
        
    def __right(self):
        self.__rawrect.x += 5
        self.__walkidx += 1
        self.__isleft = False
        
        # Collision check
        if self.__map.chk_collision(self.__rawrect):
            self.__rawrect.x = (self.__rawrect.x // 20 + (1 if self.__isleft else 0)) * 20
        
    
    def __left(self):
        self.__rawrect.x -=5
        self.__walkidx += 1
        self.__isleft = True
        
        # Collision check
        if self.__map.chk_collision(self.__rawrect):
            self.__rawrect.x = (self.__rawrect.x // 20 + (1 if self.__isleft else 0)) * 20
        
        
    def __jump(self):
        if self.__on_ground:
            self.__vy = -10
            self.__on_ground = False
    
    def __deading(self):
        if self.__animecounter == 0:
            self.__vy = -10
        
        if self.__animecounter > 10:
            self.__vy += 1
            self.__rawrect.y += self.__vy
        
        if self.__rawrect.y > H + 20:
            self.__status = Status.DEAD
            return
         
        self.__animecounter += 1
        

class Goomba(pygame.sprite.Sprite):
    WALK_SPEED = 6
    
    def __init__(self, x, y, mario, map):
        pygame.sprite.Sprite.__init__(self)
        
        # Load goomba images        
        self.__imgs: list = [
            pygame.image.load('./img/goomba.jpg'),
            pygame.image.load('./img/goomba_death.jpg'),
        ]

        self.image = self.__imgs[0]
        self.rect = pygame.Rect(x, y, 20, 20)
        
        # Get a map
        self.__map: Map = map
        
        # X axle move distance
        self.__dir: int = -2
        self.__walkidx: int = 0
        
        # Y axle move
        self.__vy: int = 0
        
        # Get mario 
        self.__mario: Mario = mario

        # Status
        self.__status = Status.NORMAL

        # Counter for collapse
        self.__collapsecount: int = 0

    @property
    def status(self):
        '''Get the status'''
        return self.__status
    
    def update(self):
        # Not update if Mario is dead
        if self.__mario.status == Status.DEADING:
            return
        
        if self.__status == Status.DEADING:
            self.image = self.__imgs[1]
            self.__collapsecount += 1
            if self.__collapsecount == 30:
                self.__status = Status.DEAD
            return
        
        if self.__status == Status.DEAD:
            pass
        
        # X axle move
        self.rect.x += self.__dir
        
        # X axle collision check
        if self.__map.chk_collision(self.rect):
            self.rect.x = (self.rect.x // 20 + (1 if self.__dir < 0 else 0)) * 20
            self.__dir *= -1
        
        # Change the direction
        # if self.rect.x <= 0 or self.rect.x >= W - self.rect.width:
        #     self.__dir *= -1
            
        # Y axle move
        self.__vy += 1
        self.rect.y += self.__vy
        
        # Y axle collision check
        if self.__map.chk_collision(self.rect):
            self.rect.y = (self.rect.y // 20 + (1 if self.__vy < 0 else 0)) * 20
        
            if self.__vy > 0:
                self.__vy = 0
            else:
                # jump
                self.__vy = 1
            
        self.__walkidx += 1
        if self.__walkidx == self.WALK_SPEED:
            self.__walkidx = 0
        
        self.image = pygame.transform.flip(self.__imgs[0], self.__walkidx < self.WALK_SPEED // 2, False)
        
        # Collision check
        if self.rect.colliderect(self.__mario.rect):
            # If Mario hits Goomba
            if self.__mario.vy > 0:
                # Squash
                self.__status = Status.DEADING
                
                # Mario jump action
                self.__mario.vy = -5
            else:
                self.__mario.status = Status.DEADING
        

def init():
     # Define Sprite group
    group = pygame.sprite.RenderUpdates()
    
    # Map class
    map = Map()
    
    # Mario class
    mario = Mario(map)
    
    # Goomba class
    goombas = [
        # Goomba(250, 180, mario, map),
        # Goomba(270, 180, mario, map),
        # Goomba(310, 180, mario, map)
    ]
    
    # Add mario into the group
    group.add(mario)
    
    # Add goomba into the group
    group.add(goombas)
    
    return group, mario, goombas, map


def main():
    '''main function'''
    
    # Initialize pygame
    pygame.init()
    
    # Build a display
    win = pygame.display.set_mode((W, H))
    
    # Create clock rate
    clock = pygame.time.Clock()
    
    # Initialize sprite
    group, mario, goombas, map = init()
    
    # Event loop
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        # Fill in the background     
        win.fill((135, 206, 235))
        
        # Update the group
        group.update()
        
        # If Mario is dead
        if mario.status == Status.DEAD:
            time.sleep(2)
            group, mario, goombas, map = init()
            continue 
        
        # Remove DEAD status
        for goomba in goombas:
            if goomba.status == Status.DEAD:
                group.remove(goomba)
        
        # Draw map
        map.draw(win, mario.rawrect)
        
        # Draw the group
        group.draw(win)
                
        # Update the display
        pygame.display.flip()

        # Frame rate
        clock.tick(30)
    
    # End pygame
    pygame.quit()
                

if __name__ == '__main__':
    main()
    