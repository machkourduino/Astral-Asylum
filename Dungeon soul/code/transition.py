import pygame
from support import import_folder
import pygame.gfxdraw

class Transition(pygame.sprite.Sprite):
    def __init__(self, pos, surface, type):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.8
        self.image = self.animations[type][self.frame_index].convert()
        self.rect = self.image.get_rect(center = pos)
        self.display_surface = surface
        self.type = type
        # enemy status
        self.status = self.type
        self.trans_rect = 0
        self.time_since_alive = 0

    def import_character_assets(self):
        character_path = '../graphics/transition/'
        self.animations = {'plus': [], 'minus': [], 'tutorial': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def return_frame_index(self):
        return self.frame_index

    def animate(self, x_shift):
        size = 5
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]

        if self.type == 'tutorial':
            image = pygame.transform.scale(image, (136 *size, 57*size))
            self.trans_rect += x_shift
            pygame.gfxdraw.box(self.display_surface, [0 + self.trans_rect/2, 100, 136 * size *10, 57 * size*2], (15, 15, 13, 150))
        else:
            image = pygame.transform.scale(image, (1200, 1200))
        self.image = image

    def update(self, x_shift):

        self.animate(x_shift)
        if self.status == 'tutorial':
            self.rect.x += x_shift/2

