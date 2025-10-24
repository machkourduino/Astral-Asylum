import sys
import os
from level import Level
import pygame.gfxdraw

screen_width = 1200
screen_height = 690
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (80, 30)
# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
level = Level(screen)

size = 34
pygame_icon = pygame.image.load("../graphics/Icon.png")
pygame_icon = pygame.transform.scale(pygame_icon, (size, size))
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption('Astral Asylum')

clock = pygame.time.Clock()
full = False
pause = False
menu = True

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN and menu == True:
				menu = False

			if event.key == pygame.K_RETURN:
				pygame.mixer.music.play()



			if event.key == pygame.K_m:
				if pause == False:
					pause = True
					break
				else:
					pause = False
			if event.key == pygame.K_f and full == False and menu == False:
				full = True
				screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

			elif event.key == pygame.K_f and full == True:
				full = False
				screen = pygame.display.set_mode((screen_width, screen_height))




	level.run(pause, menu)

	pygame.display.update()
	clock.tick(30)

input('Press ENTER to exit')
