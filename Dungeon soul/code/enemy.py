
from bullets import Bullet
from lazer import Lazer
import pygame
from support import import_folder
import random
from debris import Debris


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, surface, difficulty, type, color):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.3
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.display_surface = surface
        self.bullet_group = pygame.sprite.Group()
        self.lazer_group = pygame.sprite.Group()
        self.type = type
        self.interval = 2
        self.special_frequency = random.randint(2, 4)
        self.lazer_cooldown = 0
        self.special = False
        self.lazer = False
        self.time_since_lazer = 0
        self.debris = pygame.sprite.Group()
        self.particle_list = []
        self.color = color
        val_list = [-1, 1]
        self.val = random.choice(val_list)

        self.shoot_sound = pygame.mixer.Sound("..\shoot.wav")
        self.shoot_sound.set_volume(2)
        self.lazer_sound = pygame.mixer.Sound("..\lazer.mp3")
        self.lazer_sound.set_volume(0.34)

        self.difficulty = round(difficulty/3) + 1
        if self.difficulty >= 10:
            self.difficulty = 10

        self.bullets = random.randint(2 + round(difficulty / 2), 4 + round(difficulty / 2))

        if 15 - self.difficulty * 3 > 0:
            if random.randint(0, 15 - self.difficulty * 3) == 0 and self.difficulty >= 7:
                self.special = True
                if self.type == True:
                    self.movement = 4
                else:
                    self.movement = 0
            else:
                self.movement = 0
        else:
            self.special = True
            if self.type == True:
                self.movement = 4
            else:
                self.movement = 0

        if self.bullets >= 8:
            self.bullets = 8

        # enemy status
        self.status = 'idle'
        self.sec = 0
        if type == False:
            self.laser = False
            self.angle_list = [90]
        else:
            self.laser = True
            self.angle_list = [0, 45, 135]

        self.angle = random.choice(self.angle_list)
        self.clock = pygame.time.Clock()
        self.time_since_last_shot = 0
        self.special_cooldown = 0

    def import_character_assets(self):
        character_path = '../graphics/enemy/'
        self.animations = {'idle': [], 'shoot': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def bullet_return(self):
        return self.bullet_group

    def lazer_return(self):
        return self.lazer_group

    def palette_swap(self, surf, old_c, new_c):
        color_mask = pygame.mask.from_threshold(surf, old_c, threshold=(1, 1, 1, 255))
        color_change_surf = color_mask.to_surface(setcolor=new_c, unsetcolor=(0, 0, 0, 0))
        img_copy = surf.copy()
        img_copy.blit(color_change_surf, (0, 0))
        return img_copy

    def animate(self):
        size = 4
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        image = self.palette_swap(image, (255, 148, 66), self.color[0])
        image = self.palette_swap(image, (50, 66, 66), self.color[1])
        image = pygame.transform.scale(image, (size*16, size*16))

        if self.type == True:
            image = pygame.transform.rotate(image, self.angle - 90)
        else:
            image = pygame.transform.rotate(image, 0)

        self.image = image
        if self.movement != 0:
            self.particle_list.append(Debris([self.rect.x * 10 -5500, self.rect.y+34], 'enemy', self.display_surface, 0, self.color[0]))
            self.debris.add(self.particle_list)

    def shoot(self):
        if self.angle == 135 or self.angle == 45:
            rotational_offset = 13
        else:
            rotational_offset = 0
        if self.type == True:
            if self.lazer_cooldown == self.special_frequency - 2 and self.movement != 0:
                self.particle_list.append(Debris([self.rect.x * 10 +100, self.rect.y+10], 'bullet2', self.display_surface, self.movement, self.color[0]))
        else:
            if self.special_cooldown == self.special_frequency - 2 and self.special == True:
                self.particle_list.append(
                    Debris([self.rect.x * 10, self.rect.y], 'bullet2', self.display_surface, 0, self.color[0]))
        for i in range(self.bullets):
            self.angle += 360/self.bullets
            self.bullet_group.add(Bullet((self.rect.x + rotational_offset, self.rect.y + rotational_offset), self.angle - 90, self.movement, self.color[0]))
        for i in range(self.bullets):
            self.angle -= 360/self.bullets

        self.debris.add(self.particle_list)


    def shoot_cycle(self):
        self.status = 'idle'
        self.time_since_last_shot += 35
        if self.time_since_last_shot > (self.interval - 0.25)*1000:
            self.status = 'shoot'

        if self.time_since_last_shot >= self.interval*1000:
            #-123, 1270
            if self.rect.x > -123 and self.rect.x < 1270:
                self.shoot_sound.play()
            self.shoot()
            self.time_since_last_shot = 0
            if self.type == False and self.special == True:
                self.angle -= 30
                self.special_cooldown += 1
            else:
                self.shoot_sound.set_volume(0.2)
            if self.type == True and self.special == True:
                self.lazer_cooldown += 1

        if self.lazer_cooldown == self.special_frequency:
            if self.rect.x > -123 and self.rect.x < 1270:
                self.lazer_sound.play()
            x = 14
            if self.angle == 45:
                for i in range(35):
                    self.lazer_group.add(Lazer((self.rect.x + (i * x), self.rect.y + (i * x)), self.movement, self.angle, self.color))
                    self.lazer_group.add(Lazer((self.rect.x - (i * x), self.rect.y - (i * x)), self.movement, self.angle, self.color))
            elif self.angle == 135:
                for i in range(35):
                    self.lazer_group.add(Lazer((self.rect.x - (i * x), self.rect.y + (i * x)), self.movement, self.angle, self.color))
                    self.lazer_group.add(Lazer((self.rect.x + (i * x), self.rect.y - (i * x)), self.movement, self.angle, self.color))
            elif self.angle == 0:
                for i in range(15):
                    self.lazer_group.add(Lazer((self.rect.x, self.rect.y + (i*20)), self.movement, self.angle, self.color))
                    self.lazer_group.add(Lazer((self.rect.x, self.rect.y - (i * 20)), self.movement, self.angle, self.color))

            self.lazer_cooldown = 0
            self.lazer = True

        if self.lazer == True:
            self.time_since_lazer += 1
            if self.time_since_lazer < 30:
                self.status = 'shoot'
            else:
                self.lazer = False
                self.time_since_lazer = 0
                self.lazer_group.empty()

        if self.type == False:
            if self.special_cooldown == self.special_frequency:
                self.bullets = 1
                self.interval = 0.1

            if self.special_cooldown == 15:
                self.angle = 90
                self.interval = 2
                self.special_cooldown = 0
                self.bullets = random.randint(2 + round(self.difficulty/2), 4 + round(self.difficulty/2))

    def update(self, x_shift):
        self.debris.update(x_shift)
        self.rect.x += self.movement
        self.shoot_cycle()
        self.animate()
        self.rect.x += x_shift
        self.bullet_group.update(x_shift)
        self.bullet_group.draw(self.display_surface)
        self.lazer_group.update(x_shift)
        self.lazer_group.draw(self.display_surface)




