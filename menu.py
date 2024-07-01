import pygame
import sys

# 设置屏幕大小
screen_width = 400
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置颜色
black = (0, 0, 0)
white = (255, 255, 255)

def main_menu():
    font = pygame.font.Font(None, 36)
    while True:
        screen.fill(black)
        text = font.render("Press SPACE to Start", True, white)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
