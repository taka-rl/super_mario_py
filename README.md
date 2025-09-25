# Super Mario style 2D game


https://github.com/user-attachments/assets/a9a437cd-e64d-40d6-b692-2929143e825a


## Folder structure



    ├─ img                           # pixel images for the project
    ├─ src
    │  └─ game                       # Python package root 
    │     ├─ entities                # All in-game actors (Sprite) 
    │     │  ├─ __init__.py
    │     │  ├─ entity.py            # Entity class
    │     │  ├─ mario.py             # Mario class
    │     │  ├─ mushroom.py          # Mushroom class
    │     │  ├─ koopa.py             # Koopa class 
    │     │  ├─ goomba.py            # Goomba class
    │     │  ├─ broken_block.py      # BrokenBlock class
    │     │  ├─ star.py              # Star class
    │     │  ├─ fire.py              # Fire class
    │     │  ├─ coin.py              # Coin class
    │     │  ├─ static_coin.py       # StaticCoin class
    │     │  ├─ goal_flag.py         # GoalFlag class
    │     │  └─ castle_flag.py       # CastleFlag class
    │     ├─ levels
    │     │  ├─ __init__.py
    │     │  ├─ map.py               # Map class
    │     │  ├─ goal_manager.py      # GoalManager class
    │     │  └─ world1_1.py          # World 1-1 map data
    │     ├─ systems                
    │     │  ├─ __init__.py 
    │     │  ├─ sound.py             # Sound class
    │     │  ├─ hud.py               # HeadUpDisplay class
    │     │  └─ number.py            # Number class
    │     ├─ core
    │     │  ├─ __init__.py
    │     │  ├─ state.py             # Status and GoalStatus classes
    │     │  └─ settings.py          # constants & tunables
    │     ├─ main.py                 # Main game loop
    │     └─ __init__.py
    ├── .gitignore                             
    ├── README.md                    # Project documentation
    └── requirements.txt             # Required dependencies


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
- [ ] Introduce Reinforcement learning
- [ ] Add different stages
- [ ] Fix bugs and improve this project
- [ ] Update import methods with Protocols, Registry/Factory
