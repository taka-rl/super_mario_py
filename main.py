import pygame


# Display size
W, H = 320, 270

# Number of tiles
TILE_X = 16
TILE_Y = 14


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
        
        # Load mario images
        self.__imgs = [
            pygame.image.load('./img/mario_1.jpg'),
            pygame.image.load('./img/mario_2.jpg'),
            pygame.image.load('./img/mario_3.jpg'),
        ]
        
        self.image = self.__imgs[0]
        self.rect = pygame.Rect(150, 180, 20, 20)
    
    
    def update(self):
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
        

class Goomba(pygame.sprite.Sprite):
    def __init__(self, x, y, mario):
        pygame.sprite.Sprite.__init__(self)
        
        # Load goomba images        
        self.__imgs = [
            pygame.image.load('./img/goomba.jpg'),
        ]

        self.image = self.__imgs[0]
        self.rect = pygame.Rect(x, y, 20, 20)
        
        # X axle move distance
        self.__dir = -2
    
    def update(self):
        # Move
        self.rect.x += self.__dir
        
        # Change the direction
        if self.rect.x <= 0 or self.rect.x >= W - self.rect.width:
            self.__dir *= -1
        
        
        

def main():
    '''main function'''
    
    # Initialize pygame
    pygame.init()
    
    # Build a display
    win = pygame.display.set_mode((W, H))
    
    # Create clock rate
    clock = pygame.time.Clock()
    
    # Define Sprite group
    group = pygame.sprite.RenderUpdates()
    
    # Mario class
    mario = Mario()
    
    # Goomba class
    goombas = [
        Goomba(270, 180, mario),
        Goomba(300, 180, mario)
    ]
    
    # Add mario into the group
    group.add(mario)
    
    # Add goomba into the group
    group.add(goombas)
    
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
    