import pygame 
from support import import_folder
from lives import Lives

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,surface,create_jump_particles, difficulty, color):
		super().__init__()
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		self.color = color
		
		# dust particles 
		self.import_dust_run_particles()
		self.dust_frame_index = 0
		self.dust_animation_speed = 0.3
		self.display_surface = surface
		self.create_jump_particles = create_jump_particles
		self.clock = pygame.time.Clock()
		self.time_since_dash = 0
		self.difficulty = difficulty

		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 16
		self.jump_speed = -9
		self.gravity = -self.jump_speed/15
		self.cooldown_bar_val = 50
		self.cooldown = 0
		self.dash = False
		self.dash_reverse = False


		# player status
		self.status = 'idle'
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False

		#lives
		self.lives = pygame.sprite.Group()
		self.dead_value = 0
		self.lives_left = 0
		self.max_lives = 0
		# self.dash_sound = pygame.mixer.Sound('../dash.wav')
		self.jump_sound = pygame.mixer.Sound('../jump.wav')
		self.jump_sound.set_volume(0.9)
		self.dash_sound = pygame.mixer.Sound('../dash.wav')
		self.dash_sound.set_volume(0.84)

		self.alive = True
		self.brighten = 0

	def import_character_assets(self):
		character_path = '../graphics/character/'
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'dash':[],'dash_reverse':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def import_dust_run_particles(self):
		self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')

	def palette_swap(self, surf, old_c, new_c):
		color_mask = pygame.mask.from_threshold(surf, old_c, threshold=(1, 1, 1, 255))
		color_change_surf = color_mask.to_surface(setcolor=new_c, unsetcolor=(0, 0, 0, 0))
		img_copy = surf.copy()
		img_copy.blit(color_change_surf, (0, 0))
		return img_copy

	def animate(self):
		self.size = 5 - (self.difficulty/6)
		if self.size >= 4:
			self.size = 4
		if self.size <= 1:
			self.size = 1
		animation = self.animations[self.status]

		# loop over frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
		image = animation[int(self.frame_index)]


		image = self.palette_swap(image, (255, 148, 66), self.color[0])


		image = pygame.transform.scale(image, (11*self.size, 16*self.size))
		if self.facing_right:
			self.image = image
		else:
			flipped_image = pygame.transform.flip(image,True,False)
			self.image = flipped_image



		# set the rect
		if self.on_ground and self.on_right:
			self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
		elif self.on_ground and self.on_left:
			self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		elif self.on_ground:
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		elif self.on_ceiling and self.on_right:
			self.rect = self.image.get_rect(topright = self.rect.topright)
		elif self.on_ceiling and self.on_left:
			self.rect = self.image.get_rect(topleft = self.rect.topleft)
		elif self.on_ceiling:
			self.rect = self.image.get_rect(midtop = self.rect.midtop)

	def dead_fade(self, hit):
		if hit == True:
			if pygame.time.get_ticks() == round(pygame.time.get_ticks()/2)*2:
				if self.brighten >= 120:
					self.pulse = False
				elif self.brighten <= 5:
					self.pulse = True

				if self.pulse == True:
					self.brighten += 20
				else:
					self.brighten -= 20
		else:
			self.brighten = 0
		self.image.fill((self.brighten, self.brighten, self.brighten), special_flags=pygame.BLEND_RGB_ADD)

	def run_dust_animation(self):
		if self.status == 'run' and self.on_ground:
			self.dust_frame_index += self.dust_animation_speed
			if self.dust_frame_index >= len(self.dust_run_particles):
				self.dust_frame_index = 0

			dust_particle = self.dust_run_particles[int(self.dust_frame_index)]
			dust_particle = pygame.transform.scale2x(dust_particle)

			if self.facing_right:
				pos = self.rect.bottomleft - pygame.math.Vector2(25,20)
				self.display_surface.blit(dust_particle,pos)
			else:
				pos = self.rect.bottomright - pygame.math.Vector2(0,20)
				flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
				self.display_surface.blit(flipped_dust_particle, pos)


	def get_input(self):
		keys = pygame.key.get_pressed()
		pygame.joystick.init()
		self.cooldown -= 1
		if keys[pygame.K_SPACE] and self.cooldown <= 0:
			self.dash_sound.play()
			self.frame_index = 0
			self.dash = True
			self.facing_right = True
			self.cooldown = self.cooldown_bar_val
		if self.dash == True:
			self.direction.x = 0
			self.direction.y = 0
			self.time_since_dash += 100
			if self.time_since_dash >= 500:
				self.dash = False
				self.time_since_dash = 0
				self.dash_reverse = True
		elif self.dash_reverse == True:
			self.direction.x = 0
			self.direction.y = 0
			self.time_since_dash += 100
			if self.time_since_dash >= 500:
				self.time_since_dash = 0
				self.dash_reverse = False

		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.facing_right = False
		elif keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.facing_right = True
		else:
			self.direction.x = 0

		if keys[pygame.K_UP] and self.on_ground:
			self.jump_sound.play()
			self.jump()
			self.create_jump_particles(self.rect.midbottom)


	def get_status(self):
		time = 1.2
		if self.dash == True:

			self.animation_speed = time
			self.status = 'dash'

		elif self.dash_reverse == True:

			self.animation_speed = time
			self.status = 'dash_reverse'

		else:
			self.animation_speed = 0.3
			if self.direction.y < 0:
				self.status = 'jump'
			elif self.direction.y > 1:
				self.status = 'fall'
			else:
				if self.direction.x != 0:
					self.status = 'run'
				else:
					self.status = 'idle'

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def jump(self):
		self.direction.y = self.jump_speed

	def update(self, lives, hit, max_lives):
		self.get_input()
		self.get_status()
		self.animate()
		self.dead_fade(hit)

		self.lives.empty()
		for i in range(max_lives+1):
			if lives > i:
				fill = True
			else:
				fill = False
			if len(self.lives) < max_lives:
				self.lives.add(Lives(fill, i, self.color))
		self.lives.update()
		self.lives.draw(self.display_surface)