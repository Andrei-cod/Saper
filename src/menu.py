import pygame
from src.ui.buttons import Button
import src.constants 

class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.buttons = []  # Список кнопок
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 50)
        self.create_buttons()

    def create_buttons(self):
        button_width = 500
        button_height = 100
        spacing = 20
        # Вычисляем стартовую высоту с учетом логотипа
        start_height = (self.screen_height - src.constants.LOGO_HEIGHT - 3 * button_height - 2 * spacing)

        # Создаем кнопки
        buttons_data = [
            ("Start Game", "Играть"),
            ("Leaderboard", "Таблица лидеров"),
            ("Settings", "Настройки"),
            ("Quit", "Выход")
        ]

        for i, (action, text) in enumerate(buttons_data):
            button = Button(
                text=text,
                position=((self.screen_width - button_width) // 2, 
                         start_height + i * (button_height + spacing)),
                size=(button_width, button_height),
                color=(128, 128, 128),
                font=self.font
            )
            self.buttons.append((action, button))

    def handle_event(self, event):
        """Обрабатывает события и возвращает действие кнопки или None"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                mouse_pos = pygame.mouse.get_pos()
                for action, button in self.buttons:  # Исправлено: buttons вместо buttons()
                    if button.is_clicked(mouse_pos):  # Исправлено: is_clicked вместо is_cliced
                        return action
        return None

    def draw(self, screen):
        """Отрисовывает меню на экране"""
        screen.fill((228, 194, 159))  # Заливка фона
        
        # Загрузка и отрисовка логотипа
        try:
            image = pygame.image.load("assets/pngwing.png").convert_alpha()
            image_rect = image.get_rect(center=(self.screen_width // 2, self.screen_height // 3.5))
            screen.blit(image, image_rect)
        except:
            print("Ошибка загрузки изображения логотипа")
            # Можно добавить заглушку текстом
            title_surface = self.font.render("Сапер", True, (255, 255, 255))
            title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
            screen.blit(title_surface, title_rect)

        # Отрисовка кнопок
        for _, button in self.buttons:
            button.draw(screen)