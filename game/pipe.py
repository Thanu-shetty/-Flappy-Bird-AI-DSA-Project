import pygame
import random
from utils.constants import *

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - 100 - PIPE_GAP)
        self.passed = False
        self.width = 80
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, self.width, self.height), 2)
        
        # Bottom pipe
        bottom_pipe_y = self.height + PIPE_GAP
        bottom_pipe_height = SCREEN_HEIGHT - bottom_pipe_y
        pygame.draw.rect(screen, GREEN, (self.x, bottom_pipe_y, self.width, bottom_pipe_height))
        pygame.draw.rect(screen, BLACK, (self.x, bottom_pipe_y, self.width, bottom_pipe_height), 2)
        
    def collide(self, bird):
        bird_rect = bird.get_mask()
        
        top_pipe = pygame.Rect(self.x, 0, self.width, self.height)
        bottom_pipe = pygame.Rect(self.x, self.height + PIPE_GAP, self.width, SCREEN_HEIGHT)
        
        return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)

class PipeSystem:
    def __init__(self):
        self.pipes = []
        self.timer = 0
        self.last_pipe_time = pygame.time.get_ticks()
        
    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Add new pipe
        if current_time - self.last_pipe_time > PIPE_FREQUENCY:
            self.pipes.append(Pipe(SCREEN_WIDTH))
            self.last_pipe_time = current_time
            
        # Update pipes and remove off-screen ones
        for pipe in self.pipes[:]:
            pipe.update()
            if pipe.x < -pipe.width:
                self.pipes.remove(pipe)
                
    def draw(self, screen):
        for pipe in self.pipes:
            pipe.draw(screen)
            
    def check_collision(self, bird):
        for pipe in self.pipes:
            if pipe.collide(bird):
                return True
        return False
    
    def check_scoring(self, bird):
        scored = False
        for pipe in self.pipes:
            if not pipe.passed and pipe.x + pipe.width < bird.x:
                pipe.passed = True
                scored = True
        return scored