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
TILE_X = 16
TILE_Y = 14


class Map():
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
            [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],            
        ]

        self.__imgs = {
            1: pygame.image.load('./img/ground.jpg'),
            2: pygame.image.load('./img/block.jpg'),
        }    
    
    def draw(self, win):
        '''Draw a map'''
        for y in range(TILE_Y):
            for x in range(TILE_X + 1):
                map_num = self.__data[y][x]
                if map_num > 0:
                    win.blit(self.__imgs[map_num], (x * 20, y * 20))


class Mario(pygame.sprite.Sprite):
    '''Mario class'''
    
    WALK_ANIME_IDX = [0, 0, 1, 1, 2, 2]
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        # Flag for Mario direction
        self.__isleft = False
        
        # idx for walking animation
        self.__walkidx = 0

        # Y axle move distance
        self.__vy = 0
        
        # Judge if Mario is on ground
        self.__on_ground = False

        # Status
        self.__status = Status.NORMAL

        # Anime counter
        self.__animecounter = 0
        
        # Load mario images
        self.__imgs = [
            pygame.image.load('./img/mario_1.jpg'),
            pygame.image.load('./img/mario_2.jpg'),
            pygame.image.load('./img/mario_3.jpg'),
            pygame.image.load('./img/mario_death.jpg'),
        ]
        
        self.image = self.__imgs[0]
        self.rect = pygame.Rect(150, 180, 20, 20)
    
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
        if not self.__on_ground:
            self.rect.y += self.__vy
            self.__vy += 1
        
        # temporary heigh is set 180 for on_ground
        if self.rect.y >= 180:
            self.rect.y = 180
            self.__on_ground = True
            self.__vy = 0
        
        # Change the image direction 
        self.image = pygame.transform.flip(self.__imgs[self.WALK_ANIME_IDX[self.__walkidx % 6]], self.__isleft, False)
        
    def __right(self):
        self.rect.x += 5
        self.__walkidx += 1
        self.__isleft = False
    
    def __left(self):
        self.rect.x -=5
        self.__walkidx += 1
        self.__isleft = True
        
    def __jump(self):
        if self.__on_ground:
            self.__vy = -10
            self.__on_ground = False
    
    def __deading(self):
        if self.__animecounter == 0:
            self.__vy = -10
        
        if self.__animecounter > 10:
            self.__vy += 1
            self.rect.y += self.__vy
        
        if self.rect.y > H + 20:
            self.__status = Status.DEAD
            return
         
        self.__animecounter += 1
        

class Goomba(pygame.sprite.Sprite):
    WALK_SPEED = 6
    
    def __init__(self, x, y, mario):
        pygame.sprite.Sprite.__init__(self)
        
        # Load goomba images        
        self.__imgs = [
            pygame.image.load('./img/goomba.jpg'),
            pygame.image.load('./img/goomba_death.jpg'),
        ]

        self.image = self.__imgs[0]
        self.rect = pygame.Rect(x, y, 20, 20)
        
        # X axle move distance
        self.__dir = -2
        self.__walkidx = 0
        
        # Get mario 
        self.__mario = mario

        # Status
        self.__status = Status.NORMAL

        # Counter for collapse
        self.__collapsecount = 0

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
        
        # Move
        self.rect.x += self.__dir
        
        # Change the direction
        if self.rect.x <= 0 or self.rect.x >= W - self.rect.width:
            self.__dir *= -1
            
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
    
    # Mario class
    mario = Mario()
    
    # Goomba class
    goombas = [
        Goomba(270, 180, mario),
        Goomba(300, 180, mario)
    ]
    
    # Map class
    map = Map()
    
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
        map.draw(win)
        
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
    