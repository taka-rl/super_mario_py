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

## Future Improvements
- [ ] Complete implemetations for World 1-1
  - [x] Add images for the castle, goal pole and goal flag
  - [ ] Add animation for both Mario and the goal flag after goal
  - [ ] Add fireworks after goal
  - [ ] Sounds such as BGM, Star Mario, Crushing enemies
  - [ ] Background image such as clouds, mountains
  - [ ] Animation improvements for becoming small to big/becoming big to small
  - [ ] Pixel image improvements
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

## Bug Fixes
- [ ] Improve the transition from left to right at 120 rect in the window
- [ ] Only when Mario warps with the proper arrow input
- [ ] Mushroom jumps when Mario hits a block
- [ ] Big Mario defeats enemies while crushing blocks.
- [ ] Deleted fire balls kill enemies

## Future Developments
- [ ] Introduce Reinforcement learning
- [ ] Add different stages
