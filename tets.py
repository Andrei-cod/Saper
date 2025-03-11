import pygame
import pygame_menu as pm

pygame.init()
surface = pygame.display.set_mode((1200, 800),pygame.RESIZABLE)
pygame.display.set_caption("Example resizable window")


def on_resize() -> None:
    """
    Function checked if the window is resized.
    """
    window_size = surface.get_size()
    new_w, new_h = 0.75 * window_size[0], 0.7 * window_size[1]
    menu.resize(new_w, new_h)
    print(f'New menu size: {menu.get_size()}')


menu = pm.Menu(title="Menu",width=1200, height=800)

menu.add.image("assets/pngwing.png",background_color=(239, 231, 211)).scale(0.5,0.5)
menu.add.text_input('Name :', default='John Doe')
menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)])
menu.add.button('Play',)
menu.add.button('Quit', pm.events.EXIT)
menu.enable()
on_resize

if __name__ == '__main__':
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.VIDEORESIZE:
                surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                on_resize

        surface.fill((25, 0, 50))   

        menu.update(events)

        menu.draw(surface)

        pygame.display.flip()