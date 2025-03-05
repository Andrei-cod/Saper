import pygame

class Button:
    '''
    Класс Button - кнопка. Для создания нужны текст, позиция, размер кнопки, цвет, шрифт текста\n
    У класса есть два метода:\n
    draw(screen) - передаем методу экран в котором рисовать и на переданном экране рисуется кнопка\n
    is_clicked(mouse_pos) - передаем позицию мышки и метод вернет True, если мышкой попали в кнопку, и соответственно False, если нет\n
    '''
    def __init__(self, text, position, size, color, font):
        self.text = text
        self.position = position
        self.size = size
        self.color = color
        self.font = font
        self.rect = pygame.Rect(position, size)

    def draw(self, screen):
        "Отрисовка кнопки на экране <b>screen</b>"
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, False, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        "Проверка находится ли <b>mouse_pos</b> в области кнопки"
        return self.rect.collidepoint(mouse_pos)