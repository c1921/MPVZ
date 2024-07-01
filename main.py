import pygame
import sys
from game import game_loop
from menu import main_menu, draw_button

pygame.init()

def display_message(screen, message):
    font = pygame.font.Font(None, 36)
    screen.fill((0, 0, 0))
    text = font.render(message, True, (255, 255, 255))
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2 - 50))
    pygame.display.flip()

def game_over_screen(screen, result):
    display_message(screen, result)
    waiting_for_input = True
    while waiting_for_input:
        if draw_button(screen, "Restart Game", screen.get_width() // 2 - 75, screen.get_height() // 2, 150, 50, (200, 200, 200), (255, 255, 255), font_size=24):
            return "RESTART_GAME"
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main():
    screen = pygame.display.set_mode((400, 300))
    while True:
        main_menu()
        while True:
            result = game_loop()
            if game_over_screen(screen, result) == "RESTART_GAME":
                continue

if __name__ == "__main__":
    main()
