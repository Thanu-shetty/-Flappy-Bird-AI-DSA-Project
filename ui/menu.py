import pygame
from utils.constants import *

class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=GREEN):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.SysFont('Arial', 32)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)
    
    def update(self, pos):
        if self.is_hovered(pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.current_state = "menu"
        
        # Create buttons
        button_width, button_height = 300, 60
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        
        self.buttons = [
            Button(center_x, 200, button_width, button_height, "Play Game"),
            Button(center_x, 280, button_width, button_height, "AI Training"),
            Button(center_x, 360, button_width, button_height, "DSA Challenge Mode"),
            Button(center_x, 440, button_width, button_height, "Analytics"),
            Button(center_x, 520, button_width, button_height, "Exit")
        ]
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                for i, button in enumerate(self.buttons):
                    if button.is_hovered(event.pos):
                        if i == 0:  # Play Game
                            self.current_state = "game"
                        elif i == 1:  # AI Training
                            self.current_state = "ai_training"
                        elif i == 2:  # DSA Challenge
                            self.current_state = "dsa_challenge"
                        elif i == 3:  # Analytics
                            self.current_state = "analytics"
                        elif i == 4:  # Exit
                            self.current_state = "exit"
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
    
    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw title
        title_font = pygame.font.SysFont('Arial', 64)
        title_text = title_font.render("Flappy Bird AI + DSA", True, WHITE)
        self.screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        
        subtitle_font = pygame.font.SysFont('Arial', 24)
        subtitle_text = subtitle_font.render("Learn Data Structures & Algorithms through AI Gaming", True, YELLOW)
        self.screen.blit(subtitle_text, (SCREEN_WIDTH//2 - subtitle_text.get_width()//2, 120))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)