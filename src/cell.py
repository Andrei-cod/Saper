import pygame
import src.constans as sc

class Cell:
    def __init__(self, is_bomb, bomb_around, position):
        self.is_bomb = is_bomb
        self.bomb_around = bomb_around
        self.bomb_counter_color = [(0,128,0),(255,255,0),(65,105,225),(255,165,0),(255,0,0),(128,0,0),(47,79,79),(0,0,0)]
        self.position = position
        self.condition = "close"
        self.rect = pygame.Rect(position,(sc.CELL_WIDTH, sc.CELL_HEIGHT))
        self.simple_color = sc.CELL_COLOR
        self.marled_color = sc.CELL_MARKED_COLOR
        self.font = self.font = pygame.font.Font(None, 50)

    def draw(self, screen):
        "Отрисовка кнопки на экране <b>screen</b>"
        if self.condition == "close":
            pygame.draw.rect(screen, self.simple_color, self.rect)
        elif self.condition == "marked":
            pygame.draw.rect(screen, self.marled_color, self.rect)
        else:
            pygame.draw.rect(screen, self.simple_color, self.rect)
            text_surface = self.font.render(self.bomb_around, False, self.bomb_counter_color[self.bomb_around-1])
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
    
    def is_clicked(self, event):
        "Проверка находится ли <b>mouse_pos</b> в области кнопки"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if event.button == 1:
                    self.condition = "open"
                if event.button == 3:
                    self.condition = "marked"
        
