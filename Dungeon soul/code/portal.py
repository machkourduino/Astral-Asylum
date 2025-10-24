import pygame
from support import import_folder

class Portal(pygame.sprite.Sprite):
    def __init__(self, pos, surface, color):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(midtop=pos)
        self.display_surface = surface
        self.rect.y -= 128
        # enemy status
        self.status = 'idle'
        self.color = color

    def import_character_assets(self):
        character_path = '../graphics/portal/'
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
        image = pygame.transform.scale(image, (size * 16, size * 89))

        self.image = image


    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift
