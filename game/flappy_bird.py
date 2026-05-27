import pygame
import random
from .bird import Bird
from .pipe import PipeSystem
from .score_manager import ScoreManager
from dsa.challenges import DSAChallengeSystem
from utils.constants import *

class FlappyBirdGame:
    def __init__(self, screen, mode="human"):
        self.screen = screen
        self.mode = mode
        self.reset_game()
        
        if mode == "dsa_challenge":
            self.dsa_system = DSAChallengeSystem(self.screen)
        
    def reset_game(self):
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = PipeSystem()
        self.score_manager = ScoreManager()
        self.game_over = False
        self.paused = False
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.game_over:
                if not self.paused:
                    self.bird.jump()
                else:
                    self.paused = False
            elif event.key == pygame.K_p:
                self.paused = not self.paused
            elif event.key == pygame.K_r:
                self.reset_game()
                
        if self.mode == "dsa_challenge" and hasattr(self, 'dsa_system'):
            self.dsa_system.handle_event(event)
    
    def update(self):
        if self.paused or self.game_over:
            return
            
        # Update bird
        self.bird.update()
        
        # Update pipes
        self.pipes.update()
        
        # Check collisions
        if self.pipes.check_collision(self.bird) or self.bird.y > SCREEN_HEIGHT or self.bird.y < 0:
            self.game_over = True
            
        # Check scoring
        if self.pipes.check_scoring(self.bird):
            self.score_manager.increment_score()
            
            # Trigger DSA challenge
            if self.mode == "dsa_challenge" and self.score_manager.score % CHALLENGE_FREQUENCY == 0:
                self.paused = True
                self.dsa_system.trigger_challenge()
        
        # Update DSA system
        if self.mode == "dsa_challenge" and hasattr(self, 'dsa_system'):
            self.dsa_system.update()
            if self.dsa_system.challenge_completed:
                self.paused = False
                self.dsa_system.challenge_completed = False
    
    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw pipes
        self.pipes.draw(self.screen)
        
        # Draw bird
        self.bird.draw(self.screen)
        
        # Draw score
        self.score_manager.draw(self.screen)
        
        # Draw DSA challenge if active
        if self.mode == "dsa_challenge" and hasattr(self, 'dsa_system') and self.paused:
            self.dsa_system.draw()
        
        # Game over message
        if self.game_over:
            font = pygame.font.SysFont('Arial', 50)
            text = font.render('Game Over! Press R to restart', True, RED)
            self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))
            
        # Pause message
        if self.paused and not self.game_over and self.mode != "dsa_challenge":
            font = pygame.font.SysFont('Arial', 50)
            text = font.render('PAUSED - Press SPACE to continue', True, YELLOW)
            self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))