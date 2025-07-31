# 2048

A Python implementation of the 2048 game with two modes: human-playable and AI-driven, powered by Pygame.

## Features

- 🎮 **Human Mode**  
  - Run `2048(For humans).py` to play manually using keyboard or mouse.  
  - Classic 4×4 sliding-tile gameplay.

- 🤖 **AI Mode**  
  - Run `2048（AI player).py` to let an Expectimax-style AI solve the game.  
  - Automatically chooses moves based on weighted board evaluation, empty-cell bonus, and smoothness.

- 💾 **Save & Load**  
  - Built-in save/load support in AI mode: click **Save** or **Load** buttons in the Pygame window.  
  - On startup, AI mode asks **Load** vs. **New** game via a Pygame prompt.

- 🖼️ **Pure Pygame GUI**  
  - No external GUI libraries—everything runs in Pygame windows.  
  - Clean layout, centered button text, and game-over overlay.

## Requirements

- Python 3.7+  
- Pygame (`pip install pygame`)  

## Installation

```bash
git clone https://github.com/Piechicken/2048.git
cd 2048,,,

## Usage

Human Mode

python "2048(For humans).py"

Use arrow keys or mouse clicks to slide tiles.


AI Mode

python "2048（AI player).py"

On launch, choose Load or New game.

The AI will automatically make moves; watch it combine tiles!

Click Save to persist the current board, Load to restore.


Project Structure

2048/
├── 2048(For humans).py      # Manual‐play version
├── 2048（AI player).py      # AI‐driven version with save/load
└── README.md                # This file

AI Details

Evaluation Function

Positional weights, empty-cell bonus, smoothness penalty.


Search

Expectimax-style search with configurable sample limit and depth (3–4).



Tweak parameters in the AIPlayer class:

self.WEIGHT_MATRIX    # Tile position weights
self.SAMPLE_LIMIT     # How many random spawns to sample
search_depth = 3 or 4 # Based on empty cell count

License

MIT License © Piechicken


---

Feel free to open issues or PRs to improve gameplay, UI, or AI heuristics!
