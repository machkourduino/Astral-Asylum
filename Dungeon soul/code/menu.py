import pygame
from support import import_folder

class Menu(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.5
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect()
        self.display_surface = surface
        # enemy status
        self.status = 'idle'

    def import_character_assets(self):
        character_path = '../graphics/menu/'
        self.animations = {'idle': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        size = 2.5
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 1

        image = animation[int(self.frame_index)]
        image = pygame.transform.scale(image, (1200 ,1175))
        self.image = image

        logo = pygame.image.load("../graphics/logo_1.png")
        self.image.blit(pygame.transform.scale(logo, (128 *size, 60*size)), (442, 20))

    def update(self):
        self.animate()