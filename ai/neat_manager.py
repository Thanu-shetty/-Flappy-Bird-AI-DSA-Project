import pygame
import neat
import os
import random
from game.bird import Bird
from game.pipe import PipeSystem
from game.score_manager import ScoreManager
from utils.constants import *

class NeuralBird(Bird):
    def __init__(self, x, y, genome, config):
        super().__init__(x, y)
        self.genome = genome
        self.neural_network = neat.nn.FeedForwardNetwork.create(genome, config)
        self.fitness = 0
        self.alive = True
        
    def think(self, pipes):
        if not pipes:
            return False
            
        # Find the next pipe
        next_pipe = None
        for pipe in pipes:
            if pipe.x + pipe.width > self.x:
                next_pipe = pipe
                break
                
        if not next_pipe:
            return False
            
        # Inputs: bird y, pipe top, pipe bottom, pipe x, velocity
        inputs = (
            self.y / SCREEN_HEIGHT,
            next_pipe.height / SCREEN_HEIGHT,
            (next_pipe.height + PIPE_GAP) / SCREEN_HEIGHT,
            (next_pipe.x - self.x) / SCREEN_WIDTH,
            self.velocity / 10
        )
        
        output = self.neural_network.activate(inputs)
        return output[0] > 0.5

class NEATManager:
    def __init__(self, screen):
        self.screen = screen
        self.config = self.load_config()
        self.population = neat.Population(self.config)
        self.generation = 0
        self.birds = []
        self.pipes = PipeSystem()
        self.best_fitness = 0
        
        # Statistics
        self.stats = {
            'generation': [],
            'best_fitness': [],
            'average_fitness': []
        }
        
    def load_config(self):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, '..', 'config.txt')
        return neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
                          config_path)
    
    def eval_genomes(self, genomes, config):
        self.generation += 1
        self.birds = []
        self.pipes = PipeSystem()
        
        for genome_id, genome in genomes:
            bird = NeuralBird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, genome, config)
            self.birds.append(bird)
            
        clock = pygame.time.Clock()
        running = True
        
        while running and any(bird.alive for bird in self.birds):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            
            # Update pipes
            self.pipes.update()
            
            # Update birds
            for bird in self.birds:
                if bird.alive:
                    # Neural network decision
                    if bird.think(self.pipes.pipes):
                        bird.jump()
                    
                    bird.update()
                    bird.fitness += 0.1  # Reward for staying alive
                    
                    # Check collisions
                    if (self.pipes.check_collision(bird) or 
                        bird.y > SCREEN_HEIGHT or 
                        bird.y < 0):
                        bird.alive = False
                        bird.fitness -= 1
                    
                    # Check scoring
                    if self.pipes.check_scoring(bird):
                        bird.fitness += 5  # Reward for passing pipes
            
            # Remove dead birds from evaluation
            alive_birds = [bird for bird in self.birds if bird.alive]
            if not alive_birds:
                break
                
            # Update genomes fitness
            for bird in self.birds:
                bird.genome.fitness = bird.fitness
            
            # Render (optional for visualization)
            self.render()
            pygame.display.update()
            clock.tick(FPS)
    
    def update(self):
        # Run one generation
        winner = self.population.run(self.eval_genomes, 1)
        
        # Update statistics
        best_fitness = max([genome.fitness for genome in self.population.population.values()])
        avg_fitness = sum([genome.fitness for genome in self.population.population.values()]) / len(self.population.population)
        
        self.stats['generation'].append(self.generation)
        self.stats['best_fitness'].append(best_fitness)
        self.stats['average_fitness'].append(avg_fitness)
        
        if best_fitness > self.best_fitness:
            self.best_fitness = best_fitness
    
    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw pipes
        self.pipes.draw(self.screen)
        
        # Draw birds
        for bird in self.birds:
            if bird.alive:
                bird.draw(self.screen)
        
        # Draw info
        font = pygame.font.SysFont('Arial', 24)
        gen_text = font.render(f'Generation: {self.generation}', True, WHITE)
        alive_text = font.render(f'Alive: {sum(1 for bird in self.birds if bird.alive)}', True, WHITE)
        best_text = font.render(f'Best Fitness: {self.best_fitness:.2f}', True, WHITE)
        
        self.screen.blit(gen_text, (10, 10))
        self.screen.blit(alive_text, (10, 40))
        self.screen.blit(best_text, (10, 70))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from ui.menu import MainMenu
                # Return to menu logic here