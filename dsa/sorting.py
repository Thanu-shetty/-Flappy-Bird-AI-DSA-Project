import pygame
import random
from utils.constants import *

class SortingChallenge:
    def __init__(self, screen):
        self.screen = screen
        self.array = []
        self.sorted_array = []
        self.algorithm = None
        self.user_input = ""
        self.message = ""
        self.score = 0
        self.completed = False
        self.generate_problem()
        
    def generate_problem(self):
        algorithms = ["bubble_sort", "quick_sort", "merge_sort", "selection_sort"]
        self.algorithm = random.choice(algorithms)
        
        # Generate random array
        self.array = random.sample(range(1, 51), 8)
        self.sorted_array = sorted(self.array)
        
        self.problem = f"Sort this array using {self.algorithm.replace('_', ' ').title()}: {self.array}"
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.check_answer()
            elif event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            else:
                self.user_input += event.unicode
    
    def check_answer(self):
        try:
            user_answer = [int(x.strip()) for x in self.user_input.split(',') if x.strip()]
            if user_answer == self.sorted_array:
                self.message = "Correct! +15 points"
                self.score = 15
                self.completed = True
            else:
                self.message = f"Wrong! Correct sorted array: {self.sorted_array}"
                self.score = 0
                self.completed = True
        except ValueError:
            self.message = "Invalid input! Use comma-separated numbers"
    
    def update(self):
        pass
    
    def draw(self):
        # Draw challenge background
        challenge_rect = pygame.Rect(100, 100, 800, 500)
        pygame.draw.rect(self.screen, (50, 50, 80), challenge_rect)
        pygame.draw.rect(self.screen, WHITE, challenge_rect, 2)
        
        # Draw problem
        font = pygame.font.SysFont('Arial', 24)
        problem_text = font.render(self.problem, True, WHITE)
        self.screen.blit(problem_text, (120, 120))
        
        # Draw input box
        input_rect = pygame.Rect(120, 180, 400, 40)
        pygame.draw.rect(self.screen, WHITE, input_rect, 2)
        input_text = font.render(self.user_input, True, WHITE)
        self.screen.blit(input_text, (130, 185))
        
        # Draw message
        if self.message:
            message_text = font.render(self.message, True, YELLOW)
            self.screen.blit(message_text, (120, 240))
        
        # Draw array visualization
        self.draw_array(self.array, 150, 350, "Original")
        self.draw_array(self.sorted_array, 150, 450, "Sorted")
    
    def draw_array(self, arr, x, y, label):
        font = pygame.font.SysFont('Arial', 20)
        label_text = font.render(label, True, WHITE)
        self.screen.blit(label_text, (x, y - 30))
        
        for i, value in enumerate(arr):
            rect = pygame.Rect(x + i * 60, y, 50, value * 4)
            pygame.draw.rect(self.screen, GREEN, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 1)
            
            value_text = font.render(str(value), True, BLACK)
            self.screen.blit(value_text, (x + i * 60 + 15, y + value * 4 + 5))
    
    def is_completed(self):
        return self.completed
    
    def get_score(self):
        return self.score