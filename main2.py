import pygame
from src.menu import MainMenu
from src.game2 import Game
from src.constants import *
from src.settings import Settings
from src.liderboard import Ladder

def main():
    # Инициализация pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Сапер")
    clock = pygame.time.Clock()


    # Состояния игры
    current_screen = "menu"
    menu = MainMenu(WINDOW_WIDTH, WINDOW_HEIGHT)
    game = None
    sett = Settings()
    ladder = Ladder()
    width, height, mines = sett.get_param()

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
                elif action == "Settings":
                    current_screen = "settings"
                elif action == "Quit":
                    running = False
                

            # Игровой экран
            elif current_screen == "game" and game:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if waiting_for_click:
                        current_screen = "menu"
                        waiting_for_click = False
                    else:
                        result = game.handle_click(mouse_pos[0], mouse_pos[1], event.button)
                        if result == "game_won":
                            #name, time = game.get_res()
                            #ladder.write(name, time)
                            waiting_for_click = True
                        elif result == "game_over":
                            waiting_for_click = True


            # Настройки
            elif current_screen == "settings":
                action = sett.handle_event(event)
                if action == "back":
                    current_screen = "menu"

        # Отрисовка
        screen.fill((228, 194, 159))  # Фон

        if current_screen == "menu":
            menu.draw(screen)
        elif current_screen == "game" and game:
            if not game.time_stop:
                game.update_timer()
            game.draw(screen)
        elif current_screen == "settings":
            sett.draw(screen)
            

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()