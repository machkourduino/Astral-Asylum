import pygame, random

TILE_SIZE = 64

tile_map = {}
for i in range(200):
    tile_map[str(i-90) + ';8'] = [i, 8, (255, 0, 0)]


class Debris(pygame.sprite.Sprite):
    def __init__(self, pos, type, screen, movement, color):
        super().__init__()
        self.pos = pos
        self.screen = screen
        self.type = type
        self.index = 0
        self.particles = []
        self.movement = movement
        if type == 'dash':
            self.size_decrease = 0.3
            self.speed = 1
            self.y_speed = 1
            self.gravity = 0
            self.col = 0
            self.size = 5
            self.x_offset = 570
            self.y_offset = 0
            self.fix_x_shift = 10
            self.abs = 0
            self.amount = 30
            self.color = (254, 254, 218)
            self.shape = 0

        if type == 'dash2':
            self.size_decrease = 0.6
            self.speed = 2
            self.y_speed = 2
            self.gravity = 0
            self.size = 5
            self.col = 0
            self.x_offset = 550
            self.y_offset = 0
            self.fix_x_shift = 0
            self.abs = 0
            self.amount = 30
            self.color = (254, 254, 218)
            self.shape = 0
        if type == 'death':
            self.size_decrease = 0.03
            self.speed = 3
            self.y_speed = random.randint(0, 4000)/1000
            self.gravity = 0.3
            self.col = 1
            self.size = 5
            self.x_offset = 560
            self.y_offset = -5
            self.fix_x_shift = 10
            self.abs = 0
            self.amount = 300
            self.color = (254, 254, 218)
            self.shape = 0
        if type == 'enemy':
            self.size_decrease = 0.3
            self.speed = 1
            self.y_speed = 1
            self.gravity = 0
            self.col = 0
            self.size = 5
            self.x_offset = 565
            self.y_offset = 0
            self.fix_x_shift = 10
            self.abs = 0
            self.amount = 1
            self.color = (254, 254, 218)
            self.shape = 0
        if type == 'bullet2':
            self.size_decrease = 1.5
            self.speed = 0
            self.y_speed = 0
            self.gravity = 0
            self.col = 0
            self.size = 100
            self.x_offset = 34
            self.y_offset = 34
            self.fix_x_shift = 10
            self.abs = 0
            self.amount = 1
            self.color = color
            self.shape = 1

        if type == 'dash' or type == 'dash2' or type == 'death':
            for i in range(self.amount):
                self.particles.append(
                    [[pos[0] + random.randint(-10, 10), pos[1] + random.randint(0, 50)],
                     [random.randint(-25, 25) + random.randint(-25, 25)/100, random.randint(-2, 2) + random.randint(-2, 2)/100],
                     random.randint(self.size - 1, self.size + 1)])
        else:
            for i in range(self.amount):
                self.particles.append(
                    [[pos[0], pos[1]],
                     [random.randint(-25, 25) + random.randint(-25, 25)/100, random.randint(-2, 2) + random.randint(-2, 2)/100],
                     random.randint(self.size - 1, self.size + 1)])


    def render(self, x_shift):
        for particle in self.particles:
            particle[0][0] += particle[1][0] * self.speed + x_shift * self.fix_x_shift
            particle[0][1] += particle[1][1]*self.y_speed
            loc_str = str(int(particle[0][0] / TILE_SIZE)) + ';' + str(int(particle[0][1] / TILE_SIZE))

            if loc_str in tile_map and self.col == 1:
                particle[1][1] = -0.8 * particle[1][1]
                particle[1][0] *= 0.99
                particle[0][1] += particle[1][1] * 2
            particle[2] -= self.size_decrease
            particle[1][1] += self.gravity
            if self.shape == 0:
                pygame.draw.rect(self.screen, self.color, [int(particle[0][0])/10 + self.x_offset, int(particle[0][1]) + self.y_offset, int(particle[2]*2), int(particle[2]*2)])
            else:
                pygame.draw.circle(self.screen, self.color, [int(particle[0][0])/10 + self.x_offset, int(particle[0][1]) + self.y_offset], int(particle[2]*2), 1)
            if particle[2] <= 0:
                self.particles.remove(particle)

    def update(self, x_shift):
        self.render(x_shift)
        self.x_offset += self.movement


