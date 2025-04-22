import pygame
from src.menu import MainMenu
from src.game2 import Game
from src.constants import *
from src.settings import Settings

def main():
    # Инициализация pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Сапер")
    clock = pygame.time.Clock()

    # Состояния игры
    current_screen = "menu"  # menu/game
    menu = MainMenu(WINDOW_WIDTH, WINDOW_HEIGHT)
    game = None
    sett = Settings()
    width = sett.get_width()
    height= sett.get_height()
    mines = sett.get_mines()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Главное меню
            if current_screen == "menu":
                action = menu.handle_event(event)
                if action == "Start Game":
                    game = Game(width, height, mines)
                    current_screen = "game"
                    waiting_for_click = False
                elif action == "Quit":
                    running = False

            # Игровой экран
            elif current_screen == "game" and game:
                game.update_timer()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if waiting_for_click:
                        current_screen = "menu"
                        waiting_for_click = False
                    else:
                        result = game.handle_click(mouse_pos[0], mouse_pos[1], event.button)
                        if result in ("game_over", "game_won"):
                            waiting_for_click = True

        # Отрисовка
        screen.fill((228, 194, 159))  # Фон

        if current_screen == "menu":
            menu.draw(screen)
        elif current_screen == "game" and game:
            game.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()