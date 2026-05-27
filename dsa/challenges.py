import pygame
import random
from .binary_tree import BinaryTreeChallenge
from .sorting import SortingChallenge
from .graph_algorithms import GraphChallenge
from utils.constants import *

class DSAChallengeSystem:
    def __init__(self, screen):
        self.screen = screen
        self.active_challenge = None
        self.challenge_completed = False
        self.challenge_types = [BinaryTreeChallenge, SortingChallenge, GraphChallenge]
        self.current_score = 0
        
    def trigger_challenge(self):
        challenge_class = random.choice(self.challenge_types)
        self.active_challenge = challenge_class(self.screen)
        self.challenge_completed = False
        
    def handle_event(self, event):
        if self.active_challenge:
            self.active_challenge.handle_event(event)
            
    def update(self):
        if self.active_challenge and not self.challenge_completed:
            self.active_challenge.update()
            if self.active_challenge.is_completed():
                self.challenge_completed = True
                self.current_score += self.active_challenge.get_score()
                self.active_challenge = None
                
    def draw(self):
        if self.active_challenge:
            self.active_challenge.draw()
            
        # Draw challenge score
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f'DSA Score: {self.current_score}', True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH - 200, 10))