import pygame
import sys
from game.flappy_bird import FlappyBirdGame
from ai.neat_manager import NEATManager
from ui.menu import MainMenu
from utils.constants import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird AI + DSA Challenges")
    
    clock = pygame.time.Clock()
    menu = MainMenu(screen)
    game = None
    neat_manager = None
    
    running = True
    while running:
        current_state = menu.current_state
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if current_state == "menu":
                menu.handle_event(event)
            elif current_state == "game":
                game.handle_event(event)
            elif current_state == "ai_training":
                neat_manager.handle_event(event)
        
        # State management
        if menu.current_state != current_state:
            if menu.current_state == "game":
                game = FlappyBirdGame(screen, "human")
            elif menu.current_state == "ai_training":
                neat_manager = NEATManager(screen)
            elif menu.current_state == "dsa_challenge":
                game = FlappyBirdGame(screen, "dsa_challenge")
            elif menu.current_state == "exit":
                running = False
        
        # Update and render based on current state
        if menu.current_state == "menu":
            menu.update()
            menu.render()
        elif menu.current_state == "game":
            game.update()
            game.render()
        elif menu.current_state == "ai_training":
            neat_manager.update()
            neat_manager.render()
        elif menu.current_state == "dsa_challenge":
            game.update()
            game.render()
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()