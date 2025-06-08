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
| space | jump |
| left shift | dash |
| left shift | fire |

### Images
Images are stored in [here](https://github.com/taka-rl/super_mario_py/tree/main/img).  
Images for this project were drawn by pixels, using the following web pages written.  

ドット絵ツール: https://neutralx0.net/tools/dot3/  
ゲームドット絵図鑑: https://pixel-art.tsurezure-brog.com/home/smb/  


### Maps
Currently, World 1-1 is implemented.  
Adding more worlds is a future plan.

## Get started
1. Clone this project: `git clone https://github.com/taka-rl/super_mario_py.git`

2. Run the following command to install libraries:  
On Windows type: `python -m pip install -r requirements.txt`
On MacOS type: `pip3 install -r requirements.txt`

3. Run `main.py`

## Future Development
- Complete implemetations for game
- Introduce Pytorch/TensorFlow/Ray RLlib for Reinforcement learning
- Add different stages
