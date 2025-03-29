import pygame
from src.ui.buttons import Button
import src.constans 

class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.buttons = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 50)
        self.create_buttons()

    
    def create_buttons(self):
        button_width = 500
        button_height = 100
        spacing = 20
        start_height = (self.screen_height-src.constans.LOGO_HEIGHT-3*button_height)

        start_button = Button(
            text="Играть",
            position=((self.screen_width-button_width)//2, start_height),
            size=(button_width,button_height),
            color=(128, 128, 128),
            font=self.font
        )
        self.buttons.append(("Start Game", start_button))

        leaderboard_button = Button(
            text="Таблица лидеров",
            position=((self.screen_width-button_width)//2, start_height+ (button_height+spacing)),
            size=(button_width,button_height),
            color=(128, 128, 128),
            font=self.font
        )
        self.buttons.append(("Leaderboard", leaderboard_button))

        settings_button = Button(
            text="Настройки",
            position=((self.screen_width-button_width)//2, start_height+ 2*(button_height+spacing)),
            size=(button_width,button_height),
            color=(128, 128, 128),
            font=self.font
        )
        self.buttons.append(("Settings", settings_button))

        quit_button = Button(
            text="Выход",
            position=((self.screen_width-button_width)//2, start_height+ 3*(button_height+spacing)),
            size=(button_width,button_height),
            color=(128, 128, 128),
            font=self.font
        )
        self.buttons.append(("Quit", quit_button))

    def handle_event(self, event):
        '''Проверяет полученное событие <b>event</b>\n
        Если это клик мыши проверяется попал ли он на одну из кнопок, если попал возвращает действие соответсвующее кнопке\n
        Иначе возвращает <b>None</b>'''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for action, button in self.buttons():
                    if button.is_cliced(mouse_pos):
                        return action
        return None

    
    def draw(self, screen):
        screen.fill((25, 25, 112))
        #title_font = pygame.font.Font(None, 72)
        #title_surface = title_font.render("Minesweeper", True, (255, 255, 255))
        #title_rect = title_surface.get_rect(center=(self.screen_width//2, self.screen_height//4))
        image = pygame.image.load("assets/pngwing.png")
        image_rect = image.get_rect(center=(self.screen_width//2, self.screen_height//3.5))  # Центрирование
        screen.blit(image, image_rect)

        for _, button in self.buttons:
            button.draw(screen)