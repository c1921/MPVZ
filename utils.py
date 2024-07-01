import pygame

def draw_grid(screen, cols, rows, cell_width, cell_height):
    white = (255, 255, 255)
    for col in range(cols):
        for row in range(rows):
            rect = pygame.Rect(col * cell_width, 50 + row * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, white, rect, 1)
