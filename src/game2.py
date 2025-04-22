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
        self.paused = False

        # Таймер
        self.game_start_time = 0
        self.pause_start_time = 0
        self.paused_duration = 0
        self.view_time = 0
        self.time_stop = True

        # Позиционирование поля
        self.start_x = WINDOW_WIDTH//CELL_SIZE//2 - self.width//2
        self.start_y = WINDOW_HEIGHT//CELL_SIZE//2 - self.height//2

        self.init_cells()
        self.init_pause_ui()

    def init_cells(self):
        """Создание сетки клеток"""
        self.cells = [
            [Cell(self.start_x + x, self.start_y + y, CELL_SIZE)
             for x in range(self.width)]
            for y in range(self.height)
        ]

    def init_pause_ui(self):
        """Инициализация UI паузы"""
        button_width, button_height = 200, 50
        center_x, center_y = WINDOW_WIDTH//2, WINDOW_HEIGHT//2

        self.continue_button = Button(
            position=(center_x - button_width//2, center_y - 70),
            size=(button_width, button_height),
            color=(200, 200, 200),
            text="Продолжить",
            font=pygame.font.SysFont('Arial', 28)
        )

        self.menu_button = Button(
            position=(center_x - button_width//2, center_y + 20),
            size=(button_width, button_height),
            color=(200, 200, 200),
            text="Выход в меню",
            font=pygame.font.SysFont("Arial", 28)
        )

    def start_game_timer(self):
        """Запуск таймера"""
        self.game_start_time = pygame.time.get_ticks()
        self.paused_duration = 0
        self.pause_start_time = 0
        self.time_stop = False

    def update_timer(self):
        """Обновление состояния таймера с учётом пауз"""
        if self.game_start_time == 0:
            return

        if self.paused:
            if self.pause_start_time == 0:  # Пауза только началась
                self.pause_start_time = pygame.time.get_ticks()
        else:
            if self.pause_start_time > 0:  # Пауза только закончилась
                self.paused_duration += pygame.time.get_ticks() - self.pause_start_time
                self.pause_start_time = 0
        self.view_time = self.get_elapsed_time()

    def get_elapsed_time(self):
        """Получение игрового времени в секундах (без учёта пауз)"""
        if self.game_start_time == 0:
            return 0

        current_time = pygame.time.get_ticks()
        if self.paused:
            return (self.pause_start_time - self.game_start_time - self.paused_duration) // 1000
        return (current_time - self.game_start_time - self.paused_duration) // 1000
    
    def draw_timer(self, screen):
        """Orpucoaxa raймера в формате MM,SS"""
        elapsed = self.view_time
        time_text = f"{elapsed // 60:02d},{elapsed % 60:02d}"
        font = pygame.font.SysFont("Arial", 36)
        timer_surface = font.render(time_text, True, (0, 0, 0))
        screen.blit(timer_surface, (10, 10))

    def generate_mines(self, exclude_x, exclude_y):
        """Генерация мин с безопасной зоной"""
        # Сброс мин
        for row in self.cells:
            for cell in row:
                cell.is_mine = False

        # Все возможные позиции
        positions = [(x, y) for x in range(self.width) for y in range(self.height)]

        # Исключаем зону 3х3 вокруг первого клика
        forbidden = set()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = exclude_x + dx, exclude_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    forbidden.add((nx, ny))

        # Выбираем позиции для мин
        valid_positions = [p for p in positions if p not in forbidden]
        mines_count = min(self.mines_count, len(valid_positions))
        self.mines_positions = random.sample(valid_positions, mines_count)

        # Расставляем мины
        for x, y in self.mines_positions:
            self.cells[y][x].is_mine = True

        self.update_mines_count()

    def update_mines_count(self):
        """Обновление счетчиков мин вокруг клеток"""
        for y in range(self.height):
            for x in range(self.width):
                if not self.cells[y][x].is_mine:
                    count = sum(
                        1 for dy in [-1, 0, 1] for dx in [-1, 0, 1]
                        if (0 <= x+dx < self.width and
                            0 <= y+dy < self.height and
                            self.cells[y+dy][x+dx].is_mine))
                    self.cells[y][x].mine_around = count

    def handle_click(self, mouse_x, mouse_y, mouse_button):
        """Обработка всех кликов в игре"""
        # Проверка клика на кнопку паузы
        pause_rect = pygame.Rect(WINDOW_WIDTH-44, 0, 44, 44)
        if pause_rect.collidepoint(mouse_x, mouse_y) and mouse_button == 1:
            self.paused = not self.paused
            return "pause_toggled"

        # Обработка в режиме паузы
        if self.paused:
            if mouse_button == 1:
                if self.continue_button.rect.collidepoint(mouse_x, mouse_y):
                    self.paused = False
                    return "continue"
                elif self.menu_button.rect.collidepoint(mouse_x, mouse_y):
                    return "menu"
            return None

        # Игра завершена
        if self.game_over or self.game_won:
            return None
        
        x = (mouse_x - self.start_x * CELL_SIZE) // CELL_SIZE
        y = (mouse_y - self.start_y * CELL_SIZE) // CELL_SIZE

        if not (0 <= x < self.width and 0 <= y < self.height):
            return None

        cell = self.cells[y][x]

        # Первый клик
        if self.first_click:
            self.start_game_timer() # Запускаем таймер
            self.generate_mines(x, y)
            self.first_click = False
            self.open_cell(x, y)
            return None

        # Левый клик
        if mouse_button == 1:
            if cell.state == "closed":
                if cell.is_mine:
                    self.game_over = True
                    self.reveal_all_mines()
                    self.time_stop = True
                    return "game_over"
                self.open_cell(x, y)
                if self.check_win():
                    self.game_won = True
                    self.flag_all_mines()
                    self.time_stop = True
                    return "game_won"
            elif cell.state == "opened" and cell.mine_around > 0:
                if not self.open_surrounding(x, y):
                    self.game_over = True
                    self.reveal_all_mines()
                    self.time_stop = True
                    return "game_over"
        elif mouse_button == 3:
            if cell.state == "closed":
                cell.state = "flagged"
            elif cell.state == "flagged":
                cell.state = "closed"
            # Проверка победы после изменения флага
            if self.check_win():
                self.game_won = True
                self.flag_all_mines()
                self.time_stop = True
                return "game_won"

        return None

    def open_cell(self, x, y):
        """Рекурсивное открытие клеток"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return

        cell = self.cells[y][x]
        if cell.state != "closed":
            return

        cell.state = "opened"

        # Открываем соседей для пустых клеток
        if cell.mine_around == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        self.open_cell(x + dx, y + dy)

    def open_surrounding(self, x, y):
        """Открытие соседей при клике на число"""
        mines = flags = 0
        to_open = []

        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbor = self.cells[ny][nx]
                    if neighbor.is_mine:
                        mines += 1
                    if neighbor.state == "flagged":
                        flags += 1
                    to_open.append((nx, ny))

        # Проверка безопасного открытия
        if flags < mines:
            return False

        # Открытие клеток
        for nx, ny in to_open:
            self.open_cell(nx, ny)

        return True

    def reveal_all_mines(self):
        """Показ всех мин при проигрыше"""
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.state = "opened"

    def flag_all_mines(self):
        """Пометка всех мин при победе"""
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.state = "flagged"

    def check_win(self):
        """Проверка условий победы"""
        for row in self.cells:
            for cell in row:
                if not cell.is_mine and cell.state != "opened":
                    return False
        return True

    def draw_pause_menu(self, screen):
        """Отрисовка меню паузы"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((100, 100, 100, 150))
        screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont("Arial", 72, bold=True)
        text = font.render("ΠΑУЗА", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 150))
        screen.blit(text, text_rect)

        self.continue_button.draw(screen)
        self.menu_button.draw(screen)

    def draw_message(self, screen, message):
        """Отрисовка сообщения о результате"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((228, 194, 159, 200))
        screen.blit(overlay, (0, 0))

        font_small = pygame.font.SysFont("Arial", 72, bold=True)
        text = font_small.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        screen.blit(text, text_rect)

        font_small = pygame.font.SysFont("Arial", 36)
        text = font_small.render("Нажмите для продолжения", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
        screen.blit(text, text_rect)

    def draw_mines_counter(self, screen):
        """Отрисовка счетчика мин"""
        flagged = sum(cell.state == "flagged" for row in self.cells for cell in row)
        mines_left = max(0, self.mines_count - flagged)

        font = pygame.font.SysFont("Arial", 36)
        text = font.render(f"{mines_left}/{self.mines_count}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 30))
        screen.blit(text, text_rect)

    def draw(self, screen):
        """Основной метод отрисовки"""
        # Игровое поле
        for row in self.cells:
            for cell in row:
                cell.draw(screen)

        # Таймер и счётчик мин
        self.draw_timer(screen)
        self.draw_mines_counter(screen)

        # Кнопка паузы
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

        # Отрисовка состояний
        if self.paused:
            self.draw_pause_menu(screen)
        elif self.game_over:
            self.draw_message(screen, "Вы проиграли!")
        elif self.game_won:
            self.draw_message(screen, "Вы победили!")