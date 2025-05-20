import pygame


# Display size
W, H = 320, 270

# Number of tiles
TILE_X = 16
TILE_Y = 14


class Mario(pygame.sprite.Sprite):
    '''Mario class'''
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        # Flag for Mario direction
        self.__isleft = False
        
        # Load mario images
        self.__imgs = [
            pygame.image.load('./img/mario_1.jpg'),
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
        
        # Change the image direction 
        self.image = pygame.transform.flip(self.__imgs[0], self.__isleft, False)
        
    
    def __right(self):
        self.rect.x += 5
        self.__isleft = False
    
    def __left(self):
        self.rect.x -=5
        self.__isleft = True
        


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
    
    # Add mario into the group
    group.add(mario)
    

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
    