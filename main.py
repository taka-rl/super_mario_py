import pygame
from enum import Enum, auto
import time


class Status(Enum):
    NORMAL = auto()
    DEADING = auto()
    DEAD = auto()
    TREADING = auto()
    SLIDING = auto()
    FLYING = auto()


# Display size
W, H = 320, 270

# Number of tiles
TILE_X, TILE_Y = 16, 14


class Map():
    NOMOVE_X = 120
    
    def __init__(self):      
        # Define map 
        self.__data = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 3, 2, 4, 5, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],            
        ]

        self.__imgs: dict = {
            1: pygame.image.load('./img/ground.jpg'),
            2: pygame.image.load('./img/block.jpg'),
            3: pygame.image.load('./img/question_block.jpg'),
            4: pygame.image.load('./img/panel.jpg'),
            5: pygame.image.load('./img/coin.jpg'),
            6: pygame.image.load('./img/kinoko.jpg'),
            7: pygame.image.load('./img/star.jpg'),
            8: pygame.image.load('./img/1upkinoko.jpg')
        }
        
        # Map shifts relative to Mario's position
        self.__drawmargin: int = 0
    
    def draw(self, win: pygame.display, rect: pygame.rect) -> None:
        """
        Draw the visible area of the game map on the screen based on Mario's current position.
    
        The function determines which tiles are visible in the viewport by calculating the appropriate
        starting position and adjusting for Mario's horizontal movement. Only the visible tiles are drawn 
        to improve performance by avoiding unnecessary rendering of off-screen tiles.
            
        The startx variable is calculated based on Mario’s current x-position (rect.x), 
        ensuring that the map moves in sync with Mario. If Mario is far enough along the x-axis, 
        the map will start scrolling to the left to keep Mario in view.

        The margin is used to adjust for the sub-tile movement 
        when the x position of Mario isn't exactly divisible by the tile size (20 pixels). 
        This margin value shifts the map so that Mario’s position remains correct in the game world.

        So, the purpose of __drawmargin is to handle the adjustment needed 
        when the map shifts relative to Mario’s position.

        Args:
            win (pygame.display): Map window
            rect (pygame.rect): 
                The rectangle representing Mario's current position. 
                This is used to calculate the portion of the map that should be displayed.
        
        Returns:
            None
        """
        margin = 0
        
        # Mario start position
        if rect.x <= self.NOMOVE_X:
            startx = 0
        else:
            startx = rect.x // 20 - self.NOMOVE_X // 20
            margin = rect.x % 20
        
        # Horizontal offset in Mario's position
        self.__drawmargin = -startx * 20 -margin
        
        # Draw a map
        for y in range(TILE_Y):
            for x in range(startx, startx + TILE_X + 1):
                map_num = self.__data[y][x]
                if map_num > 0:
                    win.blit(self.__imgs[map_num], ((x - startx) * 20 - margin, y * 20))

    def chk_collision(self, rect: pygame.rect) -> bool:
        """
        Check for collision between a given rectangular area (rect) and the tiles
        in the game map. The function checks the four tiles surrounding the top-left
        corner of the given rectangle. If any of these tiles contain an obstacle 
        (represented by non-zero values in the map) and the given rectangle collides
        with the corresponding tile's area. 
        
        Args:
            rect (pygame.rect): Targeted rect to be checked collision

        Returns:
            bool: Return True to indicate a collision, otherwise it returns False
        """
    
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

    def get_drawx(self, rect: pygame.rect) -> int:
        """X coordinate to draw Mario on the map"""
        if rect.x < self.NOMOVE_X:
            x = rect.x
        else:
            x = self.NOMOVE_X
        return x

    def get_drawxenemy(self, rect: pygame.rect) -> int:
        """
        Calculate the correct X coordinate to draw enemy on the screen based on the map's scrolling position.
        This function accounts for the scrolling margin and adjusts the enemy's horizontal position accordingly.
        The position is calculated relative to the current map view, ensuring that enemies are drawn correctly 
        in the viewport and move with the map.

        Args:
            rect (pygame.rect): The rectangle representing the enemy's current position on the map.

        Returns:
            int: The calculated x-coordinate where the enemy should be drawn on the screen.
        
        """
        return rect.x + self.__drawmargin


class Mario(pygame.sprite.Sprite):
    """Mario class"""
    
    WALK_ANIME_IDX = [0, 0, 1, 1, 2, 2]
    MAX_SPEED_X: int = 5
    ACC_SPEED_X: float = 0.25
    DASH_SPPED_X: int = 8
    MAX_JUMP_Y = 7
    DASH_JUMP_Y = 10
    
    def __init__(self, map):
        pygame.sprite.Sprite.__init__(self)
        
        # Flag for Mario direction
        self.__isleft: bool = False
        
        # idx for walking animation
        self.__walkidx: int = 0

        # Y axle move distance
        self.__vy: int = 0
        
        # X axle move distance 
        self.__vx: float = 0
        
        # Flag for dash
        self.__isdash = False
        
        # Cumulative ascent distance
        self.__ay: int = 0
        
        # Judge if Mario is on ground
        self.__on_ground: bool = False

        # Status
        self.__status = Status.NORMAL
        
        # Array for Koopa kick
        self._arrlies: list = []

        # Anime counter
        self.__animecounter: int = 0
        
        # Load mario images
        self.__imgs: list = [
            pygame.image.load('./img/mario_1.jpg'),
            pygame.image.load('./img/mario_2.jpg'),
            pygame.image.load('./img/mario_3.jpg'),
            pygame.image.load('./img/mario_death.jpg'),
            pygame.image.load('./img/mario_jump.jpg')
        ]
        
        self.image = self.__imgs[0]
        
        # The coordinate for map and the location of Mario are different.
        # Mario location coordinate        
        self.__rawrect = pygame.Rect(30, 180, 20, 20)
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
    
    @property
    def arrlies(self):
        return self._arrlies
    
    def update(self):
        if self.__status == Status.DEAD:
            pass
            
        if self.__status == Status.DEADING:
            self.image = self.__imgs[3]
            self.__deading()
            self.rect = pygame.Rect(self.__map.get_drawx(self.__rawrect), self.__rawrect.y, self.__rawrect.width, self.__rawrect.height)
            return
        
        # Get key status
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.__right()
            
        if keys[pygame.K_LEFT]:
            self.__left()
        
        if keys[pygame.K_SPACE]:
            self.__jump()
        else:
            # When Space isn't inputed
            if self.__vy <= -5:
                # Don't fall down imediately
                self.__vy = -3
            if self.__vy >= 0:
                # Status is Normal when falling down
                self.__status = Status.NORMAL
        
        # Dash with left shift
        self.__isdash = keys[pygame.K_LSHIFT]
            
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and self.__vx != 0:
            self.__stop()
                    
        # Move for Y axle
        # if not self.__on_ground:
        self.__vy += 1
        self.__rawrect.y += self.__vy
        
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
        
        # Choose the stop mario image
        if self.__vx == 0:
            imageidx = 0
        else:
            imageidx = self.WALK_ANIME_IDX[self.__walkidx % 6]
        
        # Choose the jump mario image
        if not self.__on_ground:
            imageidx = 4
            
        # Change the image direction 
        self.image = pygame.transform.flip(self.__imgs[imageidx], self.__isleft, False)        
    
        # Update rect for Splite
        self.rect = pygame.Rect(self.__map.get_drawx(self.__rawrect), self.__rawrect.y, self.__rawrect.width, self.__rawrect.height)
        
    def move(self):
        self.__walkidx += 1
        
        # Collision check
        if self.__map.chk_collision(self.__rawrect):
            self.__rawrect.x = (self.__rawrect.x // 20 + (1 if self.__isleft else 0)) * 20     
    
    def __right(self):
        if not self.__isdash:
            if self.__vx > self.MAX_SPEED_X:
                self.__vx -= self.ACC_SPEED_X
            else:
                self.__vx = (self.__vx + self.ACC_SPEED_X) if self.__vx < self.MAX_SPEED_X else self.MAX_SPEED_X
        else:
            # Dash
            self.__vx = (self.__vx + self.ACC_SPEED_X) if self.__vx < self.DASH_SPPED_X else self.DASH_SPPED_X
        
        # Cancel law of inertia when changing the direction.
        if self.__isleft:
            self.__vx = 0
        
        self.__rawrect.x += self.__vx
        self.__isleft = False
        self.move()

    def __left(self):
        if not self.__isdash:
            if self.__vx < -1 * self.MAX_SPEED_X:
                self.__vx += self.ACC_SPEED_X
            else:
                self.__vx = (self.__vx - self.ACC_SPEED_X) if self.__vx > -1 * self.MAX_SPEED_X else -1 * self.MAX_SPEED_X
        else:
            # Dash
            self.__vx = (self.__vx - self.ACC_SPEED_X) if self.__vx > -1 *  self.DASH_SPPED_X else -1 * self.DASH_SPPED_X
        
        # Cancel law of inertia when changing the direction.
        if not self.__isleft:
            self.__vx = 0
        
        self.__rawrect.x += self.__vx
        self.__isleft = True
        self.move()        
        
    def __jump(self):
        # If Mario is on ground, he can jump
        if self.__on_ground:
            if abs(self.__vx) == self.DASH_SPPED_X:
                # Dash jump
                self.__vy -= self.DASH_JUMP_Y
            else:
                self.__vy -= self.MAX_JUMP_Y  
            # self.__vy = -7
            self.__ay = 0
            self.__on_ground = False
        
        if self.__vy < 0:
            # Keep jumping until ay reaches 65
            if self.__ay < 65:
                self.__vy -= 1
                self.__ay -= self.__vy
    
    def __stop(self):
        self.__vx = self.__vx + self.ACC_SPEED_X * (1 if self.__isleft else -1)
        self.__rawrect.x += self.__vx
        
        # Collision check to prevent going into blocks by inertia 
        if self.__map.chk_collision(self.__rawrect):
            self.__rawrect.x = (self.__rawrect.x // 20 + (1 if self.__isleft else 0)) * 20
    
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
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, dir, mario, map):
        pygame.sprite.Sprite.__init__(self)
                
        # The coordinate for map and the location of Mario are different.
        # Enemy location coordinate        
        self._rawrect = pygame.Rect(x, y, 20, 20)
        # Enemy coordinate for Map
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
    
    @property
    def rawrect(self):
        return self._rawrect
    
    def move_and_collide(self):
        """
        Let enemy move and check its collision. 
        """
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
    
    def kickHit(self) -> None:
        """
        Judge if Koopa kick hits or not. If it hits, the status is changed to FLYING.
        """
        # Koopa kick flying
        for marioarrly in self._mario.arrlies:
            if self._rawrect.colliderect(marioarrly):
                self._status = Status.FLYING
                    
                # Decide the direction to fly
                self._dir = 3 if self._rawrect.centerx > marioarrly.centerx else -3
                self._vy = -8
    
    def flying(self) -> None:
        """
        Let enemy fly after Koopa kick hits and change the status to DEAD
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
                        
        else:
            if self._mario.status != Status.TREADING:
                self._mario.status = Status.DEADING    

class Koopa(Enemy):
    WALK_SPEED = 6
    WALK_ANIME_IDX = [0, 0, 0, 1, 1, 1]
    
    def __init__(self, x, y, dir, mario, map):
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
        # Not update if Mario is dead
        if self._mario.status == Status.DEADING:
            return
        
        if self._status == Status.DEADING:
            self.image = self.__imgs[2]
            # Update rect for Splite
            self.rect = pygame.Rect(self._map.get_drawxenemy(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)
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

        # Flying if Koopa kick hits goomba
        if self._status == Status.FLYING:
            super().flying()
            # self._rect = self._map.get_drawxenemy(self._rawrect), self._rawrect.top
            self.image = pygame.transform.flip(self.__imgs[0], False, True)
        
        if self._status == Status.NORMAL:
            # Koopa kick flying
            super().kickHit()

        if self._status == Status.NORMAL or self._status == Status.SLIDING:
            
            super().move_and_collide()
            
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
                    self._mario.arrlies.append(self._rawrect)
                    
                elif self._status == Status.SLIDING:
                    super()._handle_mario_hit()
                                    
        # Update rect for Splite
        self.rect = pygame.Rect(self._map.get_drawxenemy(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)


class Goomba(Enemy):
    WALK_SPEED = 6
    
    def __init__(self, x, y, dir, mario, map):
        # Load goomba images        
        self.__imgs: list = [
            pygame.image.load('./img/goomba.jpg'),
            pygame.image.load('./img/goomba_death.jpg'),
        ]

        self.image = self.__imgs[0]
        super().__init__(x, y, dir, mario, map)

    
    def update(self):
        # Not update if Mario is dead
        if self._mario.status == Status.DEADING:
            return
        
        if self._status == Status.DEADING:
            self.image = self.__imgs[1]
            # Update rect for Splite
            self.rect = pygame.Rect(self._map.get_drawxenemy(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)
            self._collapsecount += 1
            if self._collapsecount == 30:
                self._status = Status.DEAD
            return
        
        if self._status == Status.DEAD:
            pass
        
        # Flying if Koopa kick hits goomba
        if self._status == Status.FLYING:
            super().flying()
            # self._rect = self._map.get_drawxenemy(self._rawrect), self._rawrect.top
            self.image = pygame.transform.flip(self.__imgs[0], False, True)
        
        if self._status == Status.NORMAL:
            super().move_and_collide()
                
            self._walkidx += 1
            if self._walkidx == self.WALK_SPEED:
                self._walkidx = 0
            
            self.image = pygame.transform.flip(self.__imgs[0], self._walkidx < self.WALK_SPEED // 2, False)
            
            # Collision check
            if self._rawrect.colliderect(self._mario.rawrect):
                super().__handle_mario_hit()
            
            # Koopa kick flying
            super().kickHit()
        
        # Update rect for Splite
        self.rect = pygame.Rect(self._map.get_drawxenemy(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)

        
def init():
     # Define Sprite group
    group = pygame.sprite.RenderUpdates()
    
    # Map class
    map = Map()
    
    # Mario class
    mario = Mario(map)
    
    # Goomba class
    goombas = [
        Koopa(200, 180, -2, mario, map),
        Koopa(220, 180, -2, mario, map),
        Goomba(250, 180, -2, mario, map),
        Goomba(270, 180, -2, mario, map),
        Koopa(310, 180, -2, mario, map),
    ]
    
    # Add mario into the group
    group.add(mario)
    
    # Add goomba into the group
    group.add(goombas)
    
    return group, mario, goombas, map


def main():
    """main function"""
    
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
    