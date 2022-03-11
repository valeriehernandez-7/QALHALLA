import source.classes.titans as titans
import source.classes.tools as tools

import pygame
import time

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
        self.projectiles = []  # projectile control list
        self.matrix = matrix
        self.section = None  # default section
        self.pos = ()  # default position
        self.screen = self.matrix.screen
        self.image = pygame.image.load(path)  # load elemental img
        self.initial_time = 0  # default time reference

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
    # screen: screen, path: filepath, elemental: elemental attacking, titan: titan under attack
    def __init__(self, screen, path, elemental, titan):
        # in charge of generating the projectiles of the elemental, move it from the position of the elemental to
        # the position of the titan and discount the power of attack to the titan's health
        self.screen = screen
        self.image = pygame.image.load(path)  # load attack img
        self.elemental = elemental  # elemental ID
        self.pos = self.elemental.section.pos  # elemental position
        self.titan = titan  # titan ID

    def update(self):
        self.pos = (self.pos[0], self.pos[1] - 3)  # projectile position
        self.screen.blit(self.image, self.pos)  # show projectile
        if self.pos[1] <= self.titan.pos[1]:  # projectile movement to titan
            if self.titan.health > 0:  # living titan
                self.titan.hurt(self.elemental.attack_power)  # discount attack power to titan's health
            self.elemental.projectiles.remove(self)  # dead titan, removes projectile
        if self.pos[1] < -50:  # projectile movement to screen edge
            self.elemental.projectiles.remove(self)  # remove projectile
