# Unit 12: SHUMP - Python/Pygame Version

This is the Python implementation of the SHUMP game using Pygame with custom sprite graphics.

## Requirements

- Python 3.7 or higher
- Pygame 2.5.0 or higher

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

Or install pygame directly:
```bash
pip install pygame
```

## How to Run

Run the game with:
```bash
python shump_game.py
```

Or make it executable and run directly:
```bash
chmod +x shump_game.py
./shump_game.py
```

## Controls

- **Arrow Keys**: Move your ship
- **Space Bar**: Shoot
- **ESC**: Pause game
- **R**: Restart game (when game over)

## Game Features

- Player ship with 4-directional movement and custom sprite graphics
- Shoot laser bullets to destroy enemies
- Enemy ships spawn from the top with custom alien ship sprites
- Animated star field background
- Score tracking system
- Lives/health system (3 lives)
- Pause functionality
- Game over screen with restart option

## Graphics

The game includes custom sprite images in the `assets/` directory:
- `player.png` - Blue spaceship sprite for the player
- `enemy.png` - Red alien ship sprite for enemies
- `bullet.png` - Yellow laser bullet sprite
- `star.png` - White star for scrolling background

If the asset files are missing, the game will automatically fall back to simple colored shapes.

## Regenerating Sprites

To regenerate the sprite images, run:
```bash
python create_sprites.py
```

This will recreate all sprite images in the `assets/` directory.

## Objective

Destroy enemy ships and survive as long as possible to achieve the highest score!
