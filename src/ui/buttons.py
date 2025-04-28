import pygame

class Button:
    '''
    Класс Button - кнопка. Для создания нужны текст, позиция, размер кнопки, цвет, шрифт текста\n
    У класса есть два метода:\n
    draw(screen) - передаем методу экран в котором рисовать и на переданном экране рисуется кнопка\n
    is_clicked(mouse_pos) - передаем позицию мышки и метод вернет True, если мышкой попали в кнопку, и соответственно False, если нет\n
    '''
    def __init__(self, position, size, color, font=None, image=None,text=None):
        self.image = image
        self.text = text
        self.position = position
        self.size = size
        self.color = color
        self.font = font
        self.rect = pygame.Rect(position, size)
        self.border_be = False
        self.border_rect = None
        self.border_color = None

    def add_border(self, width:int, color:tuple):
        self.border_be = True
        self.border_rect = pygame.Rect((self.position[0] - width, self.position[1] - width), (self.size[0] + 2 * width,self.size[1] + 2 * width))
        self.border_color = color

    def draw(self, screen):
        """Отрисовка кнопки на экране `screen`.
        Если есть изображение (`self.image`), рисует его в центре кнопки.
        Если есть текст (`self.text`), рисует текст в центре кнопки.
        """
        # Отрисовка прямоугольника кнопки
    
        if self.border_be:
            pygame.draw.rect(screen,self.border_color,self.border_rect)
        pygame.draw.rect(screen, self.color, self.rect)
        
        if self.image:  # Если есть изображение
            # Масштабируем изображение под размер кнопки (если нужно)
            scaled_image = pygame.transform.scale(self.image, (min(self.size),min(self.size)))
            screen.blit(scaled_image, self.rect)
        elif self.text:  # Если есть текст
            text_surface = self.font.render(self.text, True, (255, 255, 255))  # True - сглаживание
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        "Проверка находится ли <b>mouse_pos</b> в области кнопки"
        return self.rect.collidepoint(mouse_pos)