import pygame
import sys
from game import game_loop
from menu import main_menu

pygame.init()

def display_message(screen, message, sub_message):
    font = pygame.font.Font(None, 36)
    screen.fill((0, 0, 0))
    text = font.render(message, True, (255, 255, 255))
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
    sub_text = font.render(sub_message, True, (255, 255, 255))
    screen.blit(sub_text, (screen.get_width() // 2 - sub_text.get_width() // 2, screen.get_height() // 2 - sub_text.get_height() // 2 + 50))
    pygame.display.flip()

def main():
    screen = pygame.display.set_mode((400, 300))
    while True:
        main_menu()
        result = game_loop()
        display_message(screen, result, "Press SPACE to Return to Main Menu")
        
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting_for_input = False

if __name__ == "__main__":
    main()
