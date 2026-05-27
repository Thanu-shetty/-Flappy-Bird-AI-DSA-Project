import pygame
import os

def load_image(name, scale=1):
    """Load and scale an image"""
    try:
        image = pygame.image.load(name)
        if scale != 1:
            new_size = (int(image.get_width() * scale), 
                       int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
        return image.convert_alpha()
    except pygame.error:
        print(f"Could not load image: {name}")
        return None

def draw_text(surface, text, color, rect, font_size=24, align="center"):
    """Draw text within a rectangle with alignment"""
    font = pygame.font.SysFont('Arial', font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if align == "center":
        text_rect.center = rect.center
    elif align == "topleft":
        text_rect.topleft = rect.topleft
    
    surface.blit(text_surface, text_rect)

def create_gradient(width, height, start_color, end_color):
    """Create a vertical gradient surface"""
    gradient = pygame.Surface((width, height))
    for y in range(height):
        # Interpolate between start and end color
        ratio = y / height
        r = start_color[0] + (end_color[0] - start_color[0]) * ratio
        g = start_color[1] + (end_color[1] - start_color[1]) * ratio
        b = start_color[2] + (end_color[2] - start_color[2]) * ratio
        pygame.draw.line(gradient, (int(r), int(g), int(b)), (0, y), (width, y))
    return gradient