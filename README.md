# Super Mario style 2D game
## Motivation
I wanted to challege creating a game like Super Mario and deepen the understanding of Object Oriented Programming skills and knowledge and Python through this complicated development used multiple objects.


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
| pause | p |

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

## Future Developments
- [ ] Fix bugs and improve this project
- [ ] Introduce Reinforcement learning
- [ ] Add different stages
