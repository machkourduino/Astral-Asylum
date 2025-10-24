import pygame

class Lives(pygame.sprite.Sprite):
    def __init__(self, filled, x_shift, color):
        super().__init__()
        self.size = 4
        if filled == False:
            self.image = pygame.image.load("../graphics/lives/empty.png")
        else:
            self.image = pygame.image.load("../graphics/lives/fill.png")

        self.image = self.palette_swap(self.image, (255, 148, 66), color[0])
        self.image = self.palette_swap(self.image, (50, 66, 66), color[1])
        self.image = pygame.transform.scale(self.image, (self.size * 20, self.size * 7))
        self.rect = self.image.get_rect()
        self.rect.topleft = (40 + (68*x_shift), 40)


    def palette_swap(self, surf, old_c, new_c):
        color_mask = pygame.mask.from_threshold(surf, old_c, threshold=(1, 1, 1, 255))
        color_change_surf = color_mask.to_surface(setcolor=new_c, unsetcolor=(0, 0, 0, 0))
        img_copy = surf.copy()
        img_copy.blit(color_change_surf, (0, 0))
        return img_copy


    def update(self):
        pass


