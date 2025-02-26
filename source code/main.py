import pygame 

pygame.init() 

screen = pygame.display.set_mode((540, 540)) 

color = (0,125,125)
screen.fill(color)
bg = pygame.image.load("outline-logo.png")
screen.blit(bg,(0,0))
pygame.display.update()


running = True

while running: 
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			running = False
