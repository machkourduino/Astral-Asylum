import pygame
screen_width = 1200
screen_height = 700

class Lazer(pygame.sprite.Sprite):
    def __init__(self, pos, shift, angle, color):
        super().__init__()
        self.image = pygame.image.load("../graphics/lazer.png")
        self.image = self.palette_swap(self.image, (255, 148, 66), color[0])
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.image = pygame.transform.rotate(self.image, angle - 90)
        self.rect = self.image.get_rect(center=pos)
        if angle == 0:
            self.rect.x += 28
            self.rect.y += 32
        else:
            self.rect.x += 44.5
            self.rect.y += 44.5
        self.shift = shift
        self.color = color

    def palette_swap(self, surf, old_c, new_c):
        color_mask = pygame.mask.from_threshold(surf, old_c, threshold=(1, 1, 1, 255))
        color_change_surf = color_mask.to_surface(setcolor=new_c, unsetcolor=(0, 0, 0, 0))
        img_copy = surf.copy()
        img_copy.blit(color_change_surf, (0, 0))
        return img_copy

    def update(self, x_shift):

        self.rect.x += x_shift
        self.rect.x += self.shift