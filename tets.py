import pygame
import pygame_menu as pm


pygame.init()
surface = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Example resizable window")


menu = pm.Menu(title="Menu",width=1200, height=800, theme= pm.themes.THEME_BLUE)

menu.add.image("assets/pngwing.png",background_color=(228, 230, 246)).scale(0.5,0.5)
menu.add.button('Play',)
menu.add.button('Quit', pm.events.EXIT)


if __name__ == '__main__':
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            


        menu.update(events)

        menu.draw(surface)

        pygame.display.flip()

