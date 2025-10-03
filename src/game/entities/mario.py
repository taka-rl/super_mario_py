import pygame
from entities.fire import Fire
from core.state import Status
from core.settings import H, GOAL_FALL_SPEED, GOAL_BOTTOM_Y, TILE_SIZE, SMALL_TILE_SIZE
from levels.map import Map


class Mario(pygame.sprite.Sprite):
    """Mario class"""
    
    WALK_ANIME_IDX = [0, 0, 1, 1, 2, 2]
    WALK_ANIME_BIG_IDX = [6, 6, 7, 7, 8, 8]
    WALK_ANIME_FIRE_IDX = [10, 10, 11, 11, 12, 12]
    MAX_SPEED_X: int = 5
    ACC_SPEED_X: float = 0.25
    DASH_SPEED_X: int = 8
    MAX_JUMP_Y = 7
    DASH_JUMP_Y = 10
    
    def __init__(self, map: Map, group: pygame.sprite.Group):
        pygame.sprite.Sprite.__init__(self)
        
        # Load mario images
        self.__imgs: list = [
            pygame.image.load('./img/mario_1.jpg'),
            pygame.image.load('./img/mario_2.jpg'),
            pygame.image.load('./img/mario_3.jpg'),
            pygame.image.load('./img/mario_death.jpg'),
            pygame.image.load('./img/mario_jump.jpg'),
            pygame.image.load('./img/mario_middle.jpg'),
            pygame.image.load('./img/mario_big_1.jpg'),
            pygame.image.load('./img/mario_big_2.jpg'),
            pygame.image.load('./img/mario_big_3.jpg'),
            pygame.image.load('./img/mario_big_jump.jpg'),
            pygame.image.load('./img/mario_fire_1.jpg'),
            pygame.image.load('./img/mario_fire_2.jpg'),
            pygame.image.load('./img/mario_fire_3.jpg'),
            pygame.image.load('./img/mario_fire_jump.jpg'),
            pygame.image.load('./img/mario_sit.jpg'),
            pygame.image.load('./img/mario_fire_sit.jpg'),
            # TODO: Add images of falling down to the goal pole for the goal animation
            ]
        
        self.image = self.__imgs[0]
        
        # The coordinate for map and the location of Mario are different.
        # Mario location coordinate        
        self.__rawrect = pygame.Rect(30, 220, TILE_SIZE, TILE_SIZE)
        # Mario coordinate for Map
        self.rect = self.__rawrect
        
        # Get a map
        self.__map: Map = map

        # Set Mario to Map
        self.__map.mario = self

        # Set a group for Sprite
        self.__group = group
        
        # Common initialization
        self.__common_init()
    
    def __common_init(self):
        self.image = self.__imgs[0]

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
        self.__status = Status.OPENING
        
        # Array for Koopa kick/fire ball
        self._arrlies: list = []

        # Counter for crushing enemies continuously
        self.__continuous_counter : int = 0
        
        # Anime counter
        self.__animecounter: int = 0
        
        # Growing counter
        self.__growcounter: int = 0
        
        # Grown Mario
        self.__isbig: bool = False
        
        # Invisible
        self.__isinvisible: bool = False
        self.__invisiblecounter: int = 90

        # Warping
        self.__next_data: tuple = None
        self.__warpcounter: int = 0
        
        # Star Mario
        self.__hasstar: bool = False
        
        # Fire Mario
        self.__isfire: bool = False
        
        # Sit Mario
        self.__issit: bool = False
    
    def init_dead(self) -> pygame.sprite:
        """Initialize when Mario is dead."""
        group, group_bg = self.__map.init_dead()
        self.__group = group
        self.__rawrect = pygame.Rect(30, 220, TILE_SIZE, TILE_SIZE)
        self.__common_init()
        return group, group_bg
    
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
    
    @property
    def isbig(self):
        return self.__isbig
    
    @property
    def isinvisible(self):
        return self.__isinvisible
    
    @isinvisible.setter
    def isinvisible(self, value):
        self.__isinvisible = value

    @property
    def invisiblecounter(self):
        return self.__invisiblecounter

    @invisiblecounter.setter
    def invisiblecounter(self, value):
        self.__invisiblecounter = value

    @property
    def hasstar(self):
        return self.__hasstar
    
    @hasstar.setter
    def hasstar(self, value):
        self.__hasstar = value

    @property
    def isfire(self):
        return self.__isfire
    
    @isfire.setter
    def isfire(self, value):
        self.__isfire = value
    
    @property
    def continuous_counter(self):
        return self.__continuous_counter
    
    @continuous_counter.setter
    def continuous_counter(self, value):
        self.__continuous_counter = value
    
    def draw(self, win):
        win.blit(self.image, self.rect)
    
    def __change_pixel(self, n, image):
        pixels = pygame.surfarray.pixels3d(image)
        if n == 0:
            pixels[..., [0, 1, 2]] = pixels[..., [1, 2, 0]]
        elif n== 1:
            pixels[..., [0, 1, 2]] = pixels[..., [2, 1, 0]]
        elif n == 2:
            pixels[..., [0, 1, 2]] = pixels[..., [0, 2, 1]]
    
    def __get_image(self):
        # Image for sitting
        if self.__issit and self.__isbig:
            imageidx = 14 if not self.__isfire else 15
            
        # Choose Mario image for walking animation
        elif self.__vx == 0:
            if not self.__isfire:
                imageidx = 0 if not self.__isbig else 6 
            else:
                imageidx = 10
        else:
            if not self.__isfire:
                imageidx = self.WALK_ANIME_IDX[self.__walkidx % 6] if not self.__isbig else self.WALK_ANIME_BIG_IDX[self.__walkidx % 6]
            else:
                imageidx = self.WALK_ANIME_FIRE_IDX[self.__walkidx % 6]
        # Choose the jump mario image
        if not self.__on_ground:
            if not self.__isfire:
                imageidx = 4 if not self.__isbig else 9
            else:
                imageidx = 13
            
        # Change the image direction if its direction is left
        return pygame.transform.flip(self.__imgs[imageidx], self.__isleft, False)

    def update(self):
        if self.__status == Status.DEAD:
            pass
        
        # Draw game start
        if self.__status == Status.OPENING:
            # Put the mario at the center of the game start window
            self.rect = pygame.Rect(130, 140, TILE_SIZE, TILE_SIZE)
            self.__game_start()
            return
        
        # Draw game over
        if self.__status == Status.GAMEOVER:
            self.__game_over()
            return
        
        # When timer is 0, game ends except game clear
        if self.__map.timer == 0 and not self.__status in [Status.GOAL, Status.CLEAR]:
            self.__status = Status.DEADING
            
        if self.__status == Status.DEADING:
            self.image = self.__imgs[3]
            self.__deading()
            self.rect = pygame.Rect(self.__map.get_drawx(self.__rawrect), self.__rawrect.y, self.__rawrect.width, self.__rawrect.height)
            return
        
        # Fall handling
        if self.__rawrect.y > H:
            self.__status = Status.DEAD
            
            # Decrement life stocks
            self.__map.decrement_life_stocks()
            return
        
        # Mario gets a mushroom
        if self.__status == Status.GROWING:            
            self.__growing()
            self.rect = pygame.Rect(self.__map.get_drawx(self.__rawrect), self.__rawrect.y, self.__rawrect.width, self.__rawrect.height)
            return
        
        # Mario becomes small
        if self.__status == Status.SHRINKING:
            self.__shrinking()
            self.image.set_alpha(128) 
            self.rect = pygame.Rect(self.__map.get_drawx(self.__rawrect), self.__rawrect.y, self.__rawrect.width, self.__rawrect.height)
            return
        
        # Warping
        if self.__status in (Status.ENTERING, Status.APPEARING):
            self.__warping(is_entering=True if self.__status == Status.ENTERING else False)
            self.rect = pygame.Rect(self.__map.get_drawx(self.__rawrect), self.__rawrect.y, self.__rawrect.width, self.__rawrect.height)
            return
        
        # Game is paused
        # "p" is pushed -> Mario status changes from NORMAL to PAUSE and vice versa
        if self.__status == Status.PAUSE:
            self.image = self.__get_image()
            self.rect = pygame.Rect(self.__map.get_drawx(self.__rawrect), self.__rawrect.y, self.__rawrect.width, self.__rawrect.height)
            return
            
        # Goal process
        if self.__status == Status.GOAL:
            # Goal animation does not end
            # if not self.__goal():
            self.image = self.__get_image()
            self.rect = pygame.Rect(self.__map.get_drawx(self.__rawrect), self.__rawrect.y, self.__rawrect.width, self.__rawrect.height)
            return
        
        else:
            # Mario movement processes except GOAL status
            # Get key status
            keys = pygame.key.get_pressed()
            
            # Not move when sitting
            if not keys[pygame.K_DOWN]:
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
            
            # If Mario sits or not
            if keys[pygame.K_DOWN]:
                if not self.__issit and self.__isbig:
                    self.__rawrect.height = 30
                    self.__issit = True
            else:
                if self.__issit and self.__isbig:
                    self.__rawrect.height = 40
                self.__issit = False

            # Dash with left shift
            self.__isdash = keys[pygame.K_LSHIFT]
            
            if self.__vx != 0:
                if (not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]) or keys[pygame.K_DOWN]:
                    self.__stop()
            
            # Warp
            self.warp(keys)
                        
            # Move for Y axle
            # if not self.__on_ground:
            self.__vy += 1
            self.__rawrect.y += self.__vy
                    
            # Judge hitbox
            if self.__map.chk_collision(self.__rawrect, is_mario=True):
                # If Mario is moving upward, it lets him go downward
                # vy is bigger than 0 -> 1 to go upward
                self.__rawrect.y = ((self.__rawrect.y // TILE_SIZE + (1 if self.__vy < 0 else 0)) * TILE_SIZE)
                
                # Adjustment when Mario is sitting
                self.__rawrect.y += SMALL_TILE_SIZE if self.__issit else 0
                
                if self.__vy > 0:
                    self.__on_ground = True
                    self.__vy = 0
                    
                    # Initialize continuous_counter
                    self.__continuous_counter = 0
                        
                else:
                    self.__vy = 1
            
            # End invisible state
            if self.__isinvisible:
                self.__invisiblecounter -= 1
                if self.__invisiblecounter == 0:
                    self.__isinvisible = False
                    # Change hasstar from True to False when star ends
                    if self.__hasstar:
                        self.__hasstar = False
                    # initialization
                    self.__invisiblecounter = 90
            
            # Get the image
            self.image = self.__get_image()
        
        if self.__isinvisible:
            # Blinking for a star mario
            if self.__hasstar:
                
                if self.__invisiblecounter < 60:
                    # Slowly blinking for the last 2 seconds
                    n = self.__invisiblecounter % 16 // 4
                else:
                    n = self.__invisiblecounter % 4
                self.__change_pixel(n, self.image)

            else:
                # Set invisible Mario
                self.image.set_alpha(128)
        else:
            self.image.set_alpha(255)
                
        # Update rect for Splite
        self.rect = pygame.Rect(self.__map.get_drawx(self.__rawrect), self.__rawrect.y, self.__rawrect.width, self.__rawrect.height)
            
    def move(self):
        self.__walkidx += 1
        
        # Prevent to move to the outside of the window
        if self.__rawrect.x < self.__map.nowx:
            self.__rawrect.x = self.__map.nowx
        
        # Collision check
        if self.__map.chk_collision(self.__rawrect):
            self.__rawrect.x = (self.__rawrect.x // TILE_SIZE + (1 if self.__isleft else 0)) * TILE_SIZE     
    
    def __right(self):
        if not self.__isdash:
            if self.__vx > self.MAX_SPEED_X:
                self.__vx -= self.ACC_SPEED_X
            else:
                self.__vx = (self.__vx + self.ACC_SPEED_X) if self.__vx < self.MAX_SPEED_X else self.MAX_SPEED_X
        else:
            # Dash
            self.__vx = (self.__vx + self.ACC_SPEED_X) if self.__vx < self.DASH_SPEED_X else self.DASH_SPEED_X
        
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
            self.__vx = (self.__vx - self.ACC_SPEED_X) if self.__vx > -1 *  self.DASH_SPEED_X else -1 * self.DASH_SPEED_X
        
        # Cancel law of inertia when changing the direction.
        if not self.__isleft:
            self.__vx = 0
        
        self.__rawrect.x += self.__vx
        self.__isleft = True
        self.move()
        
    def __jump(self):
        # If Mario is on ground, he can jump
        if self.__on_ground:
            if abs(self.__vx) == self.DASH_SPEED_X:
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
        
        # Prevent to move to the outside of the window
        if self.__rawrect.x < self.__map.nowx:
            self.__rawrect.x = self.__map.nowx
        
        # Collision check to prevent going into blocks by inertia 
        if self.__map.chk_collision(self.__rawrect):
            self.__rawrect.x = (self.__rawrect.x // TILE_SIZE + (1 if self.__isleft else 0)) * TILE_SIZE
    
    def __deading(self):
        if self.__animecounter == 0:
            self.__vy = -10
        
        if self.__animecounter > 10:
            self.__vy += 1
            self.__rawrect.y += self.__vy
        
        if self.__rawrect.y > H + TILE_SIZE:
            self.__status = Status.DEAD
            
            # Decrement life stocks
            self.__map.decrement_life_stocks()
            return
        self.__animecounter += 1
    
    def __growing(self):
        if self.__isfire:
            if self.__growcounter == 30:
                self.__status = Status.NORMAL
                self.__growcounter = 0
                return
            self.image = self.__get_image()
            self.__change_pixel(self.__growcounter % 8 //2, self.image)
            
        else:
            if self.__growcounter == 0:
                self.image = self.__imgs[6]
                self.__rawrect.y -= TILE_SIZE
            
            elif self.__growcounter == 6:
                self.image = self.__imgs[5]
                
            elif self.__growcounter == 8:
                self.image = self.__imgs[0]
                self.__rawrect.y += TILE_SIZE
                        
            elif self.__growcounter == 10:
                self.image = self.__imgs[6]
                self.__rawrect.y -= TILE_SIZE
                        
            elif self.__growcounter == 12:
                self.image = self.__imgs[5]
                
            elif self.__growcounter == 14:
                self.image = self.__imgs[0]
                self.__rawrect.y += TILE_SIZE
                        
            elif self.__growcounter == 16:
                self.image = self.__imgs[6]
                self.__rawrect.y -= TILE_SIZE
                
            elif self.__growcounter == 18:
                self.image = self.__imgs[5]

            elif self.__growcounter == 20:
                self.image = self.__imgs[6]
                self.__rawrect.y -= TILE_SIZE  # to offset +=10
                self.__rawrect.height = 40
                self.__isbig = True
                self.__status = Status.NORMAL
                # Initialize counter
                self.__growcounter = 0
                        
        self.__growcounter += 1
    
    def __shrinking(self):
        if self.__growcounter == 0:
            self.image = self.__imgs[0]
            self.__rawrect.y += TILE_SIZE
        
        elif self.__growcounter == 6:
            self.image = self.__imgs[5]
            
        elif self.__growcounter == 8:
            self.image = self.__imgs[6]
                     
        elif self.__growcounter == 10:
            self.image = self.__imgs[0]
                     
        elif self.__growcounter == 12:
            self.image = self.__imgs[5]
            
        elif self.__growcounter == 14:
            self.image = self.__imgs[6]
                     
        elif self.__growcounter == 16:
            self.image = self.__imgs[0]
            
        elif self.__growcounter == 18:
            self.image = self.__imgs[5]

        elif self.__growcounter == 20:
            self.image = self.__imgs[0]
            # self.__rawrect.y += 20  # to offset +=10
            self.__rawrect.height = TILE_SIZE
            self.__isbig = False
            self.__status = Status.NORMAL
            # Initialize counter
            self.__growcounter = 0
            
            self.__isinvisible = True
        self.__growcounter += 1
    
    def slide_down_pole(self):
        self.__rawrect.y += GOAL_FALL_SPEED
        if self.__rawrect.y > GOAL_BOTTOM_Y - (TILE_SIZE if self.__isbig else 0):
            self.__rawrect.y = GOAL_BOTTOM_Y - (TILE_SIZE if self.__isbig else 0)
    
    def change_side(self) -> None:
        self.__rawrect.x += 40
        self.__rawrect.y = 240 - (TILE_SIZE if self.__isbig else 0)

        # for walk animation
        self.__walkidx = 0
        self.__on_ground = True
        
    def walk_to_castle(self) -> None:
        self.__right()
    
    def enter_castle(self) -> None:
        # TODO: Mario doesn't become invisible if it's Fire Mario.
        self.__isinvisible = True
        self.__vx = 0
        
    def fire(self):
        """Create Fire objects, limiting only two objects."""
        firecount = 0
        for entity in self.__group.sprites():
            if isinstance(entity, Fire):
                firecount += 1
        
        if firecount == 2:
            return
        
        # Create and add Fire ojects
        fire = Fire(self.__rawrect.x, self.__rawrect.y + SMALL_TILE_SIZE, -5 if self.__isleft else 5, self, self.__map)
        self.__group.add(fire)
        self.__map.sound.play_sound_asnync(self.__map.sound.play_fire)
        
        # Add if a fireball hits enemies
        self._arrlies.append(fire)
    
    def warp(self, keys: pygame.key) -> None:
        """Proceed with the necessary processes for warp if the conditions are met."""

        # Get the current location
        xidx, yidx = self.__rawrect.x // TILE_SIZE, self.__rawrect.y // TILE_SIZE

        # Ensure about the warp location and key input
        if (xidx, yidx) in self.__map.warp_info:
            self.__next_data = self.__map.warp_info[(xidx, yidx)]
            # Make sure if the key input matches or not
            if self.__next_data[3] == 1 and keys[pygame.K_DOWN]:
                self.__status = Status.ENTERING
            if  self.__next_data[3] == 2 and keys[pygame.K_RIGHT]:
                self.__status = Status.ENTERING
            
    def __warping(self, is_entering: bool) -> None:
        """
        Deal with warping animation for both entering a pipe and appearing from a pipe.

        Args:
            is_entering (bool): True if it depict an animation of entering a pipe.
        """
        if self.__warpcounter == 10:
            self.__warpcounter = 0
            self.__vx = 0
            self.__vy = 0
            
            # Adjust x,y location when showing up from the pipe
            self.__rawrect.x = self.__next_data[1] * TILE_SIZE
            if not is_entering:
                self.__rawrect.y = (self.__next_data[2] * TILE_SIZE) - (TILE_SIZE if self.__isbig else 0)
                    
            self.__map.change_map(self.__next_data)
            if self.__status == Status.APPEARING:
                self.__status = Status.NORMAL
            else:
                self.__status = Status.APPEARING if self.__next_data[4] else Status.NORMAL
                
        else:
            idx = 3 if is_entering else 4
            # To down
            if self.__next_data[idx] == 1:
                self.__rawrect.y += 2
                
            # To right
            if self.__next_data[idx] == 2:
                self.__rawrect.x += 2
                self.__walkidx = 0

            # To up
            if self.__next_data[idx] == 3:
                self.__rawrect.y -= 2           

            self.__warpcounter += 1

    def __game_start(self) -> None:
        if self.__animecounter >= 60:
            self.__status = Status.NORMAL
            self.__animecounter = 0
            return
        
        self.__animecounter += 1
    
    def __game_over(self) -> None:
        if self.__animecounter >= 180:
           self.__animecounter = 0
           self.__status = Status.INIT
           return
        
        self.__animecounter += 1
        