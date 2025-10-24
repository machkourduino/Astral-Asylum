import pygame


class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, pos, type):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.font = pygame.font.Font("../ARCADECLASSIC.TTF", size)
        self.text = text
        if type == 5:
            self.textSurf = self.font.render(("    " * (len(self.text)) + self.text), 1, color)
            self.textSurf.set_alpha(150)
        else:
            self.textSurf = self.font.render(self.text, 1, color)
        self.image = self.textSurf
        if type == 5:
            self.image = pygame.transform.scale(self.image, (353, 506))
        self.rect = self.image.get_rect(center = pos)

    def update(self, x_shift):
        if self.type == 5 or self.type == 6:
            self.rect.x += x_shift
