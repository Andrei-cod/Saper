import pygame
import os
from pygame.locals import MOUSEBUTTONDOWN, K_BACKSPACE, KEYDOWN, K_RETURN
from src.constants import *
from src.ui.buttons import Button

class Ladder:
    def __init__(self, font_size=32):
        self.leaderboard_file = "leaderboard.txt"
        self.font_size = font_size
        self.name = "guest"
        self.input_active = False
        self.input_rect = pygame.Rect(0, 0, 300, 40)
        self.submit_rect = pygame.Rect(0, 0, 150, 40)
        self.font = pygame.font.SysFont("Arial", self.font_size)
        self.title_font = pygame.font.SysFont("Arial", 72, bold=True)
        self.time = 0
        self.size = 0
        self.back_button = Button(
            position=(20, WINDOW_HEIGHT - 70),
            size=(120, 50),
            color=(200, 150, 150),
            text="Назад",
            font=pygame.font.SysFont("Arial", 24)
        )
        

    def update_leaderboard(self, name, field_size, time):
        """Обновляет таблицу лидеров или создает файл, если его нет"""
        if not os.path.exists(self.leaderboard_file):
            with open(self.leaderboard_file, 'w') as f:
                f.write("Таблица лидеров:\n")
                f.write(f"Arseniy 25х25 {0.30}\n")
                f.write(f"Anna 25х25 {0.20}\n")
                f.write(f"Andrei 25х25 {0.10}\n")
        
        with open(self.leaderboard_file, 'a') as f:
            f.write(f"{name} {field_size} {time}\n")






        # Отрисовка записей
    def draw_leaderboard(self, screen):
        """Простая отрисовка таблицы лидеров"""
        # Чтение данных
        if os.path.exists(self.leaderboard_file):
            with open(self.leaderboard_file, 'r') as f:
                lines = [line.strip().split() for line in f.readlines()[1:26]]  # Пропускаем заголовок, берём первые 20 записей
                lines.sort(key=lambda x: x[2])
        else:
            lines = []

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((228, 194, 159, 200))
        screen.blit(overlay, (0, 0))

        # Заголовок
        title = self.title_font.render("Таблица лидеров", True, (0, 0, 0))
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 50))
        # Отрисовка
        y = 180
        font = pygame.font.SysFont('Courier New', 24)  # Обязательно моноширинный шрифт!
        
        # Заголовок
        screen.blit(font.render("МЕСТО   ИМЯ                                    РАЗМЕР          ВРЕМЯ", True, (0, 0, 0)), (50, y))
        y += 40
        l = len(lines)
        # Данные
        for i, line in enumerate(lines, 1):
            if i <= l:
                # Форматирование строки с фиксированными отступами
                row_text = f"{i:>3}.   {line[0]:<38}  {line[1]:^8}  {line[2]:>11}"
                screen.blit(font.render(row_text, True, (0, 0, 0)), (50, y))
                y += 30
        for i in range(l+1, 26):
            row_text = f"{i:>3}.   {"-":<38}  {"-":^8}  {"-":>11}"
            screen.blit(font.render(row_text, True, (0, 0, 0)), (50, y))
            y += 30
        
        self.back_button.draw(screen)


                

    def draw_victory_screen(self, screen, field_size, time):
        """Отрисовывает победный экран с полем ввода имени"""


        # Фон
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((228, 194, 159, 200))
        screen.blit(overlay, (0, 0))

        # Надпись "Победа"
        victory_text = self.title_font.render("Победа!", True, (0, 0, 0))
        screen.blit(victory_text, (WINDOW_WIDTH//2 - victory_text.get_width()//2, 100))

        # Информация о игре
        stats_text = self.font.render(f"Размер поля: {field_size} | Время: {time} сек", True, (0, 0, 0))
        screen.blit(stats_text, (WINDOW_WIDTH//2 - stats_text.get_width()//2, 200))

        # Поле ввода
        self.input_rect = pygame.Rect(
            WINDOW_WIDTH//2 - 150,
            WINDOW_HEIGHT//2,
            300, 40
        )
        
        # Отрисовка поля ввода
        pygame.draw.rect(screen, (255, 255, 255), self.input_rect)
        pygame.draw.rect(screen, (100, 200, 255) if self.input_active else (128, 128, 128), self.input_rect, 2)
        
        # Текст в поле ввода
        input_surface = self.font.render(self.name, True, (0, 0, 0))
        screen.blit(input_surface, (self.input_rect.x + 10, self.input_rect.y + 5))

        # Подсказка
        hint = self.font.render("Введите ваше имя:", True, (0, 0, 0))
        screen.blit(hint, (self.input_rect.x, self.input_rect.y - 40))

        # Кнопка подтверждения
        self.submit_rect = pygame.Rect(
            WINDOW_WIDTH//2- 100,
            WINDOW_HEIGHT//2 + 70,
            200, 50
        )
        pygame.draw.rect(screen, (100, 200, 100), self.submit_rect)
        submit_text = self.font.render("Сохранить", True, (255, 255, 255))
        screen.blit(submit_text, (self.submit_rect.x + 25, self.submit_rect.y + 5))
        self.time = time
        self.size = field_size




    def handle_events(self, event):
        """Обрабатывает события для поля ввода"""
        
        
        if event.type == MOUSEBUTTONDOWN:
            if self.back_button.rect.collidepoint(event.pos):
                return "back"
            self.input_active = self.input_rect.collidepoint(event.pos)
            
            if self.submit_rect.collidepoint(event.pos) and self.name:
                self.update_leaderboard(self.name, self.size, self.time)  # Примерные значения
                return True  # Сообщает, что имя сохранено

        if event.type == KEYDOWN and self.input_active:
            if event.key == K_RETURN and self.name:
                self.update_leaderboard(self.name[:15], self.size, self.time)  # Примерные значения
                return True
            elif event.key == K_BACKSPACE:
                self.name = self.name[:-1]
            else:
                self.name += event.unicode

        
        
        return False