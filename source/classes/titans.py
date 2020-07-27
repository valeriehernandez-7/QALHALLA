# --- libraries ---
import time

import pygame

import source.classes.elementals as elementals  # source/elementals.py
import source.classes.tools as tools  # source/tools.py

pygame.init()  # pygame initialization


def get_nearest(actual, matrix):
    for i in range(actual[1], 9):
        element = matrix[actual[0]][i]
        if element.object:
            if elementals.Elemental.__subclasscheck__(element.object.__class__):
                return element
    return None


class Titan:
    def __init__(self, info, matrix, section, path, pos_y, initial_time):
        self.health, self.attack_power, self.attack_freq, self.move_freq = info[0], info[1], info[2], info[3]
        self.matrix = matrix
        self.initial_time = initial_time
        self.section = section
        self.pos = (self.section.pos[0], pos_y)
        self.screen = self.matrix.screen
        self.speed = 5
        self.current_speed = self.speed
        self.image = pygame.image.load(path)
        self.attacking = False
        self.moved = False
        self.projectiles = []
        self.projectile_path = ""

    def move(self):
        if 0 < (time.time() - self.initial_time) % self.move_freq < 0.02:
            identifier = self.section.id
            temp = self.matrix.sections[identifier[0]][identifier[1] + 1]
            if not temp.object and self.moved:
                if temp.id[1] == 8:
                    # GameOverScreen()
                    self.section.game.gameover = True
                    return 0
                self.section.object = None
                self.section = temp
                self.section.object = self
            self.moved = True
        # Activate animation for walking

    def attack(self):
        return  # overridden

    def hurt(self, damage):
        tools.sounds("source/resources/gui/sounds/hurt.wav", 0.1)
        self.health -= damage

    def die(self):
        self.section.object = None
        self.section.game.gems += 75
        self.section.game.murders += 1
        print("☠ Titan's deaths", self.section.game.murders, "☠")

    def update(self):
        for projectile in self.projectiles:
            projectile.update()
        if self.section.pos != self.pos:  # titan's current section
            self.attacking = False
            self.current_speed = self.speed
        if self.section.pos <= self.pos and self.current_speed != 0:
            self.pos = (self.section.pos[0], self.section.pos[1])
            self.attacking = True
            self.current_speed = 0
            # Deactivate animation for walking
        if self.health <= 0:
            self.die()
        self.pos = (self.pos[0], self.pos[1] + self.current_speed)
        self.screen.blit(self.image, (self.pos[0] - 6.5, self.pos[1] - 18))


class Skeleton(Titan):
    def __init__(self, info, matrix, section, path, pos_y, initial_time):
        super().__init__(info, matrix, section, path, pos_y, initial_time)
        self.projectile_path = "source/resources/gui/sprites/att_t_skeleton.png"

    def attack(self):
        if 0 < (time.time() - self.initial_time) % self.attack_freq < 0.05:
            identifier = self.section.id
            temp = get_nearest(identifier, self.matrix.sections)
            if temp:
                self.projectiles.append(Projectile(self.screen, self.projectile_path, temp.object, self))
                print("⤞ Skeleton attack", temp.id, "⤞")
                # Activate animation for attack


class Elf(Titan):
    def __init__(self, info, matrix, section, path, pos_y, initial_time):
        super().__init__(info, matrix, section, path, pos_y, initial_time)
        self.projectile_path = "source/resources/gui/sprites/att_t_elf.png"

    def attack(self):
        if 0 < (time.time() - self.initial_time) % self.attack_freq < 0.05:
            identifier = self.section.id
            temp = get_nearest(identifier, self.matrix.sections)
            if temp:
                self.projectiles.append(Projectile(self.screen, self.projectile_path, temp.object, self))
                print("➼ Elf attack", temp.id, "➼")
                # Activate animation for attack


class Orc(Titan):
    def __init__(self, info, matrix, section, path, pos_y, initial_time):
        super().__init__(info, matrix, section, path, pos_y, initial_time)

    def attack(self):
        if 0 < (time.time() - self.initial_time) % self.attack_freq < 0.05:
            identifier = self.section.id
            temp = self.matrix.sections[identifier[0]][identifier[1] + 1]
            if temp.object and elementals.Elemental.__subclasscheck__(temp.object.__class__):
                temp.on_attack(self.attack_power)
                print("✠ Orc attack", temp.id, "✠")
                # Activate animation for attack


class Dragon(Titan):
    def __init__(self, info, matrix, section, path, pos_y, initial_time):
        super().__init__(info, matrix, section, path, pos_y, initial_time)

    def attack(self):
        if 0 < (time.time() - self.initial_time) % self.attack_freq < 0.05:
            identifier = self.section.id
            temp = self.matrix.sections[identifier[0]][identifier[1] + 1]
            if temp.object and elementals.Elemental.__subclasscheck__(temp.object.__class__):
                temp.on_attack(self.attack_power)
                print("☬ Dragon attack", temp.id, "☬")
                # Activate animation for attack


class Projectile:
    def __init__(self, screen, path, elemental, titan):
        self.screen = screen
        self.image = pygame.image.load(path)
        self.elemental = elemental
        self.titan = titan
        self.pos = self.titan.section.pos

    def update(self):
        self.pos = (self.pos[0], self.pos[1] + 3)
        self.screen.blit(self.image, self.pos)
        if self.pos[1] >= self.elemental.pos[1]:
            if self.elemental.health > 0:
                self.elemental.hurt(self.titan.attack_power)
            self.titan.projectiles.remove(self)
        if self.pos[1] > 751:
            self.titan.projectiles.remove(self)
