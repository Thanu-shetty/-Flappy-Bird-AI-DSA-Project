import pygame
from utils.constants import *

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.radius = BIRD_RADIUS
        
    def jump(self):
        self.velocity = JUMP_STRENGTH
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius, 2)
        
        # Draw eye
        pygame.draw.circle(screen, BLACK, (int(self.x + 5), int(self.y - 5)), 3)
        
    def get_mask(self):
        # For pixel-perfect collision (simplified)
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)