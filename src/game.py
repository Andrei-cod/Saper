import pygame
import random
from src.cell import Cell
from src.ui.buttons import Button
from src.constants import WINDOW_HEIGHT, WINDOW_WIDTH, CELL_SIZE

class Game:
    def __init__(self, width=10, height=10, mines_count=15):
        """Инициализация игры"""
        self.width = width
        self.height = height
        self.mines_count = mines_count
        self.cells = []
        self.mines_positions = []
        self.first_click = True
        self.game_over = False
        self.game_won = False
        # Центрирование игрового поля
        self.start_x = WINDOW_WIDTH//CELL_SIZE//2 - self.width//2
        self.start_y = WINDOW_HEIGHT//CELL_SIZE//2 - self.height//2
        self.init_cells()

    def init_cells(self):
        """Создание сетки клеток"""
        self.cells = [
            [Cell(self.start_x + x, self.start_y + y, CELL_SIZE) 
            for x in range(self.width)] 
            for y in range(self.height)
        ]

    def generate_mines(self, exclude_x, exclude_y):
        """Генерация мин с безопасной зоной вокруг первого клика"""
        # Очистка предыдущих мин
        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x].is_mine = False
        
        # Подготовка позиций
        all_positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        
        # Исключаем зону 3x3 вокруг первого клика
        forbidden = set()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = exclude_x + dx, exclude_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    forbidden.add((nx, ny))
        
        # Выбираем случайные позиции для мин
        valid_positions = [pos for pos in all_positions if pos not in forbidden]
        mines_to_place = min(self.mines_count, len(valid_positions))
        random.shuffle(valid_positions)
        self.mines_positions = valid_positions[:mines_to_place]
        
        # Устанавливаем мины
        for x, y in self.mines_positions:
            self.cells[y][x].is_mine = True
        
        self.update_mines_count()

    def update_mines_count(self):
        """Подсчет мин вокруг каждой клетки"""
        for y in range(self.height):
            for x in range(self.width):
                if not self.cells[y][x].is_mine:
                    count = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if (0 <= nx < self.width and 0 <= ny < self.height 
                                and self.cells[ny][nx].is_mine):
                                count += 1
                    self.cells[y][x].mine_around = count

    def handle_click(self, mouse_x, mouse_y, mouse_button):
        """Обработка кликов мыши"""
        if self.game_over or self.game_won:
            return None
            
        # Преобразование координат
        x = (mouse_x - self.start_x * CELL_SIZE) // CELL_SIZE
        y = (mouse_y - self.start_y * CELL_SIZE) // CELL_SIZE
        
        if not (0 <= x < self.width and 0 <= y < self.height):
            return None
            
        cell = self.cells[y][x]

        # Первый клик
        if self.first_click:
            self.generate_mines(x, y)
            self.first_click = False
            self.open_cell(x, y)
            return None

        # Левый клик
        if mouse_button == 1:
            if cell.state == "closed":
                if cell.is_mine:
                    self.game_over = True
                    return "game_over"
                self.open_cell(x, y)
                if self.check_win():
                    self.game_won = True
                    return "game_won"
            elif cell.state == "opened" and cell.mine_around > 0:
                if not self.open_surrounding(x, y):
                    self.game_over = True
                    return "game_over"
                if self.check_win():
                    self.game_won = True
                    return "game_won"

        # Правый клик
        elif mouse_button == 3:
            if cell.state == "closed":
                cell.state = "flagged"
            elif cell.state == "flagged":
                cell.state = "closed"
        
        return None

    def open_surrounding(self, x, y):
        """Открытие соседних клеток"""
        mines_around = flagged_around = 0
        
        # Подсчет мин и флагов вокруг
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbor = self.cells[ny][nx]
                    if neighbor.is_mine:
                        mines_around += 1
                        if neighbor.state == "flagged":
                            flagged_around += 1
        
        if mines_around > flagged_around:
            return False
        
        # Открытие соседей
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    self.open_cell(nx, ny)
        
        return True

    def open_cell(self, x, y):
        """Рекурсивное открытие клеток"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
            
        cell = self.cells[y][x]
        if cell.state != "closed":
            return
            
        cell.state = "opened"
        
        if cell.mine_around == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        self.open_cell(x + dx, y + dy)

    def check_win(self):
        """Проверка условий победы"""
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[y][x]
                if not cell.is_mine and cell.state != "opened":
                    return False
        return True

    def draw_mines_counter(self, screen):
        """Отрисовка счетчика мин"""
        flagged = sum(1 for row in self.cells for cell in row if cell.state == "flagged")
        mines_left = max(0, self.mines_count - flagged)
        
        font = pygame.font.SysFont("Arial", 36)
        text = font.render(f"{mines_left}/{self.mines_count}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 30))
        screen.blit(text, text_rect)

    def draw(self, screen):
        """Отрисовка игрового поля"""
        # Клетки
        for row in self.cells:
            for cell in row:
                cell.draw(screen)
        
        # Счетчик мин
        self.draw_mines_counter(screen)
        
        # Кнопка паузы
        pause_button = Button(
            position=(WINDOW_WIDTH-40-2, 2),
            size=(40, 40),
            color=(228, 194, 159),
            image=pygame.image.load("assets/pause.png")
        )
        border = pygame.Rect(WINDOW_WIDTH-44, 0, 44, 44)
        pygame.draw.rect(screen, (128, 128, 128), border)
        pause_button.draw(screen)
    def draw_message(self, screen, message):
        """Отрисовывает сообщение поверх текущего экрана"""
        # Полупрозрачный фон для сообщения
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((228, 194, 159, 200))  # Прозрачный цвет фона
        screen.blit(overlay, (0, 0))
        
        # Основной текст
        font_large = pygame.font.SysFont("Arial", 72, bold=True)
        text = font_large.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        screen.blit(text, text_rect)
        
        # Подсказка
        font_small = pygame.font.SysFont("Arial", 36)
        hint = font_small.render("Нажмите чтобы продолжить", True, (0, 0, 0))
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
        screen.blit(hint, hint_rect)