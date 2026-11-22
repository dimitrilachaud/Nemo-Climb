[README.md](https://github.com/user-attachments/files/35224317/README.md)
# Nemo Climb

A vertical platform-jumping game built with **pygame-ce**. The checkpoint 2 systems are implemented with the art currently in `Assets/`; missing or unreadable art falls back to drawn game elements.

## Run

1. Install Python 3.10 or newer.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Start the game with `python Main/main.py`.

## Controls

- **Left/Right arrows** or **A/D**: move
- **Hold Space** or **Up arrow**: jump, and keep jumping when you land
- **Esc**: pause or resume
- **R**: return to character selection from pause or game over
- **Q**: quit from character selection, gameplay, pause, or game over
- **Enter** or **Space**: start with the selected character
- **Developer cheat:** type **F-L-Y** during gameplay to toggle flight; use **W/S** or **Up/Down** for vertical movement and **A/D** or **Left/Right** horizontally

The camera continues to climb slowly even while the player is idle. Stay in view and keep climbing.
Flight bypasses gravity and platform landings for quick level traversal. Enemy and hazard collisions and camera bounds remain active.
After character selection, the game shows its rescue message and `background_intro.png`, then scrolls downward through the night, rocky, cloud, and forest backgrounds before starting the run.

## Checkpoint 2 features

- Character selection loads `character_<name>.png` sprite sheets from `Assets/`. Sheets use four columns and five rows: idle, walk, jump, hurt, and power-up.
- Jumping uses gravity, one-way platform collisions, and an upward-scrolling camera. Moving platforms carry the player while they stand on them.
- Platforms generate continuously. Their spacing stays within the player's jump reach, while platform size, gaps, and moving-platform frequency change with height.
- Flying enemies travel horizontally at a constant speed, independent of player position. Spikes and energy-orb hazards can appear near platform edges; platforms keep a clear central landing strip, and generated spacing accounts for that safe strip. Touching an enemy or hazard ends the run unless temporary immunity is active; moving fully outside the camera view always ends the run.
- Heart, boot, and snowflake pickups appear along the platform route. Each lasts five seconds: hearts grant immunity, boots allow one extra midair jump on every jump cycle while active, and snowflakes freeze moving platforms. Active powers show their icon and timer at the top right.
- Height zones increase difficulty and cross-fade between matching `background_<zone>.png` images.
- After the final zone begins at 6,000 height, each additional 2,000 height units raises the endless difficulty tier: more platforms move, they move faster, platforms shrink within a safe size limit, and enemy spawn rates rise. The final zone background remains in use.
- The score increases the first time each platform is reached. The best score persists in `data/high_score.json`.
- Character selection, gameplay, pause, and game-over screens are managed as separate game states. Restart returns to character selection.

The asset loader accepts the existing double-extension PNG names as well as standard `.png` names. Backgrounds are scaled to the game window. Character sheets are divided proportionally into a 4-by-5 grid, so a different source resolution can be used as long as the sheet keeps that layout.
