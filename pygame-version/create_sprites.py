#!/usr/bin/env python3
"""
Generate sprite images for the SHUMP game
"""

import pygame
import os

# Initialize Pygame
pygame.init()

# Create assets directory if it doesn't exist
os.makedirs('assets', exist_ok=True)

# Player ship sprite (spaceship)
def create_player_sprite():
    surface = pygame.Surface((50, 50), pygame.SRCALPHA)
    
    # Main body (blue-green spaceship)
    pygame.draw.polygon(surface, (0, 200, 255), [
        (25, 5),   # top point
        (15, 20),  # left wing top
        (5, 45),   # left wing bottom
        (20, 45),  # left body bottom
        (20, 35),  # left body middle
        (25, 30),  # center bottom
        (30, 35),  # right body middle
        (30, 45),  # right body bottom
        (45, 45),  # right wing bottom
        (35, 20),  # right wing top
    ])
    
    # Cockpit
    pygame.draw.circle(surface, (100, 255, 255), (25, 20), 6)
    
    # Engine glow
    pygame.draw.circle(surface, (255, 100, 0), (20, 40), 3)
    pygame.draw.circle(surface, (255, 100, 0), (30, 40), 3)
    
    # Outline for definition
    pygame.draw.polygon(surface, (0, 150, 200), [
        (25, 5), (15, 20), (5, 45), (20, 45), (20, 35),
        (25, 30), (30, 35), (30, 45), (45, 45), (35, 20)
    ], 2)
    
    pygame.image.save(surface, 'assets/player.png')
    print("Created player.png")

# Enemy ship sprite (alien ship)
def create_enemy_sprite():
    surface = pygame.Surface((40, 40), pygame.SRCALPHA)
    
    # Main body (red alien ship)
    pygame.draw.ellipse(surface, (255, 50, 50), (5, 10, 30, 20))
    
    # Wings
    pygame.draw.polygon(surface, (200, 0, 0), [
        (5, 15), (0, 10), (0, 25), (5, 25)
    ])
    pygame.draw.polygon(surface, (200, 0, 0), [
        (35, 15), (40, 10), (40, 25), (35, 25)
    ])
    
    # Cockpit/window
    pygame.draw.circle(surface, (100, 0, 0), (20, 20), 5)
    
    # Details
    pygame.draw.line(surface, (150, 0, 0), (10, 20), (30, 20), 2)
    
    pygame.image.save(surface, 'assets/enemy.png')
    print("Created enemy.png")

# Bullet sprite (laser)
def create_bullet_sprite():
    surface = pygame.Surface((6, 20), pygame.SRCALPHA)
    
    # Gradient laser effect
    for i in range(20):
        alpha = int(255 * (1 - i / 20))
        color = (255, 255 - i * 5, 0, alpha)
        pygame.draw.line(surface, color, (3, i), (3, i), 2)
    
    # Core
    pygame.draw.rect(surface, (255, 255, 255), (2, 5, 2, 10))
    
    pygame.image.save(surface, 'assets/bullet.png')
    print("Created bullet.png")

# Background/star sprite
def create_star_sprite():
    surface = pygame.Surface((2, 2), pygame.SRCALPHA)
    surface.fill((255, 255, 255))
    pygame.image.save(surface, 'assets/star.png')
    print("Created star.png")

# Explosion sprite (simple)
def create_explosion_sprite():
    surface = pygame.Surface((50, 50), pygame.SRCALPHA)
    
    # Multiple circles for explosion effect
    pygame.draw.circle(surface, (255, 200, 0), (25, 25), 20)
    pygame.draw.circle(surface, (255, 100, 0), (25, 25), 15)
    pygame.draw.circle(surface, (255, 50, 0), (25, 25), 10)
    pygame.draw.circle(surface, (255, 255, 0), (25, 25), 5)
    
    pygame.image.save(surface, 'assets/explosion.png')
    print("Created explosion.png")

if __name__ == "__main__":
    create_player_sprite()
    create_enemy_sprite()
    create_bullet_sprite()
    create_star_sprite()
    create_explosion_sprite()
    print("\nAll sprites created successfully in assets/ directory!")
    pygame.quit()
