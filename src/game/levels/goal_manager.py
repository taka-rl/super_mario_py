from __future__ import annotations
from typing import TYPE_CHECKING
from entities.fireworks import Fireworks
from core.state import Status, GoalStatus

if TYPE_CHECKING:
    from entities.mario import Mario
    from levels.map import Map


GOAL_ANIMATION_SCRIPTS: dict = {
    "World1-1": [
        {"phase": GoalStatus.MARIO_FALL,          "start": 0,  "end": 49},
        {"phase": GoalStatus.MARIO_TURN,          "start": 50, "end": 50},
        {"phase": GoalStatus.MARIO_WALK,          "start": 51, "end": 68},
        {"phase": GoalStatus.MARIO_ENTER_CASTLE,  "start": 69, "end": 70},
        {"phase": GoalStatus.SCORE_CALCULATION,   "start": 71, "end": 71},
        {"phase": GoalStatus.CASTLE_FLAG_RISE,    "start": 72, "end": 81},
        {"phase": GoalStatus.FIREWORKS,           "start": 82, "end": 118,},
        {"phase": GoalStatus.DONE,                "start": 119, "end": 119},
    ],
    # Other Worlds in the future
}


class GoalManager:
    # base location x=4120, y=100
    # TODO: Update the correct locations
    FIREWORKS_LOC: tuple= (
        (4100, 100),
        (4040, 140),
        (4160, 140),
        (4070, 160),
        (4130, 160),
        (4110, 100)
    )
    
    FIREWORKS_TIMING: tuple = (83, 88, 93, 98, 103, 108)
    
    # To make sure if there is a bug/ unnecessary process/code, variables and so on....
    # Add TODO for the future improvements
    # How about relocating the following consts in this GoalManager class?
    # GOAL_ANIMATION_SCRIPTS and GoalStatus
    
    def __init__(self, world_name: str, mario: Mario, map: Map) -> None:        
        self.__script: dict = GOAL_ANIMATION_SCRIPTS[world_name]
        self.__counter: int = 0
        self.__phase: int = GoalStatus.IDLE
        self.__isactive: bool = False
        
        self.__map = map
        self.__map.goal_manager = self
        
        self.__mario = mario
        self.__castle_flag = None
        self.__fireworks: list[Fireworks] = None
        self.__num_fireworks: int = 0
        
    @property
    def phase(self):
        return self.__phase
    
    @property
    def castle_flag(self):
        return self.__castle_flag
    
    @castle_flag.setter
    def castle_flag(self, value):
        self.__castle_flag = value
    
    @property
    def fireworks(self):
        return self.__fireworks
    
    @fireworks.setter
    def fireworks(self, value):
        self.__fireworks = value
    
    def update(self) -> None:
        
        if not self.__isactive:
            return
        
        if self.__phase == GoalStatus.MARIO_FALL:
            self.__mario.slide_down_pole()
                
        elif self.__phase == GoalStatus.MARIO_TURN:
            self.__mario.change_side()
        
        elif self.__phase == GoalStatus.MARIO_WALK:
            self.__mario.walk_to_castle()
        
        elif self.__phase == GoalStatus.MARIO_ENTER_CASTLE:
            self.__mario.enter_castle()
        
        elif self.__phase == GoalStatus.SCORE_CALCULATION:
            # Return until the calculation ends
            if not self.__map.add_timer_score():
                return
        
        elif self.__phase == GoalStatus.CASTLE_FLAG_RISE:
            self.__castle_flag.rise()
        
        elif self.__phase == GoalStatus.FIREWORKS:
            if self.__counter == 82:
                # Get the first digit of timer
                first_digit = int(str(self.__map.goal_time)[-1])
                
                # fireworks launches if the first digit of timer is 1 or 3 or 6
                if first_digit in [1, 3, 6]:
                    fireworks = [None] * first_digit
                    for i in range(0, first_digit):
                        fireworks[i] = Fireworks(self.FIREWORKS_LOC[i][0], self.FIREWORKS_LOC[i][1], 
                                                 0, self.__mario, self.__map, self)
                    self.__fireworks = fireworks
            else:
                # Fireworks lauch unless fireworks is none
                if self.__fireworks:
                    if self.__num_fireworks < len(self.__fireworks):
                        if self.__counter == self.FIREWORKS_TIMING[self.__num_fireworks]:
                            self.__map.group.add(self.__fireworks[self.__num_fireworks])
                            self.__map.add_score(500)
                            self.__num_fireworks += 1

        elif self.__phase == GoalStatus.DONE:
            self.__isactive = False
            self.__counter = 0
            
            # Change Mario status
            self.__mario.status = Status.CLEAR
            return
        
        self.__counter += 1
        self.__update_phase()
    
    def __update_phase(self) -> None:
        for phase_info in self.__script:
            if phase_info['start'] <= self.__counter <= phase_info['end']:
                self.__phase = phase_info['phase']
                return
            
    @property
    def isactive(self):
        return self.__isactive
    
    @isactive.setter
    def isactive(self, value):
        self.__isactive = value
