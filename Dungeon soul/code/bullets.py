import pygame
from pygame.math import Vector2
screen_width = 1200
screen_height = 700

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, shift, color):
        super().__init__()
        self.image = pygame.image.load("../graphics/bullet.png")
        self.image = self.palette_swap(self.image, (255, 148, 66), color)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(center=pos)
        self.speed = 6
        self.shift = shift
        offset = Vector2(20, 0).rotate(angle)
        self.pos = Vector2(pos) + offset
        self.velocity = Vector2(1, 0).rotate(angle) * self.speed
        self.color = color

    def palette_swap(self, surf, old_c, new_c):
        color_mask = pygame.mask.from_threshold(surf, old_c, threshold=(1, 1, 1, 255))
        color_change_surf = color_mask.to_surface(setcolor=new_c, unsetcolor=(0, 0, 0, 0))
        img_copy = surf.copy()
        img_copy.blit(color_change_surf, (0, 0))
        return img_copy

    def update(self, x_shift):
        self.pos += self.velocity
        self.rect.center = self.pos[0] +32, self.pos[1]+32
        if self.rect.x > screen_width or self.rect.x < 0 or self.rect.y > screen_height or self.rect.y < 0:
            self.kill()
        self.pos[0] += x_shift
        self.pos[0] += self.shift


