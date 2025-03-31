import pygame
import src.constants as sc

import pygame
import os

class Cell:
    def __init__(self, x, y, size, is_mine=False):
        """
        Инициализация клетки
        :param x: координата X на поле
        :param y: координата Y на поле
        :param size: размер клетки в пикселях
        :param is_mine: является ли клетка миной (по умолчанию False)
        """
        self.x = x
        self.y = y
        self.size = size
        self.is_mine = is_mine
        self.mine_around = 0
        self.state = "closed"  # closed, flagged, opened
        self.rect = pygame.Rect(x * size, y * size, size, size)
        
        # Загрузка изображений
        self.image_closed = pygame.image.load(os.path.join('assets', 'image1.png')).convert_alpha()
        self.image_flagged = pygame.image.load(os.path.join('assets', 'image2.png')).convert_alpha()
        self.image_opened = None  # Будет установлено при открытии
        
        # Масштабирование изображений под размер клетки
        self.image_closed = pygame.transform.scale(self.image_closed, (size, size))
        self.image_flagged = pygame.transform.scale(self.image_flagged, (size, size))

    def draw(self, screen):
        """Отрисовка клетки в текущем состоянии"""
        if self.state == "closed":
            screen.blit(self.image_closed, self.rect)
        elif self.state == "flagged":
            screen.blit(self.image_flagged, self.rect)
        elif self.state == "opened":
            if self.is_mine:
                # Отрисовка мины (если нужно)
                pass
            else:
                # Отрисовка числа мин вокруг
                if self.mine_around > 0:
                    # Здесь нужно отрисовать число (можно использовать pygame.font)
                    font = pygame.font.SysFont(None, 30)
                    text = font.render(str(self.mine_around), True, (0, 0, 0))
                    screen.blit(text, (self.rect.x + self.size//2 - 5, self.rect.y + self.size//2 - 5))
                else:
                    # Пустая открытая клетка
                    pygame.draw.rect(screen, (200, 200, 200), self.rect)

    def handle_click(self, mouse_button):
        """
        Обработка кликов по клетке
        :param mouse_button: 1 - ЛКМ, 3 - ПКМ
        :return: "Kaboom" если открыта мина, иначе None
        """
        if mouse_button == 1:  # ЛКМ
            if self.state != "flagged":
                self.state = "opened"
                if self.is_mine:
                    return "Kaboom"
        elif mouse_button == 3:  # ПКМ
            if self.state == "closed":
                self.state = "flagged"
            elif self.state == "flagged":
                self.state = "closed"
        return None

    def set_mine_around(self, count):
        """Установка количества мин вокруг"""
        self.mine_around = count
        # Загрузка соответствующего изображения для открытой клетки
        if count > 0:
            self.image_opened = pygame.image.load(os.path.join('assets', f'mine_around_{count}.png')).convert_alpha()
            self.image_opened = pygame.transform.scale(self.image_opened, (self.size, self.size))