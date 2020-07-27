# --- libraries ---
import time

import pygame

import source.classes.titans as titans  # source/titans.py
import source.classes.tools as tools  # source/tools.py

pygame.init()  # pygame initialization


def get_nearest(actual, matrix):
    for i in range(8, -1, -1):
        element = matrix[actual][i]
        if element.object:
            if element and titans.Titan.__subclasscheck__(element.object.__class__):
                return element
    return None


class Elemental:
    def __init__(self, info, path, matrix):
        self.health, self.attack_power, self.attack_freq = info[0], info[1], matrix.game.attack_freq
        self.matrix = matrix
        self.initial_time = 0
        self.section = None
        self.pos = ()
        self.screen = self.matrix.screen
        self.image = pygame.image.load(path)
        self.projectiles = []
        self.projectile_path = ""

    def attack(self):
        if 0 < (time.time() - self.initial_time) % (6 - (6 * self.attack_freq)) < 0.05:
            temp = get_nearest(self.section.id[0], self.matrix.sections)
            if temp:
                self.projectiles.append(Projectile(self.screen, self.projectile_path, self, temp.object))
                print("✷ Elemental attack", temp.id, "✷")  # notification

    def hurt(self, damage):
        tools.sounds("source/resources/gui/sounds/hurt.wav", 0.1)
        self.health -= damage

    def die(self):
        return

    def update(self):
        for projectile in self.projectiles:
            projectile.update()
        if self.health <= 0:
            self.die()
        else:
            self.screen.blit(self.image, (self.pos[0] - 6.5, self.pos[1] - 18))


class Air(Elemental):
    def __init__(self, info, path, matrix):
        super().__init__(info, path, matrix)
        self.projectile_path = "source/resources/gui/sprites/att_e_air.png"
        self.air_sprite = tools.Sprites("source/resources/gui/sprites/e_air.png", 17, 1)

    def die(self):
        for index in range(8, 16):
            self.air_sprite.animation(self.screen, index, self.pos[0], self.pos[1], 4)
        tools.gameClock.tick(30)
        self.section.object = None


class Earth(Elemental):
    def __init__(self, info, path, matrix):
        super().__init__(info, path, matrix)
        self.projectile_path = "source/resources/gui/sprites/att_e_earth.png"

    def die(self):
        self.section.object = None


class Water(Elemental):
    def __init__(self, info, path, matrix):
        super().__init__(info, path, matrix)
        self.projectile_path = "source/resources/gui/sprites/att_e_water.png"

    def die(self):
        self.section.object = None


class Fire(Elemental):
    def __init__(self, info, path, matrix):
        super().__init__(info, path, matrix)
        self.projectile_path = "source/resources/gui/sprites/att_e_fire.png"

    def die(self):
        self.section.object = None


class Projectile:
    def __init__(self, screen, path, elemental, titan):
        self.screen = screen
        self.image = pygame.image.load(path)
        self.elemental = elemental
        self.pos = self.elemental.section.pos
        self.titan = titan

    def update(self):
        self.pos = (self.pos[0], self.pos[1] - 3)
        self.screen.blit(self.image, self.pos)
        if self.pos[1] <= self.titan.pos[1]:
            if self.titan.health > 0:
                self.titan.hurt(self.elemental.attack_power)
            self.elemental.projectiles.remove(self)
        if self.pos[1] < -51:
            self.elemental.projectiles.remove(self)
