# Super Mario style 2D game with Python and Pygame
This repository is a Super Mario style 2D game, using Python and Pygame. 

## Environment Description
### Display 
Width and Height are 320 and 270, respectively.
Pixel size is 20x20. 

### Key inputs
|Keys|Description|
| - | - |
| move | arrows |
| crouch | down arrow |
| space | jump |
| left shift | dash |
| left shift | fire ball |

### Images
Images are stored in [here](https://github.com/taka-rl/super_mario_py/tree/main/img).  
Images for this project were drawn by pixels, using the following web pages.  

- ドット絵ツール: https://neutralx0.net/tools/dot3/  
This web page is used to make pixel images. You can make any pixel images up to 50x50 sizes.

- ゲームドット絵図鑑: https://pixel-art.tsurezure-brog.com/home/smb/  
This web page is a reference to make pixel images for Super Mario characters and objects.

### Maps
Currently, World 1-1 is implemented.  
Adding more worlds is a future plan.

I built this [map creator](https://github.com/taka-rl/map_creator) as a support tool to generate a map data. 

## Get started
1. Clone this project: `git clone https://github.com/taka-rl/super_mario_py.git`

2. Run the following command to install libraries:  
On Windows type: `python -m pip install -r requirements.txt`
On MacOS type: `pip3 install -r requirements.txt`

3. Run `main.py`

## Deelopments
- [ ] Complete implemetations for World 1-1
  - [x] Environment settings for this porject
  - [x] Create the main loop for the game
  - [x] Implement Mario class and display it
  - [x] Let Mario move
  - [x] Implement Mario walking animation
  - [x] Let Mario jump
  - [x] Add Goomba class and display it
  - [x] Let Goomba move
  - [x] Implement Goomba walking animation
  - [x] Add collision check for Goomba
  - [x] Add Goomba death 
  - [x] Add Mario death
  - [x] Add Map class
  - [x] Draw a map
  - [x] Add a collision check for Mario on Y axle
  - [x] Add a collision check for Mario on X axle
  - [x] Add a collision check for Goomba on both X and Y axle
  - [x] Add scrolling
  - [x] Add law of inertia
  - [x] Add animation when Mario jumps
  - [x] Implement B Dash
  - [x] Add Koopa class
  - [x] Let Koopa move
  - [x] Add collision check for Koopa
  - [x] Add Koopa death 
  - [x] Add Koopa reborn
  - [x] Add Koopa kick
  - [x] Draw 1up mushroom, star, mushroom, block, ground block, question block, panel images
  - [x] Implement to push a block
  - [x] Change question block to panel
  - [x] Display mushroom
  - [x] Let mushroom move
  - [x] Add collision check for mushroom
  - [x] Draw Big Mario including walking and jump for animation
  - [x] Change Small Mario to Big Mario and its animation
  - [x] Add collision check for Big Mario
  - [x] Change Big Mario to Small Mario and its animation
  - [x] Implement to crush a block
  - [x] Add animation for crushed block
  - [x] Draw pipe and display it
  - [x] Implement World 1-1 main map data temporalily
  - [x] Change decimal to hex for the map data
  - [x] Set enemies and mushroom data in the map data
  - [x] Let enemies and mushroom show up through scrolling
  - [x] Implement not to scroll to the left side
  - [x] Implement Star class
  - [x] Let star move
  - [x] Add a collision check for star
  - [x] Add animation for star Mario
  - [x] Update a collision check for star Mario
  - [x] Draw fire flower, fire Mario images
  - [x] Add animation when changing to fire Mario
  - [x] Release fire balls
  - [x] Kill enemies with fire balls
  - [x] Add Coin class
  - [x] Set coin data in the map data
  - [x] Add animation when Mario gets a coin
  - [x] Implement Sound class
  - [x] Add sound when Mario gets a coin
  - [x] Add sound when Mario hits a mushroom block
  - [x] Add sound when powering up to big/fire Mario
  - [x] Implement Number class
  - [x] Display score when Mario gets a coin, mushroom, fire flower
  - [x] Add score counter when killing enemies continuously
  - [x] Display score when killing enemies with Koopa kick, fire balls, star Mario
  - [x] Add sound for fire balls
  - [x] Add 1 up mushroom and its sound
  - [x] Put star in normal block
  - [x] Draw sitting Mario image
  - [x] Implement sitting Mario
  - [x] Draw block and ground block for World 1-1 sub 
  - [x] Implement World 1-1 sub map data
  - [x] Implement World 1-1 sub map data
  - [x] Change 8bit to 16bit in the map data
  - [x] Draw pipe for World 1-1 sub map
  - [x] Change map from main to sub and vice versa
  - [x] Draw coin for World 1-1 sub map
  - [x] Implement StaticCoin class
  - [x] Add a collision check for coin in World 1-1 sub map
  - [x] Implement warp from main to sub and vice versa
  - [x] Add animation for warp
  - [x] Draw goal flag, goal pole and castle images
  - [x] Set goal flag, goal pole and castle in the map data
  - [x] Ensure the collsiion check with Mario is not for goal flag, goal pole and castle
  - [x] Add images for the castle, goal pole and goal flag
  - [x] Add animation that both Mario and the goal flag fall down to the bottom of the goal pole after goal
  - [x] Add animation that Mario walks and enters the castle
  - [ ] Draw Mario images for falling down to the goal pole
  - [ ] Implement Mario images when falling down to the goal pole
  - [ ] Add fireworks after goal
  - [ ] Add a pause bottom
- [ ] Complete the game window
  - [ ] Add map stage on the top of the window
  - [ ] Add coin on the top of the window
  - [ ] Add increase the number of the coin
  - [ ] Add score on the top of the window
  - [ ] Add increase the score
  - [ ] Add timer on the top of the window
  - [ ] Add code to decrese the timer
- [ ] Code improvements
  - [ ] Organize magic numbers
  - [ ] Optimize code
  - [ ] Divide code into several files

## Bug Fixes/Improvements
- [ ] Improve the transition from left to right at 120 rect in the window
- [ ] Only when Mario warps with the proper arrow input
- [ ] Mushroom jumps when Mario hits a block
- [ ] Big Mario defeats enemies while crushing blocks.
- [ ] Deleted fire balls kill enemies
- [ ] Small Mario isn't on the ground as soon as it shows up the pipe from the sub stage
- [ ] Change draw orders as Mario is covered by the goal flag
- [ ] Stop Mario when the goal flag reaches the bottom of the goal pole, if the goal flag is lower than Mario right after reaching the goal pole.
- [ ] Sounds such as BGM, Star Mario, Crushing enemies
- [ ] Background image such as clouds, mountains
- [ ] Animation improvements for becoming small to big/becoming big to small
- [ ] Pixel image improvements
- [ ] Delete score animation when Mario gets coins in the sub stage

## Future Developments
- [ ] Introduce Reinforcement learning
- [ ] Add different stages
