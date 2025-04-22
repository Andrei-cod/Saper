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

    running = True
    while running: 
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False
            
            # Обработка событий меню
            if current_screen == "menu":
                action = menu.handle_event(event)
                if action == "Start Game":
                    game = Game(width, height, mines)  # Создаем новую игру 10x10 с 15 минами
                    current_screen = "game"
                elif action == "Quit":
                    running = False
            
            # Обработка событий игры
            elif current_screen == "game" and game:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Получаем координаты клетки
                    start_x = WINDOW_WIDTH//CELL_SIZE//2 - width//2
                    start_y = WINDOW_HEIGHT//CELL_SIZE//2 - height//2
                    cell_size = CELL_SIZE
                    cell_x = mouse_pos[0] // cell_size
                    cell_y = mouse_pos[1] // cell_size
                    
                    # Проверяем что клик внутри поля
                    if start_x <= cell_x < start_x + width and start_y <= cell_y < start_y + height:
                        if event.button == 1:  # ЛКМ
                            result = game.handle_click(cell_x, cell_y, event.button)
                            if result == "Kaboom":
                                print("Вы проиграли!")
                                current_screen = "menu"
                        elif event.button == 3:  # ПКМ
                            game.handle_click(cell_x, cell_y, event.button)
                if game.mines_count == 0:
                    current_screen = "Win"

        # Отрисовка
        screen.fill((228, 194, 159))
        
        if current_screen == "menu":
            menu.draw(screen)
        elif current_screen == "game" and game:
            game.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()