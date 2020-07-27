# --- libraries ---
import time

import pygame

import source.classes.titans as titans  # source/titans.py
import source.classes.tools as tools  # source/tools.py

pygame.init()  # pygame initialization


def get_nearest(actual, matrix):
    # method, go through bottom-up of the matrix and check which is the closest character, in case the character is a
    # titan send element
    for i in range(8, -1, -1):
        element = matrix[actual][i]
        if element.object:
            if element and titans.Titan.__subclasscheck__(element.object.__class__):
                return element
    return None


class Elemental:
    # info[0]: health, info[1]: attack power, path: filepath, matrix: self
    def __init__(self, info, path, matrix):
        # superclass, sets up tributes and features of elemental character
        self.health = info[0]  # elemental's life amount
        self.attack_power = info[1]  # elemental's attack power amount
        self.attack_freq = matrix.game.attack_freq  # elemental's attack frequency
        self.projectile_path = ""  # attack img
        self.projectiles = []  #
        self.matrix = matrix
        self.section = None
        self.pos = ()
        self.screen = self.matrix.screen
        self.image = pygame.image.load(path)
        self.initial_time = 0

    def attack(self):
        # method, returns the projectile to the matrix section where the nearest titan is located, depending on the
        # frequency of attack chosen through the battle mode (difficulty)
        if 0 < (time.time() - self.initial_time) % (6 - (6 * self.attack_freq)) < 0.05:
            temp = get_nearest(self.section.id[0], self.matrix.sections)
            if temp:
                self.projectiles.append(Projectile(self.screen, self.projectile_path, self, temp.object))
                print("✷ Elemental attack", temp.id, "✷")  # notification

    def hurt(self, damage):
        # method, subtracts from the elemental's health the amount of the titan's attack power
        tools.sounds("source/resources/gui/sounds/hurt.wav", 0.1)  # plays hit sound
        self.health -= damage

    def die(self):
        return  # overridden

    def update(self):
        # method, event manager for the elemental class
        for projectile in self.projectiles:
            projectile.update()  # send attack
        if self.health <= 0:
            self.die()  # remove elemental
        else:
            self.screen.blit(self.image, (self.pos[0] - 6.5, self.pos[1] - 18))  # elemental img


class Air(Elemental):
    # subclass from Elemental superclass, sets the features of the air elemental
    def __init__(self, info, path, matrix):
        super().__init__(info, path, matrix)
        self.projectile_path = "source/resources/gui/sprites/att_e_air.png"  # attack img
        self.air_sprite = tools.Sprites("source/resources/gui/sprites/e_air.png", 17, 1)  # air sprite sheet

    def die(self):
        # for index in range(8, 16):
        #     self.air_sprite.animation(self.screen, index, self.pos[0], self.pos[1], 4)
        # tools.gameClock.tick(30)
        self.section.object = None  # remove elemental


class Earth(Elemental):
    # subclass from Elemental superclass, sets the features of the earth elemental
    def __init__(self, info, path, matrix):
        super().__init__(info, path, matrix)
        self.projectile_path = "source/resources/gui/sprites/att_e_earth.png"  # attack img

    def die(self):
        self.section.object = None  # remove elemental


class Water(Elemental):
    # subclass from Elemental superclass, sets the features of the water elemental
    def __init__(self, info, path, matrix):
        super().__init__(info, path, matrix)
        self.projectile_path = "source/resources/gui/sprites/att_e_water.png"  # attack img

    def die(self):
        self.section.object = None  # remove elemental


class Fire(Elemental):
    # subclass from Elemental superclass, sets the features of the fire elemental
    def __init__(self, info, path, matrix):
        super().__init__(info, path, matrix)
        self.projectile_path = "source/resources/gui/sprites/att_e_fire.png"  # attack img

    def die(self):
        self.section.object = None  # remove elemental


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
