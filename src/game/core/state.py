from enum import Enum, auto


class Status(Enum):
    NORMAL = auto()
    DEADING = auto()
    DEAD = auto()
    TREADING = auto()
    SLIDING = auto()
    FLYING = auto()
    GROWING = auto()
    SHRINKING = auto()
    ENTERING = auto()
    APPEARING = auto()
    GOAL = auto()
    CLEAR = auto()
    PAUSE = auto()
    INIT = auto()
    OPENING = auto()
    GAMEOVER = auto()


class GoalStatus(Enum):
    IDLE = auto()
    MARIO_FALL = auto()
    MARIO_TURN = auto()
    MARIO_WALK = auto()
    MARIO_ENTER_CASTLE = auto()
    SCORE_CALCULATION = auto()
    CASTLE_FLAG_RISE = auto()
    FIREWORKS = auto()
    DONE = auto()
    