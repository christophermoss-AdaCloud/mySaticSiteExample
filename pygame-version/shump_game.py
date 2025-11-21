#!/usr/bin/env python3
"""
Unit 12: SHUMP - A Shoot 'Em Up Game
Python implementation using Pygame
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Game settings
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPAWN_RATE = 0.02


class Player(pygame.sprite.Sprite):
    """Player ship sprite"""
    
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        # Draw player ship (green rectangle with white triangle)
        pygame.draw.rect(self.image, GREEN, (0, 0, 50, 50))
        pygame.draw.polygon(self.image, WHITE, [(25, 0), (0, 50), (50, 50)])
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 30
        self.speed = PLAYER_SPEED
        
    def update(self):
        """Update player position based on key presses"""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
    
    def shoot(self):
        """Create a bullet"""
        return Bullet(self.rect.centerx, self.rect.top)


class Bullet(pygame.sprite.Sprite):
    """Bullet sprite"""
    
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = BULLET_SPEED
    
    def update(self):
        """Move bullet upward"""
        self.rect.y -= self.speed
        # Remove if off screen
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    """Enemy ship sprite"""
    
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 40)
        self.rect.y = -40
        self.speed = 2 + random.random() * 2
    
    def update(self):
        """Move enemy downward"""
        self.rect.y += self.speed
        # Remove if off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    """Main game class"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Unit 12: SHUMP - Shoot 'Em Up Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.reset_game()
    
    def reset_game(self):
        """Reset game state"""
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        self.player = Player()
        self.all_sprites.add(self.player)
        
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.paused = False
    
    def spawn_enemy(self):
        """Spawn a new enemy"""
        if random.random() < ENEMY_SPAWN_RATE:
            enemy = Enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
    
    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over and not self.paused:
                    bullet = self.player.shoot()
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)
                
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
        
        return True
    
    def update(self):
        """Update game state"""
        if self.game_over or self.paused:
            return
        
        # Update all sprites
        self.all_sprites.update()
        
        # Spawn enemies
        self.spawn_enemy()
        
        # Check bullet-enemy collisions
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        for hit in hits:
            self.score += 10
        
        # Check player-enemy collisions
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if hits:
            self.lives -= len(hits)
            if self.lives <= 0:
                self.game_over = True
    
    def draw(self):
        """Draw everything to the screen"""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw score and lives
        score_text = self.small_font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.small_font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))
        
        # Draw game over screen
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("GAME OVER", True, WHITE)
            score_text = self.small_font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.small_font.render("Press R to play again", True, WHITE)
            
            self.screen.blit(game_over_text, 
                           (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 - 60))
            self.screen.blit(score_text,
                           (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                            SCREEN_HEIGHT // 2))
            self.screen.blit(restart_text,
                           (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                            SCREEN_HEIGHT // 2 + 40))
        
        # Draw pause screen
        if self.paused and not self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.font.render("PAUSED", True, WHITE)
            resume_text = self.small_font.render("Press ESC to resume", True, WHITE)
            
            self.screen.blit(pause_text,
                           (SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
                            SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(resume_text,
                           (SCREEN_WIDTH // 2 - resume_text.get_width() // 2,
                            SCREEN_HEIGHT // 2 + 10))
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Cap the frame rate
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Main entry point"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
