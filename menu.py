import pygame
import sys

# 设置屏幕大小
screen_width = 400
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置颜色
black = (0, 0, 0)
white = (255, 255, 255)
grey = (200, 200, 200)

pygame.init()  # 初始化Pygame

def draw_button(screen, text, x, y, w, h, inactive_color, active_color, font_size=24):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    small_text = pygame.font.Font(None, font_size)
    text_surf = small_text.render(text, True, black)
    text_rect = text_surf.get_rect(center=(x + w / 2, y + h / 2))
    screen.blit(text_surf, text_rect)
    
    return False

def main_menu():
    while True:
        screen.fill(black)
        if draw_button(screen, "Start Game", screen_width // 2 - 50, screen_height // 2 - 25, 100, 50, grey, white, font_size=24):
            return
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
