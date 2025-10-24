import pygame
from support import *

class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, size, tile, color):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.rect = self.image.get_rect(topleft = pos)
		self.tile_type = ''
		self.surf(tile)
		self.color = color

	def update(self,x_shift, y_shift):
		self.image = self.palette_swap(self.image, (255, 148, 66), self.color[0])
		self.image = self.palette_swap(self.image, (50, 66, 66), self.color[1])
		self.rect.x += x_shift

	def surf(self, tile):
		if tile == '1':
			self.tile_type = '12'
			self.flip(False, False, self.tile_type, 0)
		elif tile == '2':
			self.tile_type = '12'
			self.flip(True, False, self.tile_type, 0)
		elif tile == '3':
			self.tile_type = '3'
			self.flip(False, False, self.tile_type, 0)
		elif tile == '4':
			self.tile_type = '45'
			self.flip(False, False, self.tile_type, 0)
		elif tile == '5':
			self.tile_type = '45'
			self.flip(False, False, self.tile_type, 90)
		elif tile == '6':
			self.tile_type = '6789'
			self.flip(False, False, self.tile_type, 0)
		elif tile == '7':
			self.tile_type = '6789'
			self.flip(True, False, self.tile_type, 0)
		elif tile == '8':
			self.tile_type = '6789'
			self.flip(True, True, self.tile_type, 0)
		elif tile == '9':
			self.tile_type = '6789'
			self.flip(False, True, self.tile_type, 0)
		elif tile == '_':
			self.tile_type = '_&-&L&I'
			self.flip(False, True, self.tile_type, 0)
		elif tile == '-':
			self.tile_type = '_&-&L&I'
			self.flip(False, False, self.tile_type, 0)
		elif tile == 'L':
			self.tile_type = '_&-&L&I'
			self.flip(False, False, self.tile_type, 90)
		elif tile == 'I':
			self.tile_type = '_&-&L&I'
			self.flip(False, False, self.tile_type, -90)
		elif tile == 'n':
			self.tile_type = 'nu'
			self.flip(False, False, self.tile_type, 0)
		elif tile == 'u':
			self.tile_type = 'nu'
			self.flip(False, True, self.tile_type, 0)
		elif tile == 'X':
			self.image.fill((15, 15, 13))

	def palette_swap(self, surf, old_c, new_c):
		img_copy = pygame.Surface(surf.get_size())
		img_copy.fill(new_c)
		surf.set_colorkey(old_c)
		img_copy.blit(surf, (0, 0))
		return img_copy

	def flip(self, dir1, dir2, tile_type, angle):
		self.image = pygame.image.load('../graphics/tiles/' + self.tile_type + '.png')

		self.image = pygame.transform.scale(self.image, (64, 64))
		self.image = pygame.transform.flip(self.image, dir1, dir2)
		self.image = pygame.transform.rotate(self.image, angle)

