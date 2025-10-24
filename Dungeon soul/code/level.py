import pygame 
from tiles import Tile
from player import Player
from particles import ParticleEffect
from enemy import Enemy
from monster import Monster
from portal import Portal
from text import Text
from debris import Debris
from transition import Transition
from menu import Menu
import math
import random
import pygame.gfxdraw
import os



tile_size = 64
screen_width = 1200
screen_height = 700

pygame.mixer.init()
pygame.mixer.music.load("../game_music.mp3")
pygame.mixer.music.set_volume(0.14)
volume = 0.05



class Level:
	def __init__(self,surface):

		# level setup
		self.display_surface = surface
		self.tutorial = 1
		self.star_list = []
		self.star_pos = 0
		self.tick = 0
		self.menu_music = pygame.mixer.Sound("../menu.mp3")
		self.menu_music.set_volume(0.07)
		# pygame.mixer.music.load("../game_music (mp3cut.net).mp3")


		for i in range(60):
			self.star_list.append([random.randint(0, 120)*10, abs(random.randint(-2, 5)), random.randint(0, 2000)])
		self.transparent_val = 0
		self.pause = True
		self.world_shift = 100
		self.eye_x = 0
		self.y_shift = 0
		self.current_x = 0
		self.difficulty = 0
		self.rate = 2
		self.primary_palette = [(255, 148, 66), (255, 148, 66), (253, 15, 25),(253, 15, 25), (249, 4, 99),(249, 4, 99), (0, 178, 68), (0, 178, 68)]
		self.secondary_palette = [(50, 66, 66), (50, 66, 66), (0, 67, 85), (0, 67, 85), (54, 7, 139), (54, 7, 139), (77, 4, 83), (77, 4, 83)]

		if self.tutorial == True:
			if self.difficulty > 1:
				self.shuffle_map()
			else:

				self.level_data = [
					'6------------------7',
					'LXXXXXXXXXXXXXXXXXXI',
					'9__________________8',
					'M                  O',
					'M                  O',
					'M                  O',
					'M                  O',
					'M        P         O',
					'6------------------7',
					'LXXXXXXXXXXXXXXXXXXI',
					'9__________________8']
		else:
			self.shuffle_map()
		self.transition = pygame.sprite.Group()
		if self.tutorial == True and self.difficulty == 0:
			self.transition.add(Transition([400, 230], self.display_surface, 'tutorial'))

		self.reset_level(self.level_data)
		self.velocity = 1
		self.cooldown_bar_val = 50
		self.cooldown = 0
		self.max_lives = 4
		self.time_since_level = 0
		self.score = 0
		self.debris = pygame.sprite.Group()
		self.menu = pygame.sprite.GroupSingle()
		self.menu.add(Menu(self.display_surface))

		if os.path.exists("../code/highscore.txt"):
			with open("../code/highscore.txt", 'r') as file:
				self.high_score = int(file.read())
		else:
			self.high_score = 0


		# dust
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False
		self.dash = False
		self.lives = 5
		self.hit = False
		self.time_since_death = 0
		self.dead_value = 0
		self.clock = pygame.time.Clock()
		self.time_since_dash = 0
		self.score_update()
		self.time_since_bruh = 0
		self.particle_list = []
		self.speed = 10
		self.text = pygame.sprite.Group()
		self.text_list = []
		b = 255
		self.text_list.append(Text("HIGHEST " + str(self.high_score), 32, (b, b, b),
								   (598, 335), 6))
		self.text_list.append(Text("PRESS  ENTER  TO  PLAY", 15, (b, b, b),
								   (600, 395), 6))
		self.text.add(self.text_list)

		#sounds
		self.hit_sound = pygame.mixer.Sound('../hit.wav')
		self.hit_sound.set_volume(0.14)

		self.portal_sound = pygame.mixer.Sound('../portal.wav')
		self.portal_sound.set_volume(0.07)

		self.volume = volume






	def create_jump_particles(self,pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		jump_particle_sprite = ParticleEffect(pos,'jump')
		self.dust_sprite.add(jump_particle_sprite)

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-10,15)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
			self.dust_sprite.add(fall_dust_particle)

	def shuffle_colors(self, color_choice, color_step):

		#self.primary_palette = [(255, 148, 66), (253, 15, 25), (249, 4, 99), (0, 178, 68)]
		#self.secondary_palette = [(50, 66, 66), (0, 67, 85), (54, 7, 139), (77, 4, 83)]
		#round
		primary_list = []
		for i in range(3):
			if self.primary_palette[color_choice][i] >= self.primary_palette[color_choice-1][i]:
				primary_list.append(self.primary_palette[color_choice][i] - (abs(
					self.primary_palette[color_choice][i] - self.primary_palette[color_choice-1][i])/6)*color_step)
			else:
				primary_list.append(self.primary_palette[color_choice][i] + (abs(
					self.primary_palette[color_choice][i] - self.primary_palette[color_choice - 1][
						i]) / 6) * (6 - color_step))

		secondary_list = []
		for i in range(3):
			if self.secondary_palette[color_choice][i] >= self.secondary_palette[color_choice - 1][i]:
				secondary_list.append(self.secondary_palette[color_choice][i] - (abs(
					self.secondary_palette[color_choice][i] - self.secondary_palette[color_choice - 1][
						i]) / 6) * color_step)
			else:
				secondary_list.append(self.secondary_palette[color_choice][i] + (abs(
					self.secondary_palette[color_choice][i] - self.secondary_palette[color_choice - 1][
						i]) / 6) * (6 - color_step))

		return [tuple(primary_list), tuple(secondary_list)]

	def reset_level(self, layout):
		self.difficulty += self.rate-1
		self.volume = volume
		self.current_palette = self.shuffle_colors(random.randint(0,len(self.primary_palette)-1), random.randint(0, 6))
		self.tiles = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()
		self.enemy = pygame.sprite.Group()
		self.monster = pygame.sprite.Group()
		self.portal = pygame.sprite.Group()
		for row_index, row in enumerate(layout):
			for col_index, cell in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size

				if cell == 'P':
					player_sprite = Player((x, y), self.display_surface, self.create_jump_particles, round(self.difficulty/4), self.current_palette)
					self.player.add(player_sprite)
				elif cell == 'E':
					self.type = random.randint(0, 1)
					# + (random.randint(-(row_index - 3), 4 - (row_index - 3)
					enemy_sprite = Enemy((x, y), self.display_surface, round(self.difficulty/4), self.type, self.current_palette)
					self.enemy.add(enemy_sprite)
				elif cell == "M":
					monster_sprite = Monster((x, y - ((row_index - 5) * 64)), self.display_surface, round(self.difficulty/4), self.current_palette)
					self.monster.add(monster_sprite)
				elif cell == "O":
					portal_sprite = Portal((x, y - ((row_index - 5) * 64)), self.display_surface, self.current_palette)
					self.portal.add(portal_sprite)
				elif str.isspace(cell) == False:
					tile = Tile((x, y), tile_size, cell, self.current_palette)
					self.tiles.add(tile)

	def cooldown_bar(self):
		if self.cooldown <= 0:
			pygame.draw.rect(self.display_surface, (254, 254, 218), (40, 75, 300, 10))
		else:
			pygame.draw.rect(self.display_surface, self.current_palette[1], (40, 75, 300, 10))
		pygame.draw.rect(self.display_surface, self.current_palette[0], (40, 75, self.cooldown * (300/self.cooldown_bar_val), 10))

	def int_to_roman(self, num):
		val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
		syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]

		roman_numeral = ''
		for i in range(len(val)):
			count = num // val[i]
			num %= val[i]
			roman_numeral += syms[i] * count

		return roman_numeral

	def score_update(self):
		self.text = pygame.sprite.Group()
		self.text.add(Text("SOUL" + str(self.score + 1), 32, (254, 254, 218), (85, 100), 1))
		self.text.add(Text(self.int_to_roman(self.score + 1), 500, (254, 254, 218), (30, 350), 5))

	def spawn_debris(self, type):
		self.debris = pygame.sprite.Group()
		player = self.player.sprite

		if type == 'dash':
			self.particle_list.append(Debris([player.rect.x, player.rect.y], type, self.display_surface, 0, self.current_palette[0]))
		if type == 'dash2':
			self.particle_list.append(Debris([player.rect.x, player.rect.y], type, self.display_surface, 0, self.current_palette[0]))
		if type == 'death':
			self.particle_list.append(Debris([player.rect.x, player.rect.y], type, self.display_surface, 0, self.current_palette[0]))

		self.debris.add(self.particle_list)

	def explosion(self):
		self.hit_sound.play()
		self.spawn_debris('death')

	def get_input(self):
		keys = pygame.key.get_pressed()
		self.cooldown -= 1

		if keys[pygame.K_RETURN]:
			pygame.mixer.music.play(-1)

		if keys[pygame.K_SPACE] and self.cooldown <= 0:
			self.dash = True
			self.cooldown = self.cooldown_bar_val
			self.spawn_debris('dash')

		if self.dash == True:
			self.time_since_dash += 100
			if self.time_since_dash >= 500:
				self.spawn_debris('dash2')
				self.dash = False
				self.world_shift -= 250
				self.time_since_dash = 0

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 2 and direction_x < 0:
			self.world_shift = self.speed
			player.speed = 0
		elif player_x > screen_width / 2 and direction_x > 0:
			self.world_shift = -self.speed
			player.speed = 0
		else:
			player.speed = self.speed
			self.world_shift = 0

	def death(self):
		if self.lives <= 0:
			if self.time_since_death <= 2:
				self.explosion()
			self.time_since_death += 1
		elif self.time_since_death >= 50:
			self.hit = False
			self.time_since_death = 0
			self.dead_value = 0


		elif self.time_since_death < 50:
			self.hit = True
			self.time_since_death += 1

	def death_delay(self):
		if self.lives > 0:
			self.player.update(self.lives, self.hit, self.max_lives)
			self.player.draw(self.display_surface)
			if self.time_since_level >= 0 and self.time_since_level <= 14 and self.difficulty > 3:
				white = round(357 - self.time_since_level * 25.5)
				if white >= 255:
					white = 255
				pygame.gfxdraw.box(self.display_surface, [0, 0, 2000, 800], (self.current_palette[1][0] + (255-round(max(self.current_palette[1])))- 2, self.current_palette[1][1]+ (255-round(max(self.current_palette[1])))- 2, self.current_palette[1][2]+ (255-round(max(self.current_palette[1]))) - 2, white))
		else:

			keys = pygame.key.get_pressed()
			if keys[pygame.K_RETURN]:

				#reset

				self.text.empty()
				self.score_update()
				self.lives = 3
				self.max_lives = 4
				self.difficulty = 1
				self.score = 1
				self.debris.empty()
				self.particle_list.clear()
				self.level_data = [
					'                    ',
					'                    ',
					'                    ',
					'                   O',
					'                   O',
					'                  PO',
					'                   O',
					'                   O',
					'                    ',
					'                    ',
					'                    ']





				self.reset_level(self.level_data)
				self.player.sprite.rect.x += 200
				self.reset_level(self.level_data)
				self.player.sprite.rect.x += 200


			else:

				self.volume = 0.05
				if self.score > self.high_score:
					self.high_score = self.score
					with open('../code/highscore.txt', 'w') as file:
						file.write(str(self.high_score))
				self.world_shift = -1
				self.time_since_bruh += 1
				pygame.gfxdraw.box(self.display_surface, [0, 0, 2000, 800], (15, 15, 13, 150))
				self.text = pygame.sprite.Group()
				self.text.add(
					Text("   Press  enter  to  play  again", 48, (254, 254, 218),
						 (625, 435 + math.sin(self.time_since_bruh / 8) * 50), 1))
				if self.score != 1:
					self.text.add(
						Text(str(self.score) + " SOULS", 48, (254, 254, 218),
							 (625, 330 + math.sin(self.time_since_bruh / 8) * 50), 1))
				else:
					self.text.add(
						Text("1 SOUL", 48, (254, 254, 218),
							 (625, 330 + math.sin(self.time_since_bruh / 8) * 50), 1))

				self.text.add(
					Text("HIGHSCORE       " + str(self.high_score), 48, (254, 254, 218),
						 (625, 365 + math.sin(self.time_since_bruh / 8) * 50), 1))


	def bullet_collision(self):
		player = self.player.sprite
		for sprite in self.enemy:
			for bullet in sprite.bullet_return():
				if bullet.rect.colliderect(player.rect):

					bullet.kill()

					if self.dead_value == 0:
						self.hit_sound.play()
						self.lives -= 1
						self.time_since_death = 0
						self.dead_value = 1
			for lazer in sprite.lazer_return():
				if lazer.rect.colliderect(player.rect):
					if self.dead_value == 0:
						self.lives = 0
						self.dead_value = 1

		if self.dead_value == 1:
			self.death()

	def monster_collision(self):
		player = self.player.sprite
		for sprite in self.monster:
			if player.rect.left <= sprite.rect.right +45:
				self.explosion()
				self.lives = 0

		self.time_since_level += 1

		if self.time_since_level >= 1 and self.time_since_level <= 5:
			self.lives = self.max_lives



		if self.time_since_level == 2:
			self.score += 1

	def portal_collision(self):
		if self.difficulty > self.rate:
			self.transition.empty()
		if self.max_lives >= 3:
			self.max_lives = 3

		enemy = self.enemy.sprites()
		player = self.player.sprite
		for sprite in self.portal:
			if player.rect.right >= sprite.rect.left +16:


				self.time_since_level = 0
				self.score_update()
				self.shuffle_map()

				self.reset_level(self.level_data)
				if self.tutorial == True:
					if self.difficulty >= 8:
						if self.lives == self.max_lives:
							self.max_lives += 1

						else:
							self.max_lives -= 1
					else:
						self.score = 0
						self.max_lives = 4
						self.lives = 1
				else:
					if self.lives == self.max_lives:
						self.max_lives += 1

					else:
						self.max_lives -= 1
				self.speed = self.max_lives*1.6 + 9
				if self.max_lives <= 1:
					self.max_lives = 1

				if self.speed >= 14:
					self.speed = 14

				self.cooldown = 0
				self.portal_sound.play()
			for i in enemy:
				if i.rect.right >= sprite.rect.left - 32:
					i.kill()

				#fade out into next level

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False

	def shuffle_map(self):

		enemy_list = []
		enemies = []
		enemy_count = 13
		space = 52
		radius = round(15 - self.difficulty/12)

		if radius <= 5:
			radius = 5
		#minimum 4

		for i in range(enemy_count):
			enemies.append(random.randint(10, space))

		enemies.insert(0, random.randint(17, 19))

		sorted_numbers = sorted(enemies)
		adjusted_numbers = [sorted_numbers[0]]

		for i in range(1, len(sorted_numbers)):
			prev_adjusted = adjusted_numbers[-1]
			diff = sorted_numbers[i] - prev_adjusted

			if diff >= 5:
				adjusted_numbers.append(sorted_numbers[i])
			else:
				adjusted_numbers.append(prev_adjusted + radius)
		index = -1
		for i in range(len(adjusted_numbers)):
			index += 1
			if adjusted_numbers[index] > space:
				del adjusted_numbers[index]
				index -= 1


		for i in range(len(adjusted_numbers)):
			enemy_list.insert(i, (adjusted_numbers[i], random.randint(3, 7)))


		empty_level_map = [
			'6--------------------------------------------------------------7',
			'LXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXI',
			'9______________________________________________________________8',
			'M                                                              O',
			'M                                                              O',
			'M                                                              O',
			'M                                                              O',
			'M        P                                                     O',
			'6--------------------------------------------------------------7',
			'LXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXI',
			'9______________________________________________________________8']


		self.level_data = []
		index = 0
		for line in empty_level_map:
			line = list(line)
			for j in enemy_list:
				if j[1] == index:
					if not ('P' in line and (j[0] == 10 or j[0] == 9)):
						del line[j[0]-1]
						line.insert(j[0], 'E')
			self.level_data.append("".join(line))
			index += 1

	def draw_stars(self):
		self.star_pos -= 20
		if self.star_pos <= 0:
			self.star_pos = 690
		for i in self.star_list:
			pygame.draw.rect(self.display_surface, (254, 254, 218), (i[0], i[2]-self.star_pos, i[1], i[1]))
			pygame.draw.rect(self.display_surface, (254, 254, 218), (i[0], i[2] - self.star_pos+690, i[1], i[1]))

	def draw_stars_horizantal(self):
		self.star_pos += 20
		if self.star_pos >= 2000:
			self.star_pos = 0
		for i in self.star_list:
			pygame.draw.rect(self.display_surface, (254, 254, 218), (i[2]-self.star_pos, i[0], 1, 1))
			pygame.draw.rect(self.display_surface, (254, 254, 218), (i[2] - self.star_pos+2000, i[0], 1, 1))



	def run(self, pause, menu):

		# dust particles

		if menu == False:
			self.menu_music.stop()
			self.text_list[0].rect.y = 800
			self.text_list[1].rect.y = 800
			if pause == False:
				pygame.mixer.music.set_volume(self.volume)
				pygame.draw.rect(self.display_surface, (15, 15, 13), [0, 0, 2000, 800])
				self.draw_stars_horizantal()
				self.eye_x += self.world_shift
				pygame.draw.ellipse(self.display_surface, (0, 0, 0), [self.eye_x-5200, 350, 160, 80])
				pygame.draw.ellipse(self.display_surface, (255, 255, 255), [self.eye_x - 5155, 355, 70, 70])
				pygame.draw.ellipse(self.display_surface, (0, 0, 0), [self.eye_x - 5450, 350, 160, 80])
				pygame.draw.ellipse(self.display_surface, (255, 255, 255), [self.eye_x - 5405, 355, 70, 70])

				self.text.add(
					Text("p    mlls    lclyf    zpunsl    vul", 48, (255, 255, 255),
						 (self.eye_x - 5220, 500), 6))

				self.monster.update(self.world_shift)
				self.monster.draw(self.display_surface)
				self.transition.draw(self.display_surface)
				self.transition.update(self.world_shift)
				self.dust_sprite.update(self.world_shift)
				self.dust_sprite.draw(self.display_surface)
				self.debris.update(self.world_shift)
				# portal
				self.portal.update(self.world_shift)
				self.portal.draw(self.display_surface)

				# monster
				self.enemy.update(self.world_shift)
				self.enemy.draw(self.display_surface)

				# level tiles
				self.tiles.update(self.world_shift, self.y_shift)
				self.tiles.draw(self.display_surface)




				self.horizontal_movement_collision()
				self.get_player_on_ground()
				self.vertical_movement_collision()
				self.create_landing_dust()



				self.scroll_x()
				if self.lives != 0:
					self.portal_collision()
					self.bullet_collision()
					if self.difficulty > self.rate:
						self.monster_collision()
					self.get_input()
					self.cooldown_bar()



				self.death_delay()
				self.transparent_val = 0
				self.text.update(self.world_shift)
				self.text.draw(self.display_surface)
			else:
				if self.lives != 0:
					if self.transparent_val == 0:
						pygame.mixer.music.set_volume(0)
						pygame.gfxdraw.box(self.display_surface, [0, 0, 2000, 800], (15, 15, 13, 150))
						pygame.draw.rect(self.display_surface, (254, 254, 218), [screen_width / 2 - 20, screen_height / 2 - 50, 20, 100])
						pygame.draw.rect(self.display_surface, (254, 254, 218), [screen_width / 2 + 20, screen_height / 2 - 50, 20, 100])

					self.transparent_val += 1
				else:
					pygame.mixer.music.set_volume(self.volume)
					pygame.draw.rect(self.display_surface, (15, 15, 13), [0, 0, 1200, 700])
					self.draw_stars_horizantal()
					self.monster.update(self.world_shift)
					self.monster.draw(self.display_surface)
					self.dust_sprite.update(self.world_shift)
					self.dust_sprite.draw(self.display_surface)
					self.debris.update(self.world_shift)
					# portal
					self.portal.update(self.world_shift)
					self.portal.draw(self.display_surface)
					# monster

					self.enemy.update(self.world_shift)
					self.enemy.draw(self.display_surface)

					# level tiles
					self.tiles.update(self.world_shift, self.y_shift)
					self.tiles.draw(self.display_surface)




					self.horizontal_movement_collision()
					self.get_player_on_ground()
					self.vertical_movement_collision()
					self.create_landing_dust()
					self.transition.draw(self.display_surface)
					self.transition.update(self.world_shift)


					self.scroll_x()
					if self.lives != 0:
						self.portal_collision()
						self.bullet_collision()
						if self.difficulty > self.rate:
							self.monster_collision()
						self.get_input()
						self.cooldown_bar()



					self.death_delay()
					self.transparent_val = 0
					self.text.update(self.world_shift)
					self.text.draw(self.display_surface)
		else:
			self.menu_music.play(-1)
			self.tick += 1
			pygame.draw.rect(self.display_surface, (15, 15, 13), [0, 0, 2000, 800])
			self.draw_stars()
			self.menu.update()
			self.menu.draw(self.display_surface)







			self.text.update(0)

			self.text.draw(self.display_surface)





			#menu class animation with press enter to play
			# write high score



			#quit




