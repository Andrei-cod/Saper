import pygame
import random
from src.cell import Cell
from src.ui.buttons import Button
from src.constants import WINDOW_HEIGHT, WINDOW_WIDTH, CELL_SIZE

class Game:
    def __init__(self, width=10, height=10, mines_count=15):
        self.width = width
        self.height = height
        self.mines_count = mines_count
        self.cells = []
        self.mines_positions = []
        self.first_click = True
        self.game_over = False
        self.start_x = WINDOW_WIDTH//CELL_SIZE//2 - self.width//2
        self.start_y = WINDOW_HEIGHT//CELL_SIZE//2 - self.height//2
        self.init_cells()
        

    def init_cells(self):
        """Инициализация всех клеток"""
        self.cells = [
            [Cell(self.start_x + x, self.start_y + y, CELL_SIZE) 
            for x in range(self.width)] 
            for y in range(self.height)
        ]

    def generate_mines(self, exclude_x, exclude_y):
        """Генерация мин с очисткой предыдущих и исключением:
        - зоны первого клика (3x3 клетки)
        - уже открытых клеток
        """
        # Очищаем все существующие мины
        '''for y in range(self.height):
            for x in range(self.width):
                self.cells[x][y].is_mine = False'''
        
        # Собираем все возможные позиции
        all_positions = [
            (x, y) 
            for x in range(self.width)
            for y in range(self.height)
        ]
        
        # Запрещенные позиции:
        forbidden = set()
        
        # Исключаем зону 3x4 вокруг первого клика
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = exclude_x + dx, exclude_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    forbidden.add((nx, ny))
        
        # Исключаем уже открытые клетки
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[x][y].state == "opened":
                    forbidden.add((x, y))
        
        # Отбираем только разрешенные позиции
        valid_positions = [pos for pos in all_positions if pos not in forbidden]
        
        # Проверяем, что мин не больше чем доступных клеток
        mines_to_place = min(self.mines_count, len(valid_positions))
        
        # Случайно выбираем позиции для мин
        random.shuffle(valid_positions)
        self.mines_positions = valid_positions[:mines_to_place]
        
        # Расставляем новые мины
        for x, y in self.mines_positions:
            self.cells[x][y].is_mine = True
        
        # Обновляем счетчики мин
        self.update_mines_count()

    def update_mines_count(self):
        """Обновляет количество мин вокруг каждой клетки"""
        for x in range(self.width):
            for y in range(self.height):
                if not self.cells[x][y].is_mine:
                    count = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if (0 <= nx < self.width and 0 <= ny < self.height 
                                and self.cells[nx][ny].is_mine):
                                count += 1
                    self.cells[x][y].mine_around = count

    def handle_click(self, x, y, mouse_button):
        """Обрабатывает клик по клетке"""
        if self.game_over:
            return None
        x -= self.start_x
        y -= self.start_y

        cell = self.cells[x][y]

        # Первый клик - всегда открытие
        if self.first_click:
            self.generate_mines(x, y)
            self.first_click = False
            self.open_cell(x, y)
            return None

        # ЛКМ - только по открытым клеткам
        if mouse_button == 1 and cell.state == "opened":
            if not self.open_surrounding(x, y):  # Если есть неотмеченные мины
                return "Kaboom"  # Игра окончена
        
        # ПКМ - переключение флажков
        elif mouse_button == 3:
            if cell.state == "closed" and cell.is_mine:
                cell.state = "flagged"
                self.mines_count -= 1
            elif cell.state == "flagged" and cell.is_mine:
                cell.state = "closed"
                self.mines_count += 1
        
        return None

    def open_surrounding(self, x, y):
        """Открывает соседей в радиусе 1, возвращает False если есть неотмеченные мины"""
        mines_around = 0
        flagged_around = 0
        positions = []
        
        # Сначала проверяем соседей
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  
                
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbor = self.cells[ny][nx]
                    positions.append((nx, ny))
                    if neighbor.is_mine:
                        mines_around += 1
                        if neighbor.state == "flagged":
                            flagged_around += 1
        
        # Если есть неотмеченные мины - взрыв
        if mines_around > flagged_around:
            for nx, ny in positions:
                if self.cells[ny][nx].is_mine and self.cells[ny][nx].state != "flagged":
                    self.game_over = True
                    return False
        
        # Открываем все неотмеченные соседи
        for nx, ny in positions:
            neighbor = self.cells[ny][nx]
            if neighbor.state == "closed":
                self.open_cell(nx, ny)
        
        return True

    def open_cell(self, x, y):
        """Открывает клетку и соседей (если пустые)"""
        if (not 0 <= x < self.width or not 0 <= y < self.height or
            self.cells[x][y].state != "closed"):
            return

        self.cells[x][y].state = "opened"

        # Если пустая клетка - открываем соседей
        if self.cells[x][y].mine_around == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx != 0 or dy != 0:  # Не проверяем текущую клетку
                        self.open_cell(x + dx, y + dy)

    def draw(self, screen):
        """Отрисовывает игровое поле"""
        for row in self.cells:
            for cell in row:
                cell.draw(screen)
        pause = Button(
            position=(WINDOW_WIDTH-40-2,0+2),
            size=(40,40),
            color=(228, 194, 159),
            image=pygame.image.load("assets/pause.png"))
        border = pygame.Rect((WINDOW_WIDTH-44,0), (44,44))
        pygame.draw.rect(screen, (128, 128, 128), border)
        pause.draw(screen)