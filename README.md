# 2048

This is a 2048 game implemented in Python with Pygame, featuring both human-playable and AI-driven modes. Additionally, an HTML/JavaScript-based AI version is provided.

## Features

### 🎮 Human Player Mode (Python/Pygame)

*   **How to Run**: Execute `2048(For humans).py` to start the game.
*   **Controls**: Use keyboard arrow keys (or WASD) or mouse drag to move tiles.
*   **Gameplay**: Classic 4x4 grid sliding tile game, the goal is to merge numbered tiles to reach 2048.
*   **Visual Effects**: Includes tile merging animations for an enhanced gaming experience.
*   **Score Tracking**: Automatically saves and loads the high score.

### 🤖 AI Player Mode (Python/Pygame)

*   **How to Run**: Execute `2048（AI player).py` to start the game.
*   **AI Algorithm**: Employs an Expectimax search algorithm-based AI, combining weighted board evaluation, empty cell bonuses, and smoothness penalties.
*   **Automatic Decisions**: The AI automatically chooses the best move direction based on the current board state.
*   **Save & Load**: Provides "Save" and "Load" buttons within the Pygame window, allowing players to save and load game progress. A prompt will appear at startup to choose between "Load" or "New Game."
*   **Tunable Parameters**: The AI's evaluation function and search depth can be configured within the `AIPlayer` class, including `WEIGHT_MATRIX` (tile position weights), `SAMPLE_LIMIT` (number of random spawns to sample), and `search_depth` (dynamically adjusted based on the number of empty cells).

### 🌐 AI Player Mode (HTML/JavaScript)

*   **How to Run**: Open the `2048_AI(fast than python).html` file in a web browser.
*   **AI Algorithm**: Also uses an Expectimax search algorithm-based AI with evaluation and search capabilities.
*   **Automatic Decisions**: The AI starts playing automatically after the page loads.
*   **Save & Load**: Provides "Save" and "Load" buttons, utilizing browser `localStorage` for saving and loading game progress.
*   **Animation Effects**: Supports tile merging animations.

### 🖼️ Pure Pygame GUI

*   **Standalone**: No external GUI libraries required; all interfaces are rendered via Pygame.
*   **Clean Design**: Clear interface layout, centered button text, and a game-over overlay.

## Requirements

*   Python 3.7+
*   Pygame (`pip install pygame`)

## Installation

```bash
git clone https://github.com/Piechicken/2048.git
cd 2048
pip install pygame
```

## Usage

### Human Player Mode (Python)

```bash
python "2048(For humans).py"
```

Use keyboard arrow keys or mouse drag to slide tiles.

### AI Player Mode (Python)

```bash
python "2048（AI player).py"
```

At launch, choose "Load" or "New Game." The AI will automatically make moves; watch it combine tiles!

Click "Save" to persist the current board, and "Load" to restore progress.

### AI Player Mode (HTML)

Open the `2048_AI(fast than python).html` file in your browser.

The AI will start playing automatically. You can use the "Save" and "Load" buttons on the page to save or restore game progress.

## Project Structure

```
2048/
├── 2048(For humans)             # Human-playable version (Python/Pygame)
├── 2048_AI(fast than python).html # Web-based AI, implemented with HTML/JavaScript
├── 2048（AI player).py          # AI-driven version (Python/Pygame), with save/load support
└── README.md                    # This file
```

## AI Details

### Evaluation Function

The AI's evaluation function considers the following aspects:

*   **Positional Weights**: Assigns different weights to tiles at various positions based on `WEIGHT_MATRIX`, encouraging larger numbered tiles to appear in corners or edges.
*   **Empty Cell Bonus**: Higher scores for more empty cells on the board, encouraging the AI to keep the board open.
*   **Smoothness Penalty**: Penalizes large numerical differences between adjacent tiles, encouraging the AI to maintain a smooth transition of tile values for easier merging.

### Search Algorithm

The AI employs an **Expectimax**-style search algorithm, which combines the Minimax algorithm with expected value calculations. This is suitable for games involving random factors (such as the spawning of new tiles).

*   **Search Depth**: Dynamically adjusts the search depth based on the number of empty cells on the board. A shallower search depth is used when there are more empty cells (e.g., depth 3 if more than 5 empty cells, otherwise depth 4) to balance computational complexity and decision quality.
*   **Sample Limit**: When the AI simulates new tile spawns, it performs random sampling based on the `SAMPLE_LIMIT` parameter to reduce computational load.

### Tunable Parameters

You can adjust the following parameters within the `AIPlayer` class to optimize the AI's behavior:

*   `self.WEIGHT_MATRIX`: Defines the weights for each position on the board, influencing the AI's preference for tile placement.
*   `self.SAMPLE_LIMIT`: Determines the number of random positions sampled by the AI when simulating new tile spawns.
*   `search_depth`: The search depth, affecting the AI's ability to predict future moves.

## License

MIT License © Piechicken

## Contributions

Feel free to open Issues or Pull Requests to improve gameplay, UI, or AI heuristics!


