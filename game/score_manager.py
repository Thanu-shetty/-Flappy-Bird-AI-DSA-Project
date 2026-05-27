import pygame
from utils.constants import *

class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        
    def increment_score(self):
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score
            
    def reset_score(self):
        self.score = 0
        
    def draw(self, screen):
        font = pygame.font.SysFont('Arial', 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        high_score_text = font.render(f'High Score: {self.high_score}', True, WHITE)
        
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 50))