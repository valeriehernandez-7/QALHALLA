# --- libraries ---
import datetime
import random
import time

import pygame

import source.classes.elementals as elementals  # source/elementals.py
import source.classes.titans as titans  # source/titans.py
import source.classes.tools as tools  # source/tools.py
import source.classes.menu as menu  # source/menu.py


pygame.init()  # pygame initialization


class Game:
    # name:battle name, screen:display settings, difficulty:battle mode, gems:gem count,
    # start_level:name level configuration, main_menu:menu screen class
    def __init__(self, name, screen, difficulty, gems, start_level, main_menu):
        # --- load sources---
        self.frame_image = pygame.image.load("source/resources/gui/props/frame.png")  # gui frame img
        self.save_button_image_0 = pygame.image.load("source/resources/gui/buttons/b0_save.png")  # normal state img
        self.save_button_image_1 = pygame.image.load("source/resources/gui/buttons/b1_save.png")  # active state img
        self.muted_button_image_0 = pygame.image.load("source/resources/gui/buttons/b0_muted.png")  # normal state img
        self.muted_button_image_1 = pygame.image.load("source/resources/gui/buttons/b1_muted.png")  # active state img
        self.c0_air = pygame.image.load("source/resources/gui/buttons/c0_air.png")  # normal state img
        self.c1_air = pygame.image.load("source/resources/gui/buttons/c1_air.png")  # active state img
        self.c0_earth = pygame.image.load("source/resources/gui/buttons/c0_earth.png")  # normal state img
        self.c1_earth = pygame.image.load("source/resources/gui/buttons/c1_earth.png")  # active state img
        self.c0_water = pygame.image.load("source/resources/gui/buttons/c0_water.png")  # normal state img
        self.c1_water = pygame.image.load("source/resources/gui/buttons/c1_water.png")  # active state img
        self.c0_fire = pygame.image.load("source/resources/gui/buttons/c0_fire.png")  # normal state img
        self.c1_fire = pygame.image.load("source/resources/gui/buttons/c1_fire.png")  # active state img

        # --- buttons ---
        # --- save button---
        self.save_button = tools.Button(self.save_button_image_0, self.save_button_image_1, 11, 622)
        # --- muted button---
        self.muted_button = tools.Button(self.muted_button_image_0, self.muted_button_image_1, 432, 622)
        # --- air button---
        self.air_button = tools.Button(self.c0_air, self.c0_air, 99, 582)
        # ---earth button---
        self.earth_button = tools.Button(self.c0_earth, self.c0_earth, 188, 583)
        # ---water button---
        self.water_button = tools.Button(self.c0_water, self.c0_water, 272, 580)
        # ---fire button---
        self.fire_button = tools.Button(self.c0_fire, self.c0_fire, 354, 583)

        # --- game variables ---
        self.screen = screen
        self.menu = main_menu
        self.screen_state = start_level  # screen ID
        self.level_title = "Nivel 1"  # level text
        self.background = pygame.image.load("source/resources/gui/backgrounds/lvl1.jpg")  # background img
        self.today = datetime.datetime.now()  # current date
        self.name = name  # battle name
        self.gems = gems  # gem counter, defines the value available to buy elementals
        self.murders = 0  # titan death counter, defines when the next level is set
        self.difficulty = difficulty  # battle mode
        self.frequency = 0  # frequency of attack of the elementals according to battle mode
        self.attack_freq = 0  # frequency of attack of the titans according to game level
        self.gameover = False
        self.started = False
        self.moving = False

        # --- game methods ---
        self.cursor = tools.Cursor()  # Cursor, class from tools.py
        self.grid = tools.Matrix(self)  # Matrix,  class from tools.py
        self.session_manager = tools.SessionManager()  # SessionManager,  class from tools.py

        # --- setting the attack frequency of the elementals according to the battle mode ---
        if self.difficulty == "MONJE":  # high-frequency elemental attack configuration (easy level)
            self.attack_freq = 0.5
        if self.difficulty == "MAESTRO":  # regular frequency configuration of elemental attacks (regular level)
            self.attack_freq = 0.3
        if self.difficulty == "AVATAR":  # low frequency elemental attack configuration (hard level)
            self.attack_freq = 0

        print("❆ BATTLE'S NAME:", self.name, " | BATTLE MODE:", self.difficulty, " | DATE & TIME:", self.today, "❆")

    def lvl1(self):  # method, defines the settings for the level 1 screen
        self.background = pygame.image.load("source/resources/gui/backgrounds/lvl1.jpg")  # background img
        self.screen_state = "lvl1"  # screen ID
        self.level_title = "Nivel 1"  # level text

    def lvl2(self):  # method, defines the settings for the level 2 screen
        self.background = pygame.image.load("source/resources/gui/backgrounds/lvl2.jpg")  # background img
        self.level_title = "Nivel 2"  # level text
        self.grid.clean()  # clean matrix
        self.frequency = 0.3  # frequency increases by 30%

    def lvl3(self):  # method, defines the settings for the level 3 screen
        self.background = pygame.image.load("source/resources/gui/backgrounds/lvl3.jpg")  # background img
        self.level_title = "Nivel 3"  # level text
        self.grid.clean()  # clean matrix
        self.frequency = 0.6  # frequency increases by 60%

    def change_level(self, initial):
        #  method, according to the number of deaths of titans, the function changes the display identifier and calls up
        #  the lvl# method or shows the winner screen
        if self.murders == 10 and self.screen_state != "lvl2":
            tools.sounds("source/resources/gui/sounds/level_up.wav", 0.5)
            self.screen_state = "lvl2"  # screen ID
            self.lvl2()
        if self.murders == 20 and self.screen_state != "lvl3":
            tools.sounds("source/resources/gui/sounds/level_up.wav", 0.5)
            self.screen_state = "lvl3"  # screen ID
            self.lvl3()
        if self.murders == 50:
            self.screen_screen = "winner"  # screen ID
            print("⫸ VICTORY ⫷")
            pygame.mixer.music.stop()  # stops the main menu song
            after_game = AfterGame(self.screen, self.name, int(time.time() - initial), self.menu)
            after_game.winner()  # winner screen
            after_game.setup()  # after_game class loop

    def cards_cs(self):  # method, cards control system is in charge of enabling and disabling the purchase options
        if self.gems >= 200:  # enables the four purchase options
            self.air_button = tools.Button(self.c1_air, self.c1_air, 99, 582)
            self.earth_button = tools.Button(self.c1_earth, self.c1_earth, 188, 583)
            self.water_button = tools.Button(self.c1_water, self.c1_water, 272, 580)
            self.fire_button = tools.Button(self.c1_fire, self.c1_fire, 354, 583)
        elif self.gems >= 150:  # disables the fire purchase option
            self.air_button = tools.Button(self.c1_air, self.c1_air, 99, 582)
            self.earth_button = tools.Button(self.c1_earth, self.c1_earth, 188, 583)
            self.water_button = tools.Button(self.c1_water, self.c1_water, 272, 580)
            self.fire_button = tools.Button(self.c0_fire, self.c0_fire, 354, 583)
        elif self.gems >= 100:  # disables fire and water purchase options
            self.air_button = tools.Button(self.c1_air, self.c1_air, 99, 582)
            self.earth_button = tools.Button(self.c1_earth, self.c1_earth, 188, 583)
            self.water_button = tools.Button(self.c0_water, self.c0_water, 272, 580)
            self.fire_button = tools.Button(self.c0_fire, self.c0_fire, 354, 583)
        elif self.gems >= 50:  # disables fire,water and earth purchase options
            self.air_button = tools.Button(self.c1_air, self.c1_air, 99, 582)
            self.earth_button = tools.Button(self.c0_earth, self.c0_earth, 188, 583)
            self.water_button = tools.Button(self.c0_water, self.c0_water, 272, 580)
            self.fire_button = tools.Button(self.c0_fire, self.c0_fire, 354, 583)
        elif self.gems < 50:  # disables all purchase options
            self.air_button = tools.Button(self.c0_air, self.c0_air, 99, 582)
            self.earth_button = tools.Button(self.c0_earth, self.c0_earth, 188, 583)
            self.water_button = tools.Button(self.c0_water, self.c0_water, 272, 580)
            self.fire_button = tools.Button(self.c0_fire, self.c0_fire, 354, 583)

    def generator(self, initial):
        # method,
        if 0 < (time.time() - initial) % 30 < 0.05:
            self.grid.create_object(tools.Gem)
            print("✦ MAGIC RUNE ✦")
        if 0 < (time.time() - initial) % (30 - (30 * self.frequency)) < 0.05:
            self.grid.create_object(titans.Skeleton)
            print("⤞ Skeleton's coming ⤞")
        if 0 < (time.time() - initial) % (70 - (70 * self.frequency)) < 0.05:
            if self.started:
                self.grid.create_object(titans.Elf)
                print("➼ Elf's coming ➼")
        if 0 < (time.time() - initial) % (90 - (90 * self.frequency)) < 0.05:
            if self.started:
                self.grid.create_object(titans.Orc)
                print("✠ Orc's coming ✠")
        if 0 < (time.time() - initial) % (120 - (120 * self.frequency)) < 0.05:
            if self.started:
                self.grid.create_object(titans.Dragon)
                print("☬ Dragon's coming ☬")
            self.started = True

    def titan_attack(self, initial):
        titans_array = self.grid.get_titans(0, 0, [])
        if 7 < (time.time() - initial) % 20 < 7.05:
            if self.moving:
                for titan in titans_array:
                    if titan.__class__.__name__ == "Skeleton":
                        titan.attack()

        if 10 < (time.time() - initial) % 20 < 10.05:
            if self.moving:
                for titan in titans_array:
                    if titan.__class__.__name__ == "Elf":
                        titan.attack()
        if 13 < (time.time() - initial) % 20 < 13.05:
            if self.moving:
                for titan in titans_array:
                    if titan.__class__.__name__ == "Orc":
                        titan.attack()
        if 16 < (time.time() - initial) % 20 < 16.05:
            if self.moving:
                for titan in titans_array:
                    if titan.__class__.__name__ == "Dragon":
                        titan.attack()
            self.moving = True

    def entity_actions(self):
        elementals_array = self.grid.get_elementals(0, 0, [])
        for elemental in elementals_array:
            elemental.attack()

        titans_array = self.grid.get_titans(0, 0, [])
        for titan in titans_array:
            titan.attack()
            titan.move()


    def start_game(self):  # method, run the game
        fps = pygame.time.Clock()
        initial = time.time()
        tools.music("source/resources/gui/sounds/game.mp3", 0.05, -1)
        while True:
            pygame.display.update()
            fps.tick(30)
            self.change_level(initial)
            if self.gameover:
                print("⤲ GAME OVER ⤲")
                pygame.mixer.music.stop()  # stops the game song
                after_game = AfterGame(self.screen, self.name, int(time.time() - initial), self.menu)
                after_game.game_over()
                after_game.setup()
                break
            else:
                self.cards_cs()
                self.generator(initial)
                self.entity_actions()
                for event in pygame.event.get():
                    # stops code execution by pressing the window button or the esc key
                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # --- cursor-events ---
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.cursor.colliderect(self.save_button.rect):
                            tools.sounds("source/resources/gui/sounds/button.wav", 0.5)
                            self.session_manager.save(self)
                            print("☸", self.name, "SUCCESSFULLY SAVED ☸")
                        elif self.cursor.colliderect(self.muted_button.rect):
                            tools.sounds("source/resources/gui/sounds/button.wav", 0.5)
                            pygame.mixer.music.stop()
                            print("♫ MUTED MUSIC ♫")
                        elif self.cursor.colliderect(self.air_button.rect) and (self.gems >= 50):
                            tools.sounds("source/resources/gui/sounds/invoke.wav", 0.5)
                            self.cursor.elemental = self.grid.create_object(elementals.Air)
                            self.gems -= 50
                        elif self.cursor.colliderect(self.earth_button.rect) and (self.gems >= 100):
                            tools.sounds("source/resources/gui/sounds/invoke.wav", 0.5)
                            self.cursor.elemental = self.grid.create_object(elementals.Earth)
                            self.gems -= 100
                        elif self.cursor.colliderect(self.water_button.rect) and (self.gems >= 150):
                            tools.sounds("source/resources/gui/sounds/invoke.wav", 0.5)
                            self.cursor.elemental = self.grid.create_object(elementals.Water)
                            self.gems -= 150
                        elif self.cursor.colliderect(self.fire_button.rect) and (self.gems >= 200):
                            tools.sounds("source/resources/gui/sounds/invoke.wav", 0.5)
                            self.cursor.elemental = self.grid.create_object(elementals.Fire)
                            self.gems -= 200

                        x, y = event.pos
                        for array in self.grid.sections:  # handles events within the matrix zone
                            for section in array:
                                location = section.pos  # get event position
                                if (location[0] < x < location[0] + 51) and (
                                        location[1] < y < location[1] + 48):  # events within the box range
                                    section.on_click(self.cursor)

                # --- graphics ---
                # --- text ---
                self.level = tools.Trajan_font_15.render(self.level_title, True, tools.white)
                self.battlename = tools.Insula_font_15.render(self.name, True, tools.black)
                self.gems_label = tools.Insula_font_15.render(str(self.gems), True, tools.black)
                self.time = tools.Insula_font_15.render(tools.clock(), True, tools.black)

                # --- show ---
                self.screen.blit(self.background, (0, 0))
                self.grid.update()
                self.cursor.update()
                self.screen.blit(self.frame_image, (0, 0))
                self.screen.blit(self.level, (219, 39))
                self.screen.blit(self.battlename, (72, 76))
                self.screen.blit(self.gems_label, (223, 76))
                self.screen.blit(self.time, (380, 76))
                # --- update ---
                self.save_button.update(self.screen, self.cursor)
                self.muted_button.update(self.screen, self.cursor)
                self.air_button.update(self.screen, self.cursor)
                self.earth_button.update(self.screen, self.cursor)
                self.water_button.update(self.screen, self.cursor)
                self.fire_button.update(self.screen, self.cursor)


class AfterGame:
    def __init__(self, screen, name, duration, main_screen):
        # --- load source/resources ---
        self.backgrounds = ["source/resources/gui/backgrounds/gameover.jpg",
                            "source/resources/gui/backgrounds/winner.jpg"]
        self.shields = ["source/resources/gui/props/go_1.png", "source/resources/gui/props/go_2.png",
                        "source/resources/gui/props/go_3.png", "source/resources/gui/props/go_4.png",
                        "source/resources/gui/props/go_5.png"]
        self.trophies = ["source/resources/gui/props/win_1.png", "source/resources/gui/props/win_2.png",
                         "source/resources/gui/props/win_3.png", "source/resources/gui/props/win_4.png"]
        self.button_menu_st0 = pygame.image.load("source/resources/gui/buttons/b0_menu.png")  # normal state image
        self.button_menu_st1 = pygame.image.load("source/resources/gui/buttons/b1_menu.png")  # active state image
        # --- AfterGame methods ---
        self.cursor = tools.Cursor()  # Cursor, from the class Cursor in the tools py
        # --- AfterGame variables ---
        self.screen = screen
        self.name = name
        self.time = duration
        self.main_screen = main_screen
        # --- button ---
        self.menu_button = tools.Button(self.button_menu_st0, self.button_menu_st1, 375, 15)

    def game_over(self):
        tools.sounds("source/resources/gui/sounds/game_over.wav", 1)
        self.main_screen.screen_state = "game_over"
        self.background = pygame.image.load(self.backgrounds[0])
        self.shield = pygame.image.load(self.shields[random.randint(0, 4)])

    def winner(self):
        tools.music("source/resources/gui/sounds/victory.mp3", 0.2 , -1)
        self.main_screen.screen_state = "winner"
        self.background = pygame.image.load(self.backgrounds[1])
        self.trophy = pygame.image.load(self.trophies[random.randint(0, 3)])
        file = open("source/resources/data/scores.txt", "a", encoding='utf-8')
        file.write("\n" + self.name + "," + str(self.time))
        file.close()

    def setup(self):
        while True:
            pygame.display.update()
            self.screen.blit(self.background, (0, 0))  # background
            # --- cursor events ---
            for event in pygame.event.get():
                self.cursor.update()
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # --- cursor events ---
                    if self.main_screen.screen_state == "game_over":
                        if self.cursor.colliderect(self.menu_button):
                            menu_screen = menu.MenuScreen()
                            menu_screen.menu()
                            menu_screen.start_game()
                    elif self.main_screen.screen_state == "winner":
                        if self.cursor.colliderect(self.menu_button):
                            menu_screen = menu.MenuScreen()
                            menu_screen.menu()
                            menu_screen.start_game()
            # --- graphics ---
            if self.main_screen.screen_state == "game_over":
                self.menu_button.update(self.screen, self.cursor)
                self.screen.blit(self.shield, (190, 275))  # shield
            elif self.main_screen.screen_state == "winner":
                self.menu_button.update(self.screen, self.cursor)
                self.screen.blit(self.trophy, (190, 275))  # trophy
