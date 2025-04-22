import pygame
import random
import time
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
        self.game_won = False
        self.start_time = 0
        self.elapsed_time = 0 
        self.timer_running = False
        self.start_x = WINDOW_WIDTH//CELL_SIZE//2 - self.width//2
        self.start_y = WINDOW_HEIGHT//CELL_SIZE//2 - self.height//2
        self.init_cells()
        self.init_buttons()

    def init_cells(self):
        self.cells = [
            [Cell(self.start_x + x, self.start_y + y, CELL_SIZE) 
            for x in range(self.width)] 
            for y in range(self.height)
        ]
    def init_buttons(self):
        self.pause_button = Button(
            position=(WINDOW_WIDTH-40-2, 2),
            size=(40, 40),
            color=(228, 194, 159),
            image=pygame.image.load("assets/pause.png")
        )

    

    def generate_mines(self, exclude_x, exclude_y):
        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x].is_mine = False
        
        all_positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        
        forbidden = set()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = exclude_x + dx, exclude_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    forbidden.add((nx, ny))
        
        valid_positions = [pos for pos in all_positions if pos not in forbidden]
        mines_to_place = min(self.mines_count, len(valid_positions))
        random.shuffle(valid_positions)
        self.mines_positions = valid_positions[:mines_to_place]
        
        for x, y in self.mines_positions:
            self.cells[y][x].is_mine = True
        
        self.update_mines_count()

    def update_mines_count(self):
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
    
    def format_time(self, milliseconds):
        """Форматирует время в ММ:СС из миллисекунд"""
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def start_timer(self):
        if not self.timer_running:
            self.start_time = pygame.time.get_ticks()
            self.timer_running = True

    def stop_timer(self):
        self.timer_running = False

    def pause_timer(self):
        if self.timer_running:
            self.elapsed_time = pygame.time.get_ticks() - self.start_time
            self.timer_running = False

    def resume_timer(self):
        if not self.timer_running and not self.game_over and not self.game_won:
            self.start_time = pygame.time.get_ticks() - self.elapsed_time
            self.timer_running = True

    def update_timer(self):
        if self.timer_running and not self.game_over and not self.game_won:
            self.elapsed_time = pygame.time.get_ticks() - self.start_time

    def draw_timer(self, screen):
        font = pygame.font.SysFont("Arial", 36)
        timer_text = font.render(f"{self.format_time(self.elapsed_time)}", True, (0, 0, 0))
        screen.blit(timer_text, (20, 20))

    def handle_click(self, mouse_x, mouse_y, mouse_button):
        if self.check_win():
            self.game_won = True
            self.stop_timer()
        if self.game_over or self.game_won:
            return
        
        x = (mouse_x - self.start_x * CELL_SIZE) // CELL_SIZE
        y = (mouse_y - self.start_y * CELL_SIZE) // CELL_SIZE
        
        if not (0 <= x < self.width and 0 <= y < self.height):
            if self.pause_button.rect.collidepoint(mouse_x, mouse_y):
                self.paused = not self.paused
                if self.paused:
                    self.pause_timer()
                else:
                    self.resume_timer()
            return
            
        cell = self.cells[y][x]

        if self.first_click:
            self.generate_mines(x, y)
            self.start_timer()
            self.first_click = False
            self.open_cell(x, y)
            return

        if mouse_button == 1:
            if cell.state == "closed":
                if cell.is_mine:
                    self.game_over = True
                    self.stop_timer()
                self.open_cell(x, y)
                
            elif cell.state == "opened" and cell.mine_around > 0:
                if not self.open_surrounding(x, y):
                    self.game_over = True
                    self.stop_timer()

        elif mouse_button == 3:
            if cell.state == "closed":
                cell.state = "flagged"
            elif cell.state == "flagged":
                cell.state = "closed"

    def open_surrounding(self, x, y):
        mines_around = flagged_around = 0
        
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
        
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    self.open_cell(nx, ny)
        
        return True

    def open_cell(self, x, y):
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
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[y][x]
                if not cell.is_mine and cell.state != "opened":
                    return False
        return True

    def draw_mines_counter(self, screen):
        flagged = sum(1 for row in self.cells for cell in row if cell.state == "flagged")
        mines_left = max(0, self.mines_count - flagged)
        
        font = pygame.font.SysFont("Arial", 36)
        text = font.render(f"{mines_left}/{self.mines_count}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 30))
        screen.blit(text, text_rect)

    def draw_message(self, screen, message):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((228, 194, 159, 200))
        screen.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont("Arial", 72, bold=True)
        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        screen.blit(text, text_rect)
        
        font_small = pygame.font.SysFont("Arial", 36)
        hint = font_small.render("Нажмите для возврата в меню", True, (0, 0, 0))
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
        screen.blit(hint, hint_rect)

    def draw(self, screen):
        for row in self.cells:
            for cell in row:
                cell.draw(screen)
        
        self.draw_mines_counter(screen)
        self.draw_timer(screen)
        
        pause_button = Button(
            position=(WINDOW_WIDTH-40-2, 2),
            size=(40, 40),
            color=(228, 194, 159),
            image=pygame.image.load("assets/pause.png")
        )
        border = pygame.Rect(WINDOW_WIDTH-44, 0, 44, 44)
        pygame.draw.rect(screen, (128, 128, 128), border)
        pause_button.draw(screen)
        
        if self.game_over:
            self.draw_message(screen, "Вы проиграли!")
        elif self.game_won:
            self.draw_message(screen, "Вы победили!")