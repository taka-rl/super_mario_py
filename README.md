# Super Mario style 2D game


https://github.com/user-attachments/assets/a9a437cd-e64d-40d6-b692-2929143e825a


## Folder structure
    ├─ img                           # pixel images used by the game
    ├─ logs                          # mesurement csv files     
    ├─ src
    │  ├─ game                       # Python package root 
    │  │  ├─ entities                # All in-game actors (Sprite) 
    │  │  │  ├─ __init__.py
    │  │  │  ├─ entity.py            # Entity class
    │  │  │  ├─ mario.py             # Mario class
    │  │  │  ├─ mushroom.py          # Mushroom class
    │  │  │  ├─ koopa.py             # Koopa class 
    │  │  │  ├─ goomba.py            # Goomba class
    │  │  │  ├─ broken_block.py      # BrokenBlock class
    │  │  │  ├─ star.py              # Star class
    │  │  │  ├─ fire.py              # Fire class
    │  │  │  ├─ coin.py              # Coin class
    │  │  │  ├─ static_coin.py       # StaticCoin class
    │  │  │  ├─ goal_flag.py         # GoalFlag class
    │  │  │  └─ castle_flag.py       # CastleFlag class
    │  │  ├─ levels
    │  │  │  ├─ __init__.py
    │  │  │  ├─ map.py               # Map class
    │  │  │  ├─ goal_manager.py      # GoalManager class
    │  │  │  └─ world1_1.py          # World 1-1 map data
    │  │  ├─ systems                
    │  │  │  ├─ __init__.py 
    │  │  │  ├─ sound.py             # Sound class
    │  │  │  ├─ hud.py               # HeadUpDisplay class
    │  │  │  └─ number.py            # Number class
    │  │  ├─ core
    │  │  │  ├─ __init__.py
    │  │  │  ├─ state.py             # Status and GoalStatus classes
    │  │  │  └─ settings.py          # constants & tunables
    │  │  ├─ app.py                  # GameApp class
    │  │  ├─ main.py                 # Main game loop
    │  │  └─ __init__.py
    │  └─ tools                      # dev/diagnostic helpers (not core gameplay)
    │     ├─ __init__.py
    │     ├─ metrics.py              # PerfMonitor, NullMonitor, PerfCSVLogger, NullCSVLogger
    │     ├─ measure_app.py          # MeasureGameApp    
    │     └─ measurements
    │        ├─ __init__.py
    │        ├─ analysis             # Plotting and comparisons
    │        │  ├─ __init__.py
    │        │  ├─ compare_perf.py   # Result comparisons
    │        │  └─ plot_perf.py      # Plotting
    │        └─ scenarios            # Create inputs for the measurements
    │           ├─ __init__.py
    │           ├─ XXX.py            # InputRecorder, InputReplayer
    │           └─ XXX.py            # InputScript
    ├── .gitignore                             
    ├── README.md                    # Project documentation
    ├── pyproject.toml               # Config file
    └── requirements.txt             # Required dependencies


## Environment Description
### Display 
Width and Height are 320 and 270, respectively.
Pixel size is 20x20. 

### Key inputs
|Keys|Description|
|---------|-----------|
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

2. Install dependencies (choose one approach):
   - **Editable install with CLI entry points (recommended):**
     ```
     pip install -e .
     ```

   - **Plain requirements (no CLI commands):**
     ```
     python -m pip install -r requirements.txt
     ```
   *(Keep only one of these methods in the project long-term to avoid drift.)*

3. Run from source or via CLI:  
    - **From source (no install):**  
    ```
    python -m game.main
    python -m game.main --perf --perf-csv logs/perf.csv
    python -m tools.measurements.plot_perf logs/perf.csv --out logs/perf_plot.png
    ```
    - **After editable install:**  
    ```
    mario
    mario-perf --perf-csv logs/perf.csv
    perf-plot logs/perf.csv --out logs/plot.png
    ```    


## Future Developments
- [ ] Introduce Reinforcement learning
- [ ] Add different stages
- [ ] Fix bugs and improve this project
- [ ] Update import methods with Protocols, Registry/Factory
