import pygame
from src.ui.buttons import Button
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT
"""sett = Settings()
    width = sett.get_width()
    height= sett.get_height()
    mines = sett.get_mines()"""
class Settings:
    def __init__(self):
        # Параметры по умолчанию
        self.size = (15, 15)
        self.mines = 1
        
        # Варианты настроек
        self.size_options = [
            {"label": "15×15", "size": (15, 15), "mines": 20},
            {"label": "20×20", "size": (20, 20), "mines": 50}, 
            {"label": "25×25", "size": (25, 25), "mines": 99}
        ]
        
        self.buttons = []
        self.back_button = None
        self.init_buttons()

    def init_buttons(self):
        """Инициализация кнопок"""
        # Кнопки выбора размера
        button_width, button_height = 200, 60
        start_y = WINDOW_HEIGHT // 2 - len(self.size_options) * button_height // 2
        
        for i, option in enumerate(self.size_options):
            button = Button(
                position=(WINDOW_WIDTH//2 - button_width//2, start_y + i*(button_height + 40)),
                size=(button_width, button_height),
                color=(200, 200, 200),
                text=option["label"], 
                font=pygame.font.SysFont("Arial", 28)
            )
            self.buttons.append(button)

        # Кнопка "Назад"
        self.back_button = Button(
            position=(20, WINDOW_HEIGHT - 70),
            size=(120, 50),
            color=(200, 150, 150),
            text="Назад",
            font=pygame.font.SysFont("Arial", 24)
        )

    def handle_event(self, event):
        """Обработка событий"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка кнопок размера
            for i, button in enumerate(self.buttons):
                if button.rect.collidepoint(event.pos):
                    self.size = self.size_options[i]["size"]
                    self.mines = self.size_options[i]["mines"]
            
            # Проверка кнопки "Назад"
            if self.back_button.rect.collidepoint(event.pos):
                return "back"

    def get_param(self):
        """Возврат размеров и количества мин"""
        return self.size[0],self.size[0],self.mines

    def draw(self, screen):
        """Отрисовка интерфейса"""
        # Фон
        screen.fill((228, 194, 159))
        
        # Заголовок
        font = pygame.font.SysFont("Arial", 48, bold=True)
        title = font.render("Выберите размер поля", True, (0, 0, 0))
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4))
        screen.blit(title, title_rect)
        
        # Кнопки размеров
        for i, button in enumerate(self.buttons):
            if self.size == self.size_options[i]["size"]:
                button.color = (100, 200, 100)  # Зеленый для выбранного
            else:
                button.color = (200, 200, 200)  # Серый для остальных
                
            button.draw(screen)
            
            # Количество мин
            font_small = pygame.font.SysFont("Arial", 20)
            mines_text = font_small.render(
                f"Мин: {self.size_options[i]['mines']}", 
                True, 
                (0, 0, 0)
            )
            mines_rect = mines_text.get_rect(
                center=(button.rect.centerx, button.rect.bottom + 15)
            )
            screen.blit(mines_text, mines_rect)
        
        # Кнопка "Назад"
        self.back_button.draw(screen)