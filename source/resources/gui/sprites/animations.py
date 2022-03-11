import math, random, sys
import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 700))
pygame.display.set_caption("QALHALLA_animations")

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)


class Sprites:
    def __init__(self, path, cols, rows):
        self.sprite_sheet = pygame.image.load(path).convert_alpha()

        self.columns = cols
        self.rows = rows
        self.total_frames = cols * rows

        self.rect = self.sprite_sheet.get_rect()
        w = self.frame_width = int(self.rect.width / cols)
        h = self.frame_height = int(self.rect.height / rows)
        hw, hh = self.frame_middlepx = (int(w / 2), int(h / 2))

        self.sprite_sheet_list = list(
            [(index % cols * w, int(index // cols) * h, w, h) for index in range(self.total_frames)])
        self.handle = list([
            (0, 0), (-hw, 0), (-w, 0),
            (0, -hh), (-hw, -hh), (-w, -hh),
            (0, -h), (-hw, -h), (-w, -h), ])

    def animation(self, surface, frames, x, y, handle=0):
        surface.blit(self.sprite_sheet, (x + self.handle[handle][0], y + self.handle[handle][1]),
                     self.sprite_sheet_list[frames])


skeleton = Sprites("t_skeleton.png", 24, 1)
elf = Sprites("t_elf.png", 29, 1)
orc = Sprites("t_orc.png", 22, 1)
dragon = Sprites("t_dragon.png", 22, 1)
air = Sprites("e_air.png", 17, 1)
earth = Sprites("e_earth.png", 16, 1)
water = Sprites("e_water.png", 17, 1)
fire = Sprites("e_fire.png", 16, 1)

index = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    skeleton.animation(screen, index % skeleton.total_frames, 110, 110, 4)
    elf.animation(screen, index % elf.total_frames, 110, 210, 4)
    orc.animation(screen, index % orc.total_frames, 110, 310, 4)
    dragon.animation(screen, index % dragon.total_frames, 110, 410, 4)
    air.animation(screen, index % air.total_frames, 410, 110, 4)
    earth.animation(screen, index % earth.total_frames, 410, 210, 4)
    water.animation(screen, index % water.total_frames, 410, 310, 4)
    fire.animation(screen, index % fire.total_frames, 410, 410, 4)

    index += 1
    # print(index % elf.total_frames)

    pygame.display.update()
    clock.tick(7)
    screen.fill(WHITE)