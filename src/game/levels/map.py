from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from core.settings import TILE_X, TILE_Y
from core.state import Status
from levels.world1_1 import LEVEL as LEVEL_1_1
from entities.coin import Coin
from entities.goomba import Goomba
from entities.koopa import Koopa
from entities.mushroom import Mushroom
from entities.static_coin import StaticCoin
from entities.star import Star
from entities.goal_flag import GoalFlag
from entities.castle_flag import CastleFlag
from entities.broken_block import BrokenBlock

if TYPE_CHECKING:
    from systems.sound import Sound
    from systems.hud import HeadUpDisplay


class Map():
    # TODO: standardize these code: startx + TILE_X, startx + TILE_X + 1, xidx + 1

    NOMOVE_X = 120
    BLOCK_VY = 5
    BLOCK_GROUND = 1
    BLOCK_NORMAL = 2
    BLOCK_QUESTION = 3
    BLOCK_PANEL = 4
    BLOCK_STAIRS = 5
    PIPE_1 = 6
    PIPE_2 = 7
    PIPE_3 = 8
    PIPE_4 = 9
    BLOCK_INVISIBLE = 0x0A
    BLOCK_STAR = 0x0B

    PUSHED_BLOCKS = [BLOCK_NORMAL, BLOCK_QUESTION, BLOCK_INVISIBLE, BLOCK_STAR]
    
    # Sub stage
    PIPE_5 = 0x0C  # Top left
    PIPE_6 = 0x0D  # Top right
    PIPE_7 = 0x0E  # Bottom right
    PIPE_8 = 0x0F  # Bottom left

    CASTLE_1 = 0x80
    CASTLE_2 = 0x81
    CASTLE_3 = 0x82
    CASTLE_4 = 0x83
    CASTLE_5 = 0x84
    CASTLE_6 = 0x85

    GOAL_POLE_1 = 0x86
    GOAL_POLE_2 = 0x87  
    GOAL_FLAG = 0x88
    
    def __init__(self, group: pygame.sprite.Group, group_bg: pygame.sprite.Group, sound: Sound, hud: HeadUpDisplay, world: str) -> None:
        # Map index
        self.__map_idx: int = 0

        # Background color
        self.__bg_color = ((135, 206, 235), (0, 0, 0))

        # Warp infomation (xidx, yidx): (map_idx, xidx, yidx, direction to enter) 
        # direction(0: None, 1: down, 2: right, 3: top, 4: left) 
        self.__warp_info: dict = {
            0: {(59, 8): (1, 1, 1, 1, 0), (60, 8): (1, 1, 1, 1, 0), (59, 7): (1, 1, 1, 1, 0), (60, 7): (1, 1, 1, 1, 0)}, 
            1: {(12, 11): (0, 165, 10, 2, 3), (12, 10): (0, 165, 10, 2, 3)}
            }
                
        pipe_1, pipe_2 = pygame.image.load('./img/pipe_1.jpg'), pygame.image.load('./img/pipe_2.jpg')
        castle_2 = pygame.image.load('./img/castle_2.jpg')
        block_ground = pygame.image.load('./img/ground.jpg')
        self.__imgs: dict = {
            self.BLOCK_GROUND: (block_ground, pygame.image.load('./img/ground_sub.jpg')),
            self.BLOCK_NORMAL: (pygame.image.load('./img/block.jpg'), pygame.image.load('./img/block_sub.jpg')),
            self.BLOCK_QUESTION: pygame.image.load('./img/question_block.jpg'),
            self.BLOCK_PANEL: pygame.image.load('./img/panel.jpg'),
            self.PIPE_1: pipe_1,
            self.PIPE_2: pipe_2,
            self.PIPE_3: pygame.image.load('./img/pipe_3.jpg'),
            self.PIPE_4: pygame.image.load('./img/pipe_4.jpg'),
            self.BLOCK_STAIRS: pygame.image.load('./img/stairs_block.jpg'),
            self.BLOCK_STAR: pygame.image.load('./img/block.jpg'),
            self.PIPE_5: pygame.transform.rotate(pipe_1, 90),
            self.PIPE_6: pygame.transform.rotate(pipe_2, 90),
            self.PIPE_7: pygame.image.load('./img/pipe_5.jpg'),
            self.PIPE_8: pygame.image.load('./img/pipe_6.jpg'),
            self.CASTLE_1: pygame.image.load('./img/castle_1.jpg'),
            self.CASTLE_2: castle_2,
            self.CASTLE_3: pygame.transform.rotate(castle_2, 180),
            self.CASTLE_4: pygame.image.load('./img/castle_4.jpg'),
            self.CASTLE_5: pygame.image.load('./img/castle_5.jpg'),
            self.CASTLE_6: block_ground,
            self.GOAL_POLE_1: pygame.image.load('./img/goal_post_1.jpg'),
            self.GOAL_POLE_2: pygame.image.load('./img/goal_post_2.jpg'),
            }
        
        # Mario info
        self.__mario = None
        
        self.__goal_manager = None
        
        # Sprite groups
        self.__group = group
        self.__group_bg = group_bg
        
        # Set Sound class
        self.__sound = sound
        
        # Set HeadUpDisplay class
        self.__hud = hud
        self.__score: int = 0
        self.__coin: int = 0
        self.__world: str = world
        self.__goal_time: int = None
        self.__life_stocks: int = 3
        
        # Common initialization
        self.__common_init()
        
        # Draw entity 
        for xidx in range(TILE_X):
            self.__create_entity(xidx)

    def __common_init(self) -> None:
        # Define map
        self.__data = LEVEL_1_1.copy()
    
        # Map shifts relative to Mario's position
        self.__drawmargin: int = 0
        
        # X coordinate on the left edge of the map
        self.__nowx: int = 0
    
        # Array for pushed blocks
        self.__pushedblocks: dict = {}
        
        # Timer
        self.__timer: float = 400

    def init_dead(self) -> pygame.sprite:
        self.__common_init()
        self.__group, self.__group_bg = pygame.sprite.RenderUpdates(), pygame.sprite.RenderUpdates()
        return self.__group, self.__group_bg
    
    @property
    def mario(self):
        return self.__mario
    
    @mario.setter
    def mario(self, value):
        self.__mario = value
    
    @property
    def goal_manager(self):
        return self.__goal_manager
    
    @goal_manager.setter
    def goal_manager(self, value):
        self.__goal_manager = value
    
    @property
    def nowx(self):
        """Get X coordinate on the left edge of the map"""
        return self.__nowx
    
    @property
    def group(self):
        return self.__group
    
    @property
    def sound(self):
        return self.__sound
    
    @property
    def hud(self):
        return self.__hud
    
    @property
    def score(self):
        return self.__score
    
    @property
    def coin(self):
        return self.__coin
    
    @property
    def timer(self):
        return self.__timer
    
    @property
    def goal_time(self):
        return self.__goal_time
    
    @goal_time.setter
    def goal_time(self, value):
        self.__goal_time = value
    
    @property
    def warp_info(self):
        return self.__warp_info[self.__map_idx]

    def get_mapdata(self, x: int, y: int) -> int:
        """
        Get data from the lower 8 bit on the map, corresponding to x, y coordinate tile.
        
        The function returns only the lowest 8 bits of the tile's value, discarding any higher bits.
        0xFF is hexadecimal for decimal 255 (binary: 1111 1111).
        The bitwise AND with 0xFF is a common trick to extract just these bits.
        
        Args:
            x (int): X axle on the map data
            y (int): Y axle on the map data

        Returns:
            int: The lower 8 bit block data
        """
        return self.__data[self.__map_idx][y][x] & 0x00FF

    def is_goal_block(self, x: int, y: int) -> bool:
        """
        Check whether the tile at (x, y) tile is a goal-block obstacle (Goal pole or castle). 

        Obstacles related to the goal blocks are marked by the 0x0080 bit in the map data.
        This function determines collision avoidance when Mario interacts with the goal pole or castle.

        Args:
            x (int): X axle on the map data
            y (int): Y axle on the map data
        Returns:
            bool: True if the tile's data contains the goal-block (0x0080), False otherwise.
        """
        return self.__data[self.__map_idx][y][x] & 0x0080 != 0
    
    def set_mapdata(self, x: int, y: int, val: int) -> None:
        """
        Set data to the lower 8 bits on the map data
        
        self.__data[y][x] & 0xFF00:
            Clears the lower 8 bits using and of 0xFF00, keeping only the upper 8 bits

        val & 0x00FF:
            Extracting only the 8 bits of val, ensuring the data fits within one byte (0-255).

        Args:
            x (int): X axle on Map
            y (int): Y axle on Map
            val (int): object data such as block
        """
        self.__data[self.__map_idx][y][x] = (self.__data[self.__map_idx][y][x] & 0xFF00) | (val & 0x00FF)
        
    def get_upper(self, n):
        """Get the upper 8 bit by shifting 8 bits to the right"""
        return (n >> 8) & 0x00FF
    
    def get_entitydata(self, x, y):
        """Get entity data from the map data"""
        return self.get_upper(self.__data[self.__map_idx][y][x])
     
    def set_entitydata(self, x: int, y: int, val: int) -> None:
        """
        Set entity data to the upper 8 bits on the map data.
        
        self.__data[y][x] & 0x00FF:
            Keeps only the lower 8 bits of the tile, effectively clearing the upper 8 bits.
        
        val & 0xFF00:
            Keeps only the upper 8 bits of val, ensuring the function doesn't accidentally set any lowe bits.
        
        0x00FF: 0000000011111111
        0xFF00: 1111111100000000
        
        """
        self.__data[self.__map_idx][y][x] = (self.__data[self.__map_idx][y][x] & 0x00FF) | (val & 0xFF00)

    def __create_entity(self, xidx: int) -> None:
        """
        Create entity objects based on the map data.

        The function scans a vertical column of tiles at the specified x-index (xidx) across all y-indices (yidx).
        For each tile in that column, it checks the upper 8 bits of the tile's data to determine if an entity should be created.
        If an entity is created, the corresponding map data is cleared (set to 0) to prevent duplicate creation.
        
        Args:
            xidx (int): X axle on the map data
        """
        # Extract the upper 8 bits for the entire column at xidx
        entity_col = [self.get_upper(self.__data[self.__map_idx][yidx][xidx]) for yidx in range(TILE_X)]
        x = xidx * 20
        
        # Scan through each tile in the column
        for yidx, dte in enumerate(entity_col):
            if dte == 0:
                continue
            if dte == 1:
                self.__group.add(Goomba(x, yidx * 20, -2, self.__mario, self))
            elif dte == 2:
                self.__group.add(Koopa(x, yidx * 20, -2, self.__mario, self)) 
            elif dte == 3:  # Mushroom
                self.__group_bg.add(Mushroom(x, yidx * 20, 2, self.__mario, self, oneup=False))  
            elif dte == 4:  # Star
                self.__group_bg.add(Star(x, yidx * 20, 2, self.__mario, self))
            elif dte == 5:  # Coin
                self.__group_bg.add(Coin(x, yidx * 20, 2, self.__mario, self))  
            elif dte == 6:  # 1 UP mushroom
                self.__group_bg.add(Mushroom(x, yidx * 20, 2, self.__mario, self, oneup=True))
            elif dte == 7:  # Static Coin
                self.__group.add(StaticCoin(x, yidx * 20, 2, self.__mario, self))  
            elif dte == 8:  # Goal Flag
                self.__group.add(GoalFlag(x + 10, yidx * 20, 2, self.__mario, self))
            elif dte == 9:  # Castle Flag
                self.__group_bg.add(CastleFlag(x, yidx * 20, 2, self.__mario, self, self.__goal_manager))

            self.set_entitydata(xidx, yidx, 0)

    def draw(self, win: pygame.display, rect: pygame.rect) -> None:
        """
        Draw the visible area of the game map, entities, and HUD on the screen based on Mario's current position.

        This method determines which tiles and entities are visible in the current viewport by calculating the starting
        tile index and horizontal margin based on Mario's position. It handles map scrolling, entity creation, pushed block
        animation, and draws all visible map tiles, background entities, and foreground entities. It also draws the HUD and
        special overlays (game start, pause, game over) depending on Mario's status.

        Parameters:
            win (pygame.display): The Pygame display surface to draw the map and entities onto.
            rect (pygame.rect): The rectangle representing Mario's current position, used to determine the visible portion of the map.

        Returns:
            None
        """
        if self.__mario.status == Status.OPENING:
            self.__hud.draw_game_start(win, self.__world, self.__life_stocks)
        
        elif self.__mario.status == Status.GAMEOVER:
            self.__hud.draw_game_over(win)

        else:
            if self.__mario.status == Status.PAUSE:
                self.__hud.draw_pause(win)

            else:  # If not paused, decrement timer
                self.decrement_timer(self.__mario.status)
            
            margin = 0
        
            # Mario at the left
            if rect.x <= self.NOMOVE_X + self.__nowx:
                startx = self.__nowx // 20
                margin = self.__nowx % 20
            
            # Mario at the mostright
            elif rect.x >= (len(self.__data[self.__map_idx][0]) - 1 - (TILE_X - self.NOMOVE_X // 20)) * 20:
                startx = len(self.__data[self.__map_idx][0]) - TILE_X - 1
                margin = 0
                
            else:
                # Normal scrolling
                startx = rect.x // 20 - self.NOMOVE_X // 20
                margin = rect.x % 20

            # Horizontal offset in Mario's position
            self.__drawmargin = -startx * 20 -margin
            # Update X coordinate on the left edge of the map
            self.__nowx = startx * 20
            
            # Entities appear
            self.__create_entity(startx + TILE_X)

            # pushed block
            delkeys = []
            for key in self.__pushedblocks:
                blockydata = (self.__pushedblocks[key][0] + 1, self.__pushedblocks[key][1] + 1 + self.__pushedblocks[key][0] + 1)
                self.__pushedblocks[key] = blockydata
                if self.__pushedblocks[key][0] >= self.BLOCK_VY:
                    delkeys.append(key)
            for key in delkeys:
                del self.__pushedblocks[key]
            
            # Draw a map
            for y in range(TILE_Y):
                for x in range(startx, startx + TILE_X + 1):
                    map_num = self.get_mapdata(x, y)
                    if map_num > 0 and map_num != self.BLOCK_INVISIBLE:
                        ymargin = 0
                        if (y, x) in self.__pushedblocks:
                            ymargin = self.__pushedblocks[(y, x)][1]
                        win.blit(self.__get_img(map_num), ((x - startx) * 20 - margin, y * 20 + ymargin))

        
        # Draw Heads-up display
        self.__hud.draw(win, self.__score, self.__timer, self.__coin, self.__world)
        
    def fill(self, win: pygame.display) -> None:
        """Fill the background of the window with the color."""
        if self.__mario.status in [Status.OPENING, Status.GAMEOVER]:
            win.fill(self.__bg_color[1])
        else:
            win.fill(self.__bg_color[self.__map_idx])
    
    def __get_img(self, map_num: int) -> pygame.Surface:
        """Get an image"""
        img = self.__imgs[map_num]
        if isinstance(img, tuple):
            img = img[0 if self.__map_idx == 0 else 1]
        return img

    def chk_collision(self, rect: pygame.rect, is_mario: bool = False) -> tuple[int, int] | bool:
        """
        Check for collision between a given rectangular area (rect) and the tiles in the game map. 
        The function checks the 2x2(small Mario) or 2x3(big Mario) tiles surrounding the rectangle.
        If a collision is detected with a pushable block, the function handles the logic for pushing the block.
        If Mario collides with an invisible block, the function returns False to indicate no collision.
    
        Args:
            rect (pygame.rect): Targeted rect to be checked collision

        Returns:
            tuple: Return (x,y) coordinate to indicate a collision, otherwise it returns False
        """
    
        # Convert the top-left position of the rectangle to the corresponding tile indices
        xidx, yidx = rect.x // 20, rect.y // 20  
        
        # Check the 2x2 or 2x3 grid of tiles surrounding the rectangle's top-left corner
        for y in range(2 if rect.height == 20 else 3):
            # Get Mario's both side of rect
            hitleft, hitright = False, False
            blockrectL = pygame.Rect(xidx * 20, (yidx + y) * 20, 20, 20)
            blockrectR = pygame.Rect((xidx + 1) * 20, (yidx + y) * 20, 20, 20)
            
            # Prevent list index out of range
            if (yidx + y) >= len(self.__data[self.__map_idx]) or (xidx + 1) >= len(self.__data[self.__map_idx][0]):
                return
            
            # Collision check            
            if (self.get_mapdata(xidx, yidx + y) and 
                not self.is_goal_block(xidx, yidx + y) and rect.colliderect(blockrectL)):
                hitleft = True
            if (self.get_mapdata(xidx + 1, yidx + y) and 
                not self.is_goal_block(xidx + 1, yidx + y) and rect.colliderect(blockrectR)):
                hitright = True
            
            # Make sure which block is pushed considering the Mario location
            x = 0
            if hitleft and hitright:
                if rect.x < blockrectL.centerx:
                    blockrect = blockrectL
                else:
                    blockrect = blockrectR
                    x = 1
            elif hitleft:
                blockrect = blockrectL
            elif hitright:
                blockrect = blockrectR
                x = 1
            else:
                continue
                # If nothing collides, the function returns.

            if is_mario:
                map_id = self.get_mapdata(xidx + x, yidx + y)
                # Block is being pushed, and prevent jumping on the invisible block
                if (map_id in self.PUSHED_BLOCKS and rect.y > blockrect.y and self.__mario.vy < 0 and
                    rect.centery - blockrect.centery > 5):
                    
                    if abs(blockrect.centerx - rect.centerx) < 10:
                        # Crush a block
                        if map_id == self.BLOCK_NORMAL and self.__mario.isbig:
                            self.set_mapdata(xidx + x, yidx + y, 0)
                            
                            # Add animation for a crushed block
                            bx, by = (xidx + x) * 20, (yidx + y) * 20
                            self.__group.add(BrokenBlock(bx, by, 3, -5, self.__mario, self))
                            self.__group.add(BrokenBlock(bx, by, -3, -5, self.__mario, self))
                            self.__group.add(BrokenBlock(bx, by, 3, 5, self.__mario, self))
                            self.__group.add(BrokenBlock(bx, by, -3, 5, self.__mario, self))
                            
                        else:
                            self.__pushedblocks[(yidx + y, xidx + x)] = (-1 * self.BLOCK_VY, 0)
                    
                            # Change Question/Invisible 1Up/Normal Star blocks to Panel
                            if map_id in [self.BLOCK_QUESTION, self.BLOCK_INVISIBLE, self.BLOCK_STAR] :
                                self.set_mapdata(xidx + x, yidx + y, self.BLOCK_PANEL)
                
                elif map_id == self.BLOCK_INVISIBLE:
                    return False
                                
            return (yidx + y, xidx + x)
        return False

    def get_drawx(self, rect: pygame.rect) -> int:
        """X coordinate to draw Mario on the map"""
        # Mario at the left
        if rect.x < self.NOMOVE_X + self.__nowx:
            x = rect.x - self.__nowx
        
        # Mario at the mostright
        elif rect.x >= (len(self.__data[self.__map_idx][0]) - 1 - (TILE_X - self.NOMOVE_X // 20)) * 20:
            x = rect.x - (len(self.__data[self.__map_idx][0]) - 1 - (TILE_X - self.NOMOVE_X // 20)) * 20 + self.NOMOVE_X
        
        else:
            # Keep Mario at the center
            x = self.NOMOVE_X
        return x

    def get_drawxentity(self, rect: pygame.rect) -> int:
        """
        Calculate the correct X coordinate to draw entity on the screen based on the map's scrolling position.
        This function accounts for the scrolling margin and adjusts the entity's horizontal position accordingly.
        The position is calculated relative to the current map view, ensuring that enemies are drawn correctly 
        in the viewport and move with the map.

        Args:
            rect (pygame.rect): The rectangle representing the entity's current position on the map.

        Returns:
            int: The calculated x-coordinate where the entity should be drawn on the screen.
        
        """
        return rect.x + self.__drawmargin
    
    def ispushedblock(self, yx: tuple[int, int]) -> bool: 
        """Ensure if it's pushed or not."""
        return yx in self.__pushedblocks
    
    def change_map(self, next_mapdata) -> None:
        """
        Change the map with deleting entities and drawing entites.
        """
        from entities.mario import Mario

        map_idx, xidx = next_mapdata[:2]
        self.__map_idx = map_idx
        self.__nowx = xidx * 20 - self.NOMOVE_X

        if self.__nowx < 0:
            self.__nowx = 0
        
        # Mario at the right
        elif self.__nowx > (len(self.__data[self.__map_idx][0]) - 1 - (TILE_X - self.NOMOVE_X // 20)) * 20:
            self.__nowx = (len(self.__data[self.__map_idx][0]) - 1 - (TILE_X - self.NOMOVE_X // 20)) * 20

        # Delete entities
        for entity in self.__group.sprites():
            if not isinstance(entity, Mario):
                entity.status = Status.DEAD

        for entity in self.__group_bg.sprites():
            entity.status = Status.DEAD
        
        # Draw entity
        for xidx in range(self.__nowx // 20, self.__nowx // 20 + TILE_X):
            self.__create_entity(xidx)

    def add_score(self, value) -> None:
        """Add score"""
        self.__score += value
        
    def add_coin(self) -> None:
        """Increment a coin"""
        self.__coin += 1
    
    def decrement_timer(self, status: int) -> None:
        """Decrease timer"""
        if status != Status.GOAL:     
            # Decrease timer
            self.__timer -= 0.033
            if self.__timer <= 0:
                self.__timer = 0
    
    def add_timer_score(self) -> bool:
        """Add 100 score per a second at the goal."""
        if self.__timer > 0:
            self.add_score(100)
            self.__timer -= 1
            return False
        
        elif self.__timer <= 0:
            self.__timer = 0
            return True
    
    def decrement_life_stocks(self):
        """Decrement life stocks and change Mario status to GAMEOVER if the life stock becomes zero."""
        self.__life_stocks -= 1
        if self.__life_stocks == 0:
            # Change Mario status to GAMEOVER
            self.__mario.status = Status.GAMEOVER
    
    def increment_life_stocks(self) -> None:
        """Increment life stocks when it get a 1 up mushroom."""
        self.__life_stocks += 1
        