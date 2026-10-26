[README.md](https://github.com/user-attachments/files/33943618/README.md)
# Nemo Climb MVP

A small vertical platform-jumping prototype built with **pygame-ce**. It runs without art assets: the starter character, platforms, and background are drawn in code. Add image assets to `Assets/` later and connect them through `Source/asset_manager.py`.

## Run

1. Install Python 3.10 or newer.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Start the game with `python Main/main.py`.

## Controls

- **A/D** or **Left/Right arrows**: move
- **Hold Space** or **Up arrow**: jump and automatically jump again on landing
- **Esc**: pause or resume
- **R**: restart after game over
- **Q**: quit from pause or game over

The MVP includes input-triggered jumping, one-way platform collisions, an upward-following camera, endless platform generation with bounded reachable spacing, a current height score, and a game-over screen. Character selection, saved high scores, zone difficulty, background transitions, enemies, and hazards are planned for later development.
