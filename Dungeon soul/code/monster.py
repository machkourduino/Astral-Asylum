import pygame
from support import import_folder

class Monster(pygame.sprite.Sprite):
    def __init__(self, pos, surface, speed, color):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.8
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(midtop=pos)
        self.display_surface = surface
        self.difficulty = (speed/3) + 6
        self.rect.y -= 126
        self.status = 'idle'
        self.color = color

    def import_character_assets(self):
        character_path = '../graphics/monster/'
        self.animations = {'idle': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def palette_swap(self, surf, old_c, new_c):
        color_mask = pygame.mask.from_threshold(surf, old_c, threshold=(1, 1, 1, 255))
        color_change_surf = color_mask.to_surface(setcolor=new_c, unsetcolor=(0, 0, 0, 0))
        img_copy = surf.copy()
        img_copy.blit(color_change_surf, (0, 0))
        return img_copy

    def animate(self):
        size = 3.6
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        image = self.palette_swap(image, (255, 148, 66), self.color[0])
        image = self.palette_swap(image, (50, 66, 66), self.color[1])
        image = pygame.transform.scale(image, (size * 18, size * 88))
        self.image = image

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift
        if self.difficulty <= 15:
            if self.difficulty >= 9:
                self.rect.x += 9
            else:
                self.rect.x += self.difficulty
        else:
            self.rect.x += 11
            self.image.fill((100, 100, 100), special_flags=pygame.BLEND_RGB_ADD)
