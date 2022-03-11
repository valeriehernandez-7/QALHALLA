import source.classes.elementals as elementals
import source.classes.titans as titans
import source.classes.game as game

import pygame
import json
import random
import time

pygame.init()  # initialize pygame modules

# -- -constants ---
gameClock = pygame.time.Clock()  # tick function arg
seconds = 0
minutes = 0

# ---fonts---
PfefferMediaeval_font = pygame.font.Font("source/resources/gui/fonts/PfefferMediaeval.otf", 16)
Trajan_font_15 = pygame.font.Font("source/resources/gui/fonts/Trajan.otf", 15)
Insula_font_13 = pygame.font.Font("source/resources/gui/fonts/Insula.ttf", 13)
Insula_font_14 = pygame.font.Font("source/resources/gui/fonts/Insula.ttf", 14)
Insula_font_15 = pygame.font.Font("source/resources/gui/fonts/Insula.ttf", 15)
Insula_font_28 = pygame.font.Font("source/resources/gui/fonts/Insula.ttf", 28)

# ---colors---
black = (0, 0, 0)
blood_color = (130, 22, 19)
blue = (22, 46, 98)
ink_color = (40, 18, 12)
white = (255, 255, 255)

# ---Clock functions---

def clock():  # Input: the global variables, seconds and minutes
    global seconds, minutes  # Output: a string whit the current time in te game in format 00:00
    seconds += 1 / 30
    if seconds > 60:
        seconds = 0
        minutes += 1
        if minutes < 10 and seconds < 10:
            return "0" + str(minutes) + ":0" + str(int(seconds))
        elif minutes < 10:
            return "0" + str(minutes) + ":" + str(int(seconds))
        elif seconds < 10:
            return str(minutes) + ":0" + str(int(seconds))
        else:
            return str(minutes) + ":" + str(int(seconds))
    else:
        if minutes < 10 and seconds < 10:
            return "0" + str(minutes) + ":0" + str(int(seconds))
        elif minutes < 10:
            return "0" + str(minutes) + ":" + str(int(seconds))
        elif seconds < 10:
            return str(minutes) + ":0" + str(int(seconds))
        else:
            return str(minutes) + ":" + str(int(seconds))


def set_timer(new_minutes, new_seconds):  # Set the time of the clock
    global seconds, minutes
    seconds = new_seconds
    minutes = new_minutes


# --- graphic classes ---

class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, 0, 0, 1, 1)
        self.elemental = None

    def update(self):
        self.left, self.top = pygame.mouse.get_pos()
        if self.elemental:
            self.elemental.pos = (self.left - 32, self.top - 32)
            self.elemental.screen.blit(self.elemental.image, self.elemental.pos)


class Button(pygame.sprite.Sprite):

    def __init__(self, image1, image2, x, y):
        self.normal = image1
        self.selected = image2
        self.actual_image = self.normal
        self.rect = self.actual_image.get_rect()
        self.rect.left, self.rect.top = (x, y)

    def update(self, screen, cursor):
        if cursor.colliderect(self.rect):
            self.actual_image = self.selected
        else:
            self.actual_image = self.normal
        screen.blit(self.actual_image, self.rect)


# --- game's matrix classes ---

class Section:
    def __init__(self, game, position, identifier):
        self.screen = game.screen
        self.game = game
        self.pos = position
        self.id = identifier
        self.object = None
        self.update_section()

    def on_click(self, cursor):
        name = self.object.__class__.__name__  # returns class name
        if self.object:
            if name == "Gem":
                sounds("source/resources/gui/sounds/gems.wav", 0.5)
                self.game.gems += self.object.value  # adds gem value to the gem's counter
                self.object = None  # ""
            if elementals.Elemental.__subclasscheck__(self.object.__class__):
                self.object = None
        else:
            if cursor.elemental:
                self.object = cursor.elemental
                cursor.elemental = None
                self.object.section = self
                self.object.pos = self.pos
                self.object.initial_time = time.time()

    def on_attack(self, damage):
        name = type(self.object).__name__
        if name != "Gem":
            sounds("source/resources/gui/sounds/hurt.wav", 0.1)
            self.object.health -= damage

    def update_section(self):
        if self.object:
            self.object.update()


class Matrix:
    def __init__(self, game):
        self.screen = game.screen
        self.game = game
        self.sections = []
        self.create_matrix(0, 0, [])
        self.last_gem = 0
        self.gems = [["source/resources/gui/props/g5.png", 5], ["source/resources/gui/props/g25.png", 25],
                     ["source/resources/gui/props/g50.png", 50], ["source/resources/gui/props/g100.png", 100]]

    def clean(self):
        for i in self.sections:
            for j in i:
                if j.object:
                    j.object = None

    def create_matrix(self, i, j, templist):
        if j < 9:
            if i < 5:
                temp = Section(self.game, (116 + (i * 54), 123 + (j * 50)), (i, j))
                templist.append(temp)
                return self.create_matrix(i, j + 1, templist)
            return 0
        self.sections.append(templist)
        return self.create_matrix(i + 1, 0, [])

    def available(self, i, j):
        if j < 9:
            if i < 5:
                if not self.sections[i][j].object:
                    return True
                return self.available(i, j + 1)
            return False
        return self.available(i + 1, 0)

    def available_row(self, i):
        if i < 5:
            if not self.sections[i][0].object:
                return True
            return self.available_row(i + 1)
        return False

    def get_elementals(self, i, j, array):
        if j < 9:
            if i < 5:
                if elementals.Elemental.__subclasscheck__(self.sections[i][j].object.__class__):
                    array.append(self.sections[i][j].object)
                return self.get_elementals(i, j + 1, array)
            return array
        return self.get_elementals(i + 1, 0, array)

    def get_titans(self, i, j, array):
        if j < 9:
            if i < 5:
                if titans.Titan.__subclasscheck__(self.sections[i][j].object.__class__):
                    array.append(self.sections[i][j].object)
                return self.get_titans(i, j + 1, array)
            return array
        return self.get_titans(i + 1, 0, array)

    def create_object(self, object):
        available = self.available(0, 0)
        if available:
            if object.__name__ == "Gem":
                return self.create_gem(object)
            else:
                if titans.Titan.__subclasscheck__(object):
                    return self.create_titan(object)
                else:
                    return self.create_elemental(object)
        return 0

    def create_gem(self, object):
        i = random.randint(0, 4)
        j = random.randint(0, 8)
        section = self.sections[i][j]
        if not section.object:
            if object.__name__ == "Gem":
                section = self.sections[i][j]
                section.object = Gem(self.screen, self.gems[random.randint(0, 3)],
                                     (section.pos[0] + 10.5, section.pos[1] + 8.5))
                return
        return self.create_gem(object)

    def create_elemental(self, elemental):
        name = elemental.__name__
        print("✧", name, "elemental invoked ✧")  # notification
        if self.available(0, 0):
            if name == "Air":
                return elementals.Air([12, 2], "source/resources/gui/sprites/0-air.png", self)
            elif name == "Earth":
                return elementals.Earth([14, 4], "source/resources/gui/sprites/0-earth.png", self)
            elif name == "Water":
                return elementals.Water([16, 8], "source/resources/gui/sprites/0-water.png", self)
            elif name == "Fire":
                return elementals.Fire([18, 12], "source/resources/gui/sprites/0-fire.png", self)
        return None

    def create_titan(self, titan):
        i = random.randint(0, 4)
        name = titan.__name__
        section = self.sections[i][0]
        if self.available_row(0):
            if not section.object:
                if name == "Skeleton":
                    section.object = titans.Skeleton([5, 2, 10, 7], self, section,
                                                     "source/resources/gui/sprites/0-skeleton.png", -20, time.time())
                elif name == "Elf":
                    section.object = titans.Elf([10, 3, 15, 10], self, section,
                                                "source/resources/gui/sprites/0-elf.png", -20, time.time())
                elif name == "Orc":
                    section.object = titans.Orc([20, 9, 5, 13], self, section,
                                                "source/resources/gui/sprites/0-orc.png", -20, time.time())
                elif name == "Dragon":
                    section.object = titans.Dragon([25, 12, 3, 16], self, section,
                                                   "source/resources/gui/sprites/0-dragon.png", -20, time.time())
                return section.object
            return self.create_titan(titan)
        return 0

    def update(self):
        for array in self.sections:
            for section in array:
                section.update_section()


# --- gem's class ---

class Gem:
    def __init__(self, screen, info, position):
        self.screen = screen
        self.path = info[0]
        self.value = info[1]
        self.pos = position
        self.image = pygame.image.load(self.path)

    def update(self):
        self.screen.blit(self.image, self.pos)


# --- animation's class ---

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
            [(index % cols * w, int(index / cols) * h, w, h) for index in range(self.total_frames)])
        self.handle = list([
            (0, 0), (-hw, 0), (-w, 0),
            (0, -hh), (-hw, -hh), (-w, -hh),
            (0, -h), (-hw, -h), (-w, -h), ])

    def animation(self, surface, frames, x, y, handle=0):
        surface.blit(self.sprite_sheet, (x + self.handle[handle][0], y + self.handle[handle][1]),
                     self.sprite_sheet_list[frames])


# --- data's manager class ---

class SessionManager:
    def __init__(self):
        self.path = "source/resources/data/sessions.json"

    def save(self, game):
        data = self.get_game_state(game)
        with open(self.path, "w") as write:
            json.dump(data, write, indent=4)

    def reload(self, screen, menu):
        with open(self.path) as read:
            data = json.load(read)
        temp_game = game.Game(data["name"], screen, data["difficulty"], data["gems"], data["level"], menu)
        temp_game.murders = data["murders"]
        set_timer(int(data["duration"][:2]), int(data["duration"][3:5]))
        matrix = Matrix(temp_game)
        self.load_titans(matrix, data["titans"])
        self.load_elementals(matrix, data["elementals"])

        temp_game.grid = matrix
        print("⋟ RESUMED BATTLE ⋞")  # notification
        return temp_game

    def get_game_state(self, game):
        data = {}
        data["name"] = game.name
        data["difficulty"] = game.difficulty
        data["date"] = str(game.today.date())
        data["hour"] = str(game.today.time())[:5]
        data["duration"] = clock()
        data["level"] = game.screen_state
        data["gems"] = game.gems
        data["murders"] = game.murders
        data["titans"] = self.get_titans(game)
        data["elementals"] = self.get_elementals(game)
        return data

    def get_elementals(self, game):
        array = game.grid.get_elementals(0, 0, [])
        result = []
        for elemental in array:
            data = {}
            data["type"] = elemental.__class__.__name__
            data["position"] = elemental.section.id
            data["health"] = elemental.health
            data["time"] = int(time.time() - elemental.initial_time)
            result.append(data)
        return result

    def get_titans(self, game):
        array = game.grid.get_titans(0, 0, [])
        result = []
        for titan in array:
            data = {}
            data["type"] = titan.__class__.__name__
            data["position"] = titan.section.id
            data["health"] = titan.health
            data["time"] = int(time.time() - titan.initial_time)
            result.append(data)
        return result

    def load_elementals(self, matrix, data):
        for elemental in data:
            pos = elemental["position"]
            section = matrix.sections[pos[0]][pos[1]]
            if elemental["type"] == "Air":
                section.object = elementals.Air([elemental["health"], 2], "source/resources/gui/sprites/0-air.png",
                                                matrix)

            elif elemental["type"] == "Earth":
                section.object = elementals.Earth([elemental["health"], 4], "source/resources/gui/sprites/0-earth.png",
                                                  matrix)

            elif elemental["type"] == "Water":
                section.object = elementals.Water([elemental["health"], 8], "source/resources/gui/sprites/0-water.png",
                                                  matrix)

            elif elemental["type"] == "Fire":
                section.object = elementals.Fire([elemental["health"], 12], "source/resources/gui/sprites/0-fire.png",
                                                 matrix)
            section.object.section = section
            section.object.pos = section.pos
            section.object.initial_time = time.time() - elemental["time"]

    def load_titans(self, matrix, data):
        for titan in data:
            pos = titan["position"]
            section = matrix.sections[pos[0]][pos[1]]
            if titan["type"] == "Skeleton":
                section.object = titans.Skeleton([titan["health"], 2, 10, 3], matrix, section,
                                                 "source/resources/gui/sprites/0-skeleton.png",
                                                 section.pos[1], time.time() - titan["time"])
            elif titan["type"] == "Elf":
                section.object = titans.Elf([titan["health"], 3, 15, 10], matrix, section,
                                            "source/resources/gui/sprites/0-elf.png",
                                            section.pos[1], time.time() - titan["time"])
            elif titan["type"] == "Orc":
                section.object = titans.Orc([titan["health"], 9, 5, 13], matrix, section,
                                            "source/resources/gui/sprites/0-orc.png",
                                            section.pos[1], time.time() - titan["time"])
            elif titan["type"] == "Dragon":
                section.object = titans.Dragon([titan["health"], 12, 3, 16], matrix, section,
                                               "source/resources/gui/sprites/0-dragon.png",
                                               section.pos[1], time.time() - titan["time"])


# --- music & sounds ---

def music(path, volume, loop):  # method, initializes and loops the song
    pygame.mixer.init()
    pygame.mixer.music.load(path)  # filepath
    pygame.mixer.music.set_volume(volume)  # 0.0 - 1.0
    pygame.mixer.music.play(loop)  # -1:infinite , 0:play once


def sounds(path, volume):  # method, initializes and play the sound
    pygame.mixer.get_init()
    song = pygame.mixer.Sound(path)  # filepath
    song.set_volume(volume)  # 0.0 - 1.0
    pygame.mixer.Sound.play(song)