import pygame
from enum import Enum, auto
import time
import numpy as np
import threading
import platform


class Status(Enum):
    NORMAL = auto()
    DEADING = auto()
    DEAD = auto()
    TREADING = auto()
    SLIDING = auto()
    FLYING = auto()
    GROWING = auto()
    SHRINKING = auto()


# Display size
W, H = 320, 270

# Number of tiles
TILE_X, TILE_Y = 16, 14

# Array for socre
SCORE_ARRAY = [100, 200, 400, 500, 800, 1000, 2000, 4000, 8000, 9999]


class Map():
    NOMOVE_X = 120
    BLOCK_VY = 5
    
    BLOCK_WALL = 1
    BLOCK_NORMAL = 2
    BLOCK_QUESTION = 3
    BLOCK_PANEL = 4
    BLOCK_STAIRS = 5
    PIPE_1 = 6
    PIPE_2 = 7
    COIN = 8
    KINOKO = 9
    STAR = 10
    ONEUPKINOKO = 11
    PUSHED_BLOCKS = [BLOCK_NORMAL, BLOCK_QUESTION]
    
    def __init__(self, group, group_bg):      
        # Define map
        self.__data = [
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x53, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x00, 0x00, 0x00, 0x02, 0x02, 0x02, 0x53, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x33, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x02, 0x53, 0x53, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x05, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x05, 0x05, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x05, 0x05, 0x05, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x53, 0x00, 0x00, 0x00, 0x02, 0x33, 0x02, 0x53, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x33, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x43, 0x00, 0x00, 0x00, 0x00, 0x53, 0x00, 0x00, 0x53, 0x00, 0x00, 0x53, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x05, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x53, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x05, 0x00, 0x00, 0x05, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x05, 0x05, 0x00, 0x00, 0x05, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x02, 0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x05, 0x05, 0x00, 0x00, 0x05, 0x05, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x05, 0x05, 0x05, 0x00, 0x00, 0x05, 0x05, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06, 0x00, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x00, 0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x10, 0x00, 0x10, 0x00, 0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x10, 0x00, 0x00, 0x10, 0x00, 0x10, 0x00, 0x00, 0x00, 0x05, 0x05, 0x05, 0x05, 0x00, 0x00, 0x05, 0x05, 0x05, 0x05, 0x00, 0x00, 0x00, 0x00, 0x05, 0x05, 0x05, 0x05, 0x05, 0x00, 0x00, 0x05, 0x05, 0x05, 0x05, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x10, 0x00, 0x00, 0x06, 0x06, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x02, 0x02, 0x00, 0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],
            [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        ]
        
        self.__imgs: dict = {
            self.BLOCK_WALL: pygame.image.load('./img/ground.jpg'),
            self.BLOCK_NORMAL: pygame.image.load('./img/block.jpg'),
            self.BLOCK_QUESTION: pygame.image.load('./img/question_block.jpg'),
            self.BLOCK_PANEL: pygame.image.load('./img/panel.jpg'),
            self.COIN: pygame.image.load('./img/coin.jpg'),
            self.KINOKO: pygame.image.load('./img/kinoko.jpg'),
            self.STAR: pygame.image.load('./img/star.jpg'),
            self.ONEUPKINOKO: pygame.image.load('./img/1upkinoko.jpg'),
            self.PIPE_1: pygame.image.load('./img/pipe_1.jpg'),
            self.PIPE_2: pygame.image.load('./img/pipe_2.jpg'),
            self.BLOCK_STAIRS: pygame.image.load('./img/stairs_block.jpg'),
            }
        
        # Map shifts relative to Mario's position
        self.__drawmargin: int = 0
        
        # X coordinate on the left edge of the map
        self.__nowx: int = 0
    
        # Array for pushed blocks
        self.__pushedblocks: dict = {}
        
        # Mario info
        self.__mario = None
        
        # Sprite groups
        self.__group = group
        self.__group_bg = group_bg
    
    @property
    def mario(self):
        return self.__mario
    
    @mario.setter
    def mario(self, value):
        self.__mario = value
    
    @property
    def nowx(self):
        """Get X coordinate on the left edge of the map"""
        return self.__nowx
    
    @property
    def group(self):
        return self.__group
    
    def get_mapdata(self, x, y):
        """
        Get data from the lower 4 bit on the map, corresponding to x, y coordinate tile.
        
        The function returns only the lowest 4 bits of the tile's value, discarding any higher bits.
        0xF is hexadecimal for decimal 15 (binary: 0000 1111).
        The bitwise AND with 0xF is a common trick to extract just these bits.
        
        Args:
            x (int): X axle on the map data
            y (int): Y axle on the map data

        Returns:
            int or char: Specific data on the map data
        """
        return self.__data[y][x] & 0xF
    
    def set_mapdata(self, x: int, y: int, val):
        """
        Set data to the lower 4 bits on the map data
        
        self.__data[y][x] & ~0xF:
            Clears the lower 4 bits using bitwise NOT of 0xF, keeping only the upper 4 bits.

        val & 0xF:
            Extracting only the 4 bits of val, ensuring data is within 0-15.

        Args:
            x (int): X axle on Map
            y (int): Y axle on Map
            val (int or char): object data such as block
        """
        self.__data[y][x] = (self.__data[y][x] & ~0xF) | (val & 0xF)
        
    def get_upper(self, n):
        """Get the upper 4 bit by shifting 4 bits to the right"""
        return (n >> 4) & 0xF
    
    def get_enemydata(self, x, y):
        """Get enemy data from the map data"""
        return self.get_upper(self.__data[y][x])   
     
    def set_enemydata(self, x, y, val):
        """
        Set enemy data to the upper 4 bits on the map data.
        
        self.__data[y][x] & 0xF:
            Keeps only the lower 4 bits of the tile, effectively clearing the upper 4 bits.
        
        val & 0xF0:
            Keeps only the upper 4 bits of val, ensuring the function doesn't accidentally set any lowe bits.
        
        0xF: 00001111
        0xF0: 11110000
        
        """
        self.__data[y][x] = (self.__data[y][x] & 0xF) | (val & 0xF0)
    
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
        if rect.x <= self.NOMOVE_X + self.__nowx:
            startx = self.__nowx // 20
            margin = self.__nowx % 20
        else:
            startx = rect.x // 20 - self.NOMOVE_X // 20
            margin = rect.x % 20        
        # Horizontal offset in Mario's position
        self.__drawmargin = -startx * 20 -margin
        # Update X coordinate on the left edge of the map
        self.__nowx = startx * 20
        
        # Enemy apprers
        enemy_col = [self.get_upper(self.__data[yidx][startx + TILE_X + 1]) for yidx in range(16)]
        x = (startx + TILE_X + 1) * 20
        
        for yidx, dte in enumerate(enemy_col):
            if dte != 0:
                if dte == 1:
                    self.__group.add(Goomba(x, yidx * 20, -2, self.__mario, self))
                    self.set_enemydata(startx + TILE_X + 1, yidx, 0)

                if dte == 2:
                    self.__group.add(Koopa(x, yidx * 20, -2, self.__mario, self))
                    self.set_enemydata(startx + TILE_X + 1, yidx, 0)
                
                if dte == 3:
                    self.__group_bg.add(Mushroom(x, yidx * 20, 2, self.__mario, self))
                    self.set_enemydata(startx + TILE_X + 1, yidx, 0)
                
                if dte == 4:
                    # Star
                    self.__group_bg.add(Star(x, yidx * 20, 2, self.__mario, self))
                    self.set_enemydata(startx + TILE_X + 1, yidx, 0)

                if dte == 5:
                    # Coin
                    self.__group_bg.add(Coin(x, yidx * 20, 2, self.__mario, self))
                    self.set_enemydata(startx + TILE_X + 1, yidx, 0)
                
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
                if map_num > 0:
                    ymargin = 0
                    if (y, x) in self.__pushedblocks:
                        ymargin = self.__pushedblocks[(y, x)][1]
                    win.blit(self.__imgs[map_num], ((x - startx) * 20 - margin, y * 20 + ymargin))

    def chk_collision(self, rect: pygame.rect, is_mario: bool = False) -> bool:
        """
        Check for collision between a given rectangular area (rect) and the tiles in the game map. 
        The function checks the 2x2(small Mario) or 2x3(big Mario) tiles surrounding the rectangle.
    
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
            if (yidx + y) >= len(self.__data) or (xidx + 1) >= len(self.__data[0]):
                return
            
            # Collision check            
            if self.get_mapdata(xidx, yidx + y) and rect.colliderect(blockrectL):
                hitleft = True
            if self.get_mapdata(xidx + 1, yidx + y) and rect.colliderect(blockrectR):
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
                if map_id in self.PUSHED_BLOCKS and rect.y > blockrect.y: # Block is being pushed.
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
                    
                            # Change Question block to Panel
                            if map_id == self.BLOCK_QUESTION:
                                self.set_mapdata(xidx + x, yidx + y, self.BLOCK_PANEL)
            return (yidx + y, xidx + x)
        return None

    def get_drawx(self, rect: pygame.rect) -> int:
        """X coordinate to draw Mario on the map"""
        if rect.x < self.NOMOVE_X + self.__nowx:
            x = rect.x - self.__nowx
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
    
    def ispushedblock(self, yx): 
        """Ensure if it's pushed or not."""
        return yx in self.__pushedblocks


class Mario(pygame.sprite.Sprite):
    """Mario class"""
    
    WALK_ANIME_IDX = [0, 0, 1, 1, 2, 2]
    WALK_ANIME_BIG_IDX = [6, 6, 7, 7, 8, 8]
    WALK_ANIME_FIRE_IDX = [10, 10, 11, 11, 12, 12]
    MAX_SPEED_X: int = 5
    ACC_SPEED_X: float = 0.25
    DASH_SPPED_X: int = 8
    MAX_JUMP_Y = 7
    DASH_JUMP_Y = 10
    
    def __init__(self, map, group):
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
        
        # Star Mario
        self.__hasstar: bool = False
        
        # Fire Mario
        self.__isfire: bool = False
        
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
            ]
        
        self.image = self.__imgs[0]
        
        # The coordinate for map and the location of Mario are different.
        # Mario location coordinate        
        self.__rawrect = pygame.Rect(30, 220, 20, 20)
        # Mario coordinate for Map
        self.rect = self.__rawrect
        
        # Get a map
        self.__map: Map = map

        # Set Mario to Map
        self.__map.mario = self
        
        # Set a group for Sprite
        self.__group = group
    
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
    
    def __change_pixel(self, n, image):
        pixels = pygame.surfarray.pixels3d(image)
        if n == 0:
            pixels[..., [0, 1, 2]] = pixels[..., [1, 2, 0]]
        elif n== 1:
            pixels[..., [0, 1, 2]] = pixels[..., [2, 1, 0]]
        elif n == 2:
            pixels[..., [0, 1, 2]] = pixels[..., [0, 2, 1]]
    
    def __get_image(self):
        # Choose Mario image for walking animation
        if self.__vx == 0:
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
            
        if self.__status == Status.DEADING:
            self.image = self.__imgs[3]
            self.__deading()
            self.rect = pygame.Rect(self.__map.get_drawx(self.__rawrect), self.__rawrect.y, self.__rawrect.width, self.__rawrect.height)
            return
        
        # Fall handling
        if self.__rawrect.y > H:
            self.__status = Status.DEAD
        
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
        if self.__map.chk_collision(self.__rawrect, is_mario=True):
            # If Mario is moving upward, it lets him go downward
            # vy is bigger than 0 -> 1 to go upward
            self.__rawrect.y = (self.__rawrect.y // 20 + (1 if self.__vy < 0 else 0)) * 20
            
            if self.__vy > 0:
                self.__on_ground = True
                self.__vy = 0
                
                # Initialize continuous_counter
                self.__continuous_counter = 0
                    
            else:
                self._vy = 1
        
        # End invisible state
        if self.__isinvisible:
            self.__invisiblecounter -= 1
            if self.__invisiblecounter == 0:
                self.__isinvisible = False
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

            else:
                # Set invisible Mario
                self.image.set_alpha(128)
        else:
            self.image.set_alpha(256)
                
        # Update rect for Splite
        self.rect = pygame.Rect(self.__map.get_drawx(self.__rawrect), self.__rawrect.y, self.__rawrect.width, self.__rawrect.height)
        
    def move(self):
        self.__walkidx += 1
        
        # Prevent to move to the outside of the window
        if self.__rawrect.x < self.__map.nowx:
            self.__rawrect.x = self.__map.nowx
        
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
        
        # Prevent to move to the outside of the window
        if self.__rawrect.x < self.__map.nowx:
            self.__rawrect.x = self.__map.nowx
        
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
                self.__rawrect.y -= 20
            
            elif self.__growcounter == 6:
                self.image = self.__imgs[5]
                
            elif self.__growcounter == 8:
                self.image = self.__imgs[0]
                self.__rawrect.y += 20
                        
            elif self.__growcounter == 10:
                self.image = self.__imgs[6]
                self.__rawrect.y -= 20
                        
            elif self.__growcounter == 12:
                self.image = self.__imgs[5]
                
            elif self.__growcounter == 14:
                self.image = self.__imgs[0]
                self.__rawrect.y += 20
                        
            elif self.__growcounter == 16:
                self.image = self.__imgs[6]
                self.__rawrect.y -= 20
                
            elif self.__growcounter == 18:
                self.image = self.__imgs[5]
                self.__rawrect.y += 10

            elif self.__growcounter == 20:
                self.image = self.__imgs[6]
                self.__rawrect.y -= 10  # to offset +=10
                self.__rawrect.height = 40
                self.__isbig = True
                self.__status = Status.NORMAL
                # Initialize counter
                self.__growcounter = 0
                        
        self.__growcounter += 1
    
    def __shrinking(self):
        if self.__growcounter == 0:
            self.image = self.__imgs[0]
            self.__rawrect.y += 20
        
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
            self.__rawrect.height = 20
            self.__isbig = False
            self.__status = Status.NORMAL
            # Initialize counter
            self.__growcounter = 0
            
            self.__isinvisible = True
        self.__growcounter += 1
    
    def fire(self):
        """Create Fire objects, limiting only two objects."""
        firecount = 0
        for enemy in self.__group.sprites():
            if isinstance(enemy, Fire):
                firecount += 1
        
        if firecount == 2:
            return
        
        # Create and add Fire ojects
        fire = Fire(self.__rawrect.x, self.__rawrect.y + 10, -5 if self.__isleft else 5, self, self.__map)
        self.__group.add(fire)
        
        # Add if a fireball hits enemies
        self._arrlies.append(fire)

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
    
    @status.setter
    def status(self, value):
        self._status = value
    
    @property
    def rawrect(self):
        return self._rawrect
    
    @property
    def dir(self):
        return self._dir
        
    def kickHit(self) -> None:
        """
        Judge if Koopa kick hits or not. If it hits, the status is changed to FLYING.
        """
        # Koopa kick flying
        for marioarrly in self._mario.arrlies:
            if self._rawrect.colliderect(marioarrly.rawrect):
                self._status = Status.FLYING
                    
                # Decide the direction to fly
                self._dir = 3 if self._rawrect.centerx > marioarrly.rawrect.centerx else -3
                
                # Remove a fire ball
                if isinstance(marioarrly, Fire):
                    marioarrly.status = Status.DEADING
                    self._mario.arrlies.remove(marioarrly)
                
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
            # Display score
            self._map.group.add(Number(self.rect.x, self.rect.y, SCORE_ARRAY[self._mario.continuous_counter]))
            self._mario.continuous_counter += 1
        else:
            # If Mario is invisible, then return.
            if self._mario.isinvisible and not self._mario.hasstar:
                return
            
            if self._mario.hasstar:
                self._status = Status.FLYING
                return
            
            if self._mario.status != Status.TREADING:
                if self._mario.isbig:
                    self._mario.status = Status.SHRINKING
                    if self._mario.isfire:
                        self._mario.isfire = False
                else:
                    self._mario.status = Status.DEADING
            

class Mushroom(Enemy):    
    def __init__(self, x, y, dir, mario, map):
        self.__imgs = [
            pygame.image.load('./img/kinoko.jpg'),
            pygame.image.load('./img/fireflower.jpg')
            ]
        # self.image = self.__imgs[0]
        self._rawrect = pygame.Rect(x, y, 20, 20)
        
        self.__isflower: bool = False
        
        super().__init__(x, y, dir, mario, map)

        self.__sound = Sound()
    
    def update(self):
        # Not update if Mario is dead or growing or shrinking
        if self._mario.status in [Status.DEADING, Status.GROWING, Status.SHRINKING]:
            return
        
        # If Mario hit Mushroom box
        if self._status == Status.NORMAL:
            x, y = self._rawrect.x // 20, self._rawrect.y // 20
            if self._map.ispushedblock((y, x)):
                self.__sound.play_sound_asnync(self.__sound.play_item)
                self._status = Status.TREADING
                self._rawrect.y -= 5
                self.__isflower = self._mario.isbig 
        
        # Fall handling
        if self._rawrect.y > H:
            self._status = Status.DEAD
        
        # Mushroom is showing up
        elif self._status == Status.TREADING:
            self._walkidx += 1
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
                if not self._mario.isfire:                    
                    self._mario.status = Status.GROWING
                    self.__sound.play_sound_asnync(self.__sound.play_power)
                    if self.__isflower:
                        self._mario.isfire = True
                self._status = Status.DEAD
                self._map.group.add(Number(self.rect.x, self.rect.y, 1000))
                
        self.image = self.__imgs[0 if not self._mario.isbig else 1]
        self.rect = pygame.Rect(self._map.get_drawxenemy(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)
        

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
        # Not update if Mario is dead or growing or shrinking
        if self._mario.status in [Status.DEADING, Status.GROWING, Status.SHRINKING]:
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
                
                # Remove Koopa from Mario's arrlies list if reborn
                for _ in range(len(self._mario.arrlies)):
                    if self._rawrect in self._mario.arrlies:
                       self._mario.arrlies.remove(self._rawrect)

        # Flying if Koopa kick hits goomba
        if self._status == Status.FLYING:
            super().flying()
            # self._rect = self._map.get_drawxenemy(self._rawrect), self._rawrect.top
            self.image = pygame.transform.flip(self.__imgs[0], False, True)
        
        if self._status == Status.NORMAL:
            # Koopa kick flying
            super().kickHit()

        if self._status == Status.NORMAL or self._status == Status.SLIDING:
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
            if yx := self._map.chk_collision(self._rawrect):
                self._rawrect.y = (self._rawrect.y // 20 + (1 if self._vy < 0 else 0)) * 20
                # If a block is pushedW
                if self._map.ispushedblock(yx):
                    self._status = Status.FLYING
                    self._dir = 3 if self._rawrect.centerx > self._mario.rawrect.centerx else -3
                    self._vy = -8
                    
                    self.image = pygame.transform.flip(self.__imgs[0], False, True)
                    # Update rect for Splite
                    self.rect = pygame.Rect(self._map.get_drawxenemy(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)
                    return

                if self._vy > 0:
                    self._vy = 0
                else:
                    # jump
                    self._vy = 1

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
                    self._mario.arrlies.append(self)
                    
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
        # Not update if Mario is dead or growing or shrinking
        if self._mario.status in [Status.DEADING, Status.GROWING, Status.SHRINKING]:
            return

        # Fall handling
        if self._rawrect.y > H:
            self._status = Status.DEAD
        
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
            if yx := self._map.chk_collision(self._rawrect):
                self._rawrect.y = (self._rawrect.y // 20 + (1 if self._vy < 0 else 0)) * 20
                # If a block is pushedW
                if self._map.ispushedblock(yx):
                    self._status = Status.FLYING
                    self._dir = 3 if self._rawrect.centerx > self._mario.rawrect.centerx else -3
                    self._vy = -8
                    
                    self.image = pygame.transform.flip(self.__imgs[0], False, True)
                    # Update rect for Splite
                    self.rect = pygame.Rect(self._map.get_drawxenemy(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)
                    return
                
                if self._vy > 0:
                    self._vy = 0
                else:
                    # jump
                    self._vy = 1

            self._walkidx += 1
            if self._walkidx == self.WALK_SPEED:
                self._walkidx = 0
            
            self.image = pygame.transform.flip(self.__imgs[0], self._walkidx < self.WALK_SPEED // 2, False)
            
            # Collision check
            if self._rawrect.colliderect(self._mario.rawrect):
                super()._handle_mario_hit()
            
            # Koopa kick flying
            super().kickHit()
        
        # Update rect for Splite
        self.rect = pygame.Rect(self._map.get_drawxenemy(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)


class BrokenBlock(Enemy):
    def __init__(self, x, y, dir, vy, mario, map):
        self.__imgs: list = [pygame.image.load('./img/crushed_block.jpg')]
        self.image = self.__imgs[0]
        
        self._rawrect = pygame.Rect(x, y, 10, 10)
        super().__init__(x, y, dir, mario, map)
        self._vy = vy
        
    def update(self):
        super().flying()
        self.rect = pygame.Rect(self._map.get_drawxenemy(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)


class Star(Enemy):
    def __init__(self, x, y, dir, mario, map):
        self.__imgs: list = [pygame.image.load('./img/star.jpg')]
        self.image = self.__imgs[0]
        
        self._rawrect = pygame.Rect(x, y, 20, 20)
        super().__init__(x, y, dir, mario, map)
    
    def update(self):
        # Not update if Mario is dead or growing or shrinking
        if self._mario.status in [Status.DEADING, Status.GROWING, Status.SHRINKING]:
            return
        
        if self._status == Status.NORMAL:
            x, y = self._rawrect.x // 20, self._rawrect.y // 20
            
            if self._map.ispushedblock((y, x)):
                self._status = Status.TREADING
                self._rawrect.y -= 5
            self.image.set_alpha(0)
        elif self._status == Status.TREADING:
            self._walkidx += 1
            if self._walkidx == 4:
                self.image.set_alpha(256)
            if self._walkidx <= 15:
                self._rawrect.y -= 1
            if self._walkidx == 18:
                self._vy = -10
                self._status = Status.FLYING
        elif self._status == Status.FLYING:
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
                    self._vy = -10
                else:
                    # jump
                    self._vy = 0
        
            # Collision check with Mario
            if self._rawrect.colliderect(self._mario.rawrect):
                # Disappear star
                self._status = Status.DEAD
                
                # Prepare for a star mario
                self._mario.hasstar = True
                self._mario.isinvisible = True
                self._mario.invisiblecounter = 240  # 8 seconds
        
        self.rect = pygame.Rect(self._map.get_drawxenemy(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)


class Fire(Enemy):
    def __init__(self, x, y, dir, mario, map):
        self._imgs: list = [
            pygame.image.load('./img/fireball.jpg'),
            pygame.image.load('./img/explode.jpg'),
        ]
        self.image = self._imgs[0]
        
        self._rawrect = pygame.Rect(x, y, 10, 10)
        super().__init__(x, y, dir, mario, map)
    
    def update(self):
        # Not update if Mario is dead or growing or shrinking
        if self._mario.status in [Status.DEADING, Status.GROWING, Status.SHRINKING]:
            return
        
        if self._status == Status.NORMAL:
            # X axle move
            self._rawrect.x += self._dir
                    
            # X axle collision check
            if self._map.chk_collision(self._rawrect):
                self._status = Status.DEAD
                return
            
            # Disappear fire balls when hitting walls/pipes
            if self._rawrect.x < self._map.nowx or self._rawrect.x > self._map.nowx + W:
                self._status = Status.DEAD
                return
            
            # Disappear fire balls for fall handing
            if self._rawrect.y > H:
                self._status = Status.DEAD
                return

            # Y axle move
            self._vy += 1
            self._rawrect.y += self._vy
            
            # Y axle collision check
            if self._map.chk_collision(self._rawrect):
                self._rawrect.y = (self._rawrect.y // 20 + (1 if self._vy < 0 else 0)) * 20
                                    
                if self._vy > 0:
                    self._vy = -5
                else:
                    # jump
                    self._vy = 0
            
            # Add fire ball image animation here
            self.image = pygame.transform.rotate(self._imgs[0], (self._walkidx % 4) * 90)
            self._walkidx += 1
        elif self._status == Status.DEADING:
            # Change to explosion image
            if self._collapsecount < 4:
                self.image = self._imgs[1]
            else:
                self._status = Status.DEAD
                return
            
            self._collapsecount += 1
            
        self.rect = pygame.Rect(self._map.get_drawxenemy(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)


class Coin(Enemy):
    # ANIME_IDX = [0, 1, 2, 3]
    def __init__(self, x, y, dir, mario, map):
        self.__imgs: list = [
            pygame.image.load('./img/coin.jpg'),
        ]
        self.image = self.__imgs[0]
        
        self._rawrect = pygame.Rect(x, y, 20, 20)
        super().__init__(x, y, dir, mario, map)

        self.__sound = Sound()
    
    def update(self):
        # Not update if Mario is dead or growing or shrinking
        if self._mario.status in [Status.DEADING, Status.GROWING, Status.SHRINKING]:
            return
        
        if self._status == Status.NORMAL:
            x, y = self._rawrect.x // 20, self._rawrect.y // 20
            
            # Block with coins is pushed
            if self._map.ispushedblock((y, x)):
                self.__sound.play_sound_asnync(self.__sound.play_coin)
                self._status = Status.FLYING
                self._vy = -15
                self._rawrect.y -= 20
                return
            # Coin is invisible
            self.image.set_alpha(0)
        
        elif self._status == Status.FLYING:
            # Reset the invisible and coin appears
            self.image.set_alpha(256)
            self._vy += 2
            self._rawrect.y += self._vy
            if self._vy > 10:
                self._status = Status.DEAD
                self._map.group.add(Number(self.rect.x, self.rect.y, 200))
                return
            
            # Coin animation
            # self.image = self.__imgs[self.ANIME_IDX[self._walkidx]]
            # self._walkidx += 1
    
        self.rect = pygame.Rect(self._map.get_drawxenemy(self._rawrect), self._rawrect.y, self._rawrect.width, self._rawrect.height)


class Sound:

    FREQ_C = 261.63  # Sound for ド(C)
    FREQ_CS = 277.18
    FREQ_D = 293.66  # Sound for レ(D)
    FREQ_DS = 311.13
    FREQ_E = 329.63  # Sound for ミ(E)
    FREQ_F = 349.23  # Sound for ファ(F)
    FREQ_FS = 369.99
    FREQ_G = 392.00  # Sound for ソ(G)
    FREQ_GS = 415.30
    FREQ_A = 440.00  # Sound for ラ(A)
    FREQ_AS = 466.16
    FREQ_B = 493.88  # Sound for シ(B)

    def __init__(self):
        self.__sample_rate = 44100

        # Sound for coins
        self.__coin_durations = (0.1, 0.7)
        coin_frequencies = (self.FREQ_B * 2, self.FREQ_E * 4)
        coin_fades = (False, True)
        self.__coin_sounds = self._make_sound(coin_frequencies, self.__coin_durations, coin_fades)

        # Sound for mushrooms
        self.__item_durations = [0.04] * 8
        item_frequencies = (self.FREQ_C, self.FREQ_GS, self.FREQ_CS, self.FREQ_D, self.FREQ_AS, self.FREQ_DS, self.FREQ_AS)
        self.__item_sounds = self._make_sound(item_frequencies, self.__item_durations, [False] * 8)
        
        # Sound for power up
        power_frequencies = (
            self.FREQ_C * 2, self.FREQ_G, self.FREQ_C * 2, self.FREQ_E * 2, self.FREQ_G * 2, self.FREQ_C * 4,
            self.FREQ_G * 2, self.FREQ_GS, self.FREQ_C * 2, self.FREQ_DS * 2, self.FREQ_GS * 2, self.FREQ_E * 2,
            self.FREQ_A * 2, self.FREQ_C * 4, self.FREQ_DS * 4, self.FREQ_GS * 4, self.FREQ_DS * 4, self.FREQ_AS,
            self.FREQ_D * 2, self.FREQ_F * 2, self.FREQ_AS * 2, self.FREQ_F * 2, self.FREQ_B * 2, self.FREQ_D * 4, 
            self.FREQ_AS * 4, self.FREQ_D * 4
        )
        self.__power_durations = [0.05] * len(power_frequencies)
        self.__power_sounds = self._make_sound(power_frequencies, self.__power_durations, [False] * len(self.__power_durations))
        
        # Sound for Clear game
        self.__clear_durations = [0.2] * len(power_frequencies)
        self.__clear_sounds = self._make_sound(power_frequencies, self.__clear_durations, [False] * len(self.__power_durations))
        
    def _make_square_sound(self, frequency, duration, fadeout=False):
        """Generate a sawtooth sound"""
        t = np.linspace(0, duration, int(self.__sample_rate * duration), endpoint=False)
        
        # Create a wave
        waveform = 0.125 * np.sign(np.sin(2 * np.pi * frequency * t))

        if fadeout:
            waveform *= np.exp(-5 * t)
        
        if platform.system() == 'Windows':
            # For windows
            mono = (waveform * 32767).astype(np.int16)
            stereo = np.column_stack((mono, mono))  # duplicate to L/R channels
            return pygame.sndarray.make_sound(stereo)
        else:
            # For mac
            return pygame.sndarray.make_sound(((waveform * 32767)).astype(np.int16))
    
    def _make_sound(self, freqs, durs, fades):
        return [self._make_square_sound(freq, dur, fade) for freq, dur, fade in zip(freqs, durs, fades)]
    
    def play_sound_asnync(self, func):
        threading.Thread(target=func).start()

    def play_sounds(self, sounds, durations):
         for sound, dur in zip(sounds, durations):
            sound.play()
            pygame.time.wait(int(dur * 1000))       

    def play_coin(self):
        self.play_sounds(self.__coin_sounds, self.__coin_durations)
    
    def play_item(self):
        self.play_sounds(self.__item_sounds, self.__item_durations)
        
    def play_power(self):
        self.play_sounds(self.__power_sounds, self.__power_durations)
    
    def play_clear(self):
        self.play_sounds(self.__clear_sounds, self.__clear_durations)


class Number(pygame.sprite.Sprite):   
    def __init__(self, x, y, score):
        pygame.sprite.Sprite.__init__(self)
        
        font_size: int = 14
        self.__font = pygame.font.SysFont("Arial", font_size)
        self.image: pygame.Surface = self.__create_surface(score)
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.__counter: int = 0
        self.__status = Status.NORMAL
    
    @property
    def status(self):
        return self.__status
        
    def __create_surface(self, score):
        """Generate a surface for score"""
        text_surface = self.__font.render(str(score), True, (255, 255, 255))
        surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)        
        surface.blit(text_surface, (0, 0))
        return surface

    def update(self):
        # Move up
        self.rect.y -= 1        
        # Disappear after 1 second
        if self.__counter == 30:
            self.__status = Status.DEAD   
        self.__counter += 1     
    

def init():
     # Define Sprite group
    group = pygame.sprite.RenderUpdates()
    group_bg = pygame.sprite.RenderUpdates()
    
    # Map class
    map = Map(group, group_bg)
    
    # Mario class
    mario = Mario(map, group)
        
    # Add mario into the group
    group.add(mario)
    
    return group, group_bg, mario, map


def main():
    """main function"""
    
    # Initialize pygame
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=1)
    pygame.init()
    
    # Build a display
    win = pygame.display.set_mode((W, H))
    
    # Create clock rate
    clock = pygame.time.Clock()
    
    # Initialize sprite
    group, group_bg, mario, map = init()
    
    # Event loop
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            
            # Release fire balls
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LSHIFT and mario.isfire:
                    mario.fire()

        # Fill in the background     
        win.fill((135, 206, 235))
        
        # Update the group_bg
        group_bg.update()
        
        # Update the group
        group.update()
        
        # If Mario is dead
        if mario.status == Status.DEAD:
            time.sleep(2)
            group, group_bg, mario, map = init()
            continue 
        
        # Remove DEAD status
        for enemy in group.sprites():
            if enemy.status == Status.DEAD:
                group.remove(enemy)
        
        for enemy_bg in group_bg.sprites():
            if enemy_bg.status == Status.DEAD:
                group_bg.remove(enemy_bg)

        # Draw the group_bg
        group_bg.draw(win)
             
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
    