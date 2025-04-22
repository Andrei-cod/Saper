import pygame
from src.menu import MainMenu
from src.game import Game
from src.constants import *
from src.settings import width, height, mines



def main():
    pygame.init() 
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Сапер")
    clock = pygame.time.Clock()

    # Инициализация состояний
    current_screen = "menu"
    menu = MainMenu(WINDOW_WIDTH, WINDOW_HEIGHT)
    game = None
    game_result = None  # Хранит результат игры ("game_over" или "game_won")

    running = True
    while running: 
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False
            
            # Обработка клика при отображении результата игры
            if game_result and event.type == pygame.MOUSEBUTTONDOWN:
                game_result = None
                current_screen = "menu"
                continue
            
            # Обработка событий меню
            if current_screen == "menu":
                action = menu.handle_event(event)
                if action == "Start Game":
                    game = Game(width, height, mines)
                    current_screen = "game"
                    game_result = None
                elif action == "Quit":
                    running = False
            
            # Обработка событий игры
            elif current_screen == "game" and game and not game_result:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Преобразуем экранные координаты в координаты клетки
                    cell_x = (mouse_pos[0] - game.start_x * CELL_SIZE) // CELL_SIZE
                    cell_y = (mouse_pos[1] - game.start_y * CELL_SIZE) // CELL_SIZE
                    
                    # Проверяем что клик внутри поля
                    if 0 <= cell_x < width and 0 <= cell_y < height:
                        result = game.handle_click(mouse_pos[0], mouse_pos[1], event.button)
                        if result in ("game_over", "game_won"):
                            game_result = result

        # Отрисовка
        screen.fill((228, 194, 159))
        
        if current_screen == "menu":
            menu.draw(screen)
        elif current_screen == "game":
            if game:
                game.draw(screen)
                # Отрисовка прозрачного экрана
                if game_result == "game_over":
                    game.draw_message(screen, "Вы проиграли!")
                elif game_result == "game_won":
                    game.draw_message(screen, "Вы победили!")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()