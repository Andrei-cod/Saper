import pygame
from src.menu import MainMenu
from src.game import Game
from src.constans import *

def main():
	pygame.init() 
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption("Сапер")

	current_screen = "menu"
	menu = MainMenu(WINDOW_WIDTH, WINDOW_HEIGHT)
	game = Game()

	running = True
	while running: 
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				running = False
			
			match current_screen:
				case "menu":
					action = menu.handle_event(event)
					match action:
						case "Start Game":
							current_screen = "game"
						case "Leaderboard":
							current_screen = "leaderboard"
						case "Settings":
							current_screen = "settings"
						case "Quit":
							running = False
				
		if current_screen == "menu":
			menu.draw(screen)

		pygame.display.flip()
	
	
					

if __name__ == "__main__":
	main()