# Scenarios for the measurements 
There are five cases to be covered for the measurements. 

1. Game initialization 
2. Normal game play 
3. Mario death reset (Mario._init_dead()) 
4. Transition from GameOver to Opening 
5. Game clear

## Scenario Descriptions
All steps heppen in one continuous session. The bullets in (case ...) show which measurement case you're exercising. 

### 1st scenario: 
1. Wait for 5 seconds after the initialization. (case 1 + 2)
2. Defeat first Goomba and then get a mushroom to be a big-mario (case 2)
3. Then mario is dead by falling out of the map  (case 2)
4. Then measure self._mario.init_dead(). (case 3)

### 2nd scenario: 
1. wait for 3 seconds after the reset (case 2)
2. defeat first Goomba and then get a mushroom to be a power mario (case 2)
3. Go to the sub area by tonel (case 2)
4. Go back to the main area and dead by Goomba. (case 2)
5. Then measure self._mario.init_dead(). (case 3)

### 3rd scenario: 
1. wait for 3 seconds after the reset (case 2)
2. defeat first Goomba and then get a mushroom to be a power mario (case 2)
3. Go and get a fire flower (case 2)
4. Defeat some enemies by fire balls (case 2) 
5. Do Koopa kick. (case 2) 
6. Get a star and defeat enemies (case 2) 
7. Dead by falling out of the map (case 2)
8. Then measure the transition from Mario.GAMEOVER to Mario.OPENING. (case 4)

### 4th scenario: 
1. Wait for 3 seconds after the  (case 2)
1. Normally play and get mushroom, fire flower and star and 1up-mushroom  (case 2)
2. Goal the game with 6 fireworks  (case 5)
