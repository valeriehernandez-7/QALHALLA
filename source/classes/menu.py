import source.classes.tools as tools
import source.classes.game as game

import pygame
import json

pygame.init()  # initialize pygame modules

# ---game-screens classes---

class MenuScreen:
    def __init__(self):
        # --- load sources ---
        # --- main screen button images ---
        self.button_play_st0 = pygame.image.load("source/resources/gui/buttons/b0_play.png")  # normal state img
        self.button_play_st1 = pygame.image.load("source/resources/gui/buttons/b1_play.png")  # active state img
        self.button_load_st0 = pygame.image.load("source/resources/gui/buttons/b0_load.png")  # normal state img
        self.button_load_st1 = pygame.image.load("source/resources/gui/buttons/b1_load.png")  # active state img
        self.button_scores_st0 = pygame.image.load("source/resources/gui/buttons/b0_scores.png")  # normal state img
        self.button_scores_st1 = pygame.image.load("source/resources/gui/buttons/b1_scores.png")  # active state img
        self.button_help_st0 = pygame.image.load("source/resources/gui/buttons/b0_help.png")  # normal state img
        self.button_help_st1 = pygame.image.load("source/resources/gui/buttons/b1_help.png")  # active state img
        self.button_credits_st0 = pygame.image.load("source/resources/gui/buttons/b0_credits.png")  # normal state img
        self.button_credits_st1 = pygame.image.load("source/resources/gui/buttons/b1_credits.png")  # active state img
        # --- menu button images ---
        self.button_menu_st0 = pygame.image.load("source/resources/gui/buttons/b0_menu.png")  # normal state img
        self.button_menu_st1 = pygame.image.load("source/resources/gui/buttons/b1_menu.png")  # active state img
        # --- help screen button images ---
        self.b_page_R = pygame.image.load("source/resources/gui/buttons/b_page_R.png")  # active state img
        self.b_page_L = pygame.image.load("source/resources/gui/buttons/b_page_L.png")  # active state img
        self.b_page_0 = pygame.image.load("source/resources/gui/buttons/b_page_0.png")  # normal state img
        # --- difficulty screen button images ---
        self.button_easy_0 = pygame.image.load("source/resources/gui/buttons/b0_difficulty.png")  # normal state img
        self.button_easy_1 = pygame.image.load("source/resources/gui/buttons/b1_easy.png")  # active state img
        self.button_regular_0 = pygame.image.load("source/resources/gui/buttons/b0_difficulty.png")  # normal state img
        self.button_regular_1 = pygame.image.load("source/resources/gui/buttons/b1_regular.png")  # active state img
        self.button_hard_0 = pygame.image.load("source/resources/gui/buttons/b0_difficulty.png")  # normal state img
        self.button_hard_1 = pygame.image.load("source/resources/gui/buttons/b1_hard.png")  # active state img
        # --- player screen button images ---
        self.button_start_game_st0 = pygame.image.load("source/resources/gui/buttons/b0_game.png")  # normal state img
        self.button_start_game_st1 = pygame.image.load("source/resources/gui/buttons/b1_game.png")  # active state img
        self.next_window_0 = pygame.image.load("source/resources/gui/buttons/b0_next.png")  # normal state img
        self.next_window_1 = pygame.image.load("source/resources/gui/buttons/b1_next.png")  # active state img

        # --- game variables ---
        self.screen = pygame.display.set_mode((500, 700))  # screen size graphic method
        self.cursor = tools.Cursor()  # cursor graphic method from tools.py
        self.update_screen = pygame.display.update()  # pygame update
        self.screen_state = "menu"
        self.game = None
        self.difficulty = None

        self.menu()

    def menu(self):
        # method, sets the display to the main menu format
        self.screen_state = "menu"  # screen ID
        self.background = pygame.image.load("source/resources/gui/backgrounds/menu.jpg")  # background img
        # --- buttons ---
        # "INICIAR BATALLA" button graphic method from tools
        self.play_button = tools.Button(self.button_play_st0, self.button_play_st1, 132, 305)
        # "REANUDAR BATALLA" button graphic method from tools
        self.load_button = tools.Button(self.button_load_st0, self.button_load_st1, 132, 370)
        # "HISTORIAL DE BATALLAS" button graphic method from tools
        self.scores_button = tools.Button(self.button_scores_st0, self.button_scores_st1, 132, 435)
        # "AYUDA" button graphic method from tools
        self.help_button = tools.Button(self.button_help_st0, self.button_help_st1, 132, 500)
        # "CREDITOS" button graphic method from tools
        self.credits_button = tools.Button(self.button_credits_st0, self.button_credits_st1, 132, 565)

    def select_difficulty(self):
        # method, sets the display to the difficulty selection screen format (battle mode)
        self.screen_state = "select_difficulty"  # screen ID
        self.background = pygame.image.load("source/resources/gui/backgrounds/power.jpg")  # background img
        # --- buttons ---
        # "MENU" button graphic method from tools
        self.menu_button = tools.Button(self.button_menu_st0, self.button_menu_st1, 375, 15)
        # "MONJE - MAESTRO - AVATAR" button graphic method from tools
        self.easy_button = tools.Button(self.button_easy_1, self.button_easy_0, 127, 318)
        self.regular_button = tools.Button(self.button_regular_1, self.button_regular_0, 217, 318)
        self.hard_button = tools.Button(self.button_hard_1, self.button_hard_0, 308, 318)
        # "SIGUIENTE" button graphic method from tools
        self.next_window_button = tools.Button(self.next_window_0, self.next_window_1, 200, 462)

    def player(self):
        # method, sets the display to the format of the screen where the user enters the battle name
        self.screen_state = "player"  # screen ID
        self.background = pygame.image.load("source/resources/gui/backgrounds/player.jpg")  # background img
        # --- buttons ---
        # "MENU" button graphic method from tools
        self.menu_button = tools.Button(self.button_menu_st0, self.button_menu_st1, 375, 15)
        # "JUGAR" button graphic method from tools
        self.game_button = tools.Button(self.button_start_game_st0, self.button_start_game_st1, 197, 464)
        # --- entry-text ---
        self.name_text = "INSERTE NOMBRE DE BATALLA"  # instruction text
        self.name = ""

    def check_box(self, name):
        # method, checks data entered by user
        if name == "" or name == "INSERTE NOMBRE DE BATALLA":
            return False
        elif name[0] == " ":
            return self.check_box(name[1:])
        else:
            return True

    def load(self):
        # method, sets the display to battle loading format, receives and displays data from sessions.json
        self.screen_state = "load_game"  # screen ID
        self.background = pygame.image.load("source/resources/gui/backgrounds/load.jpg")  # background img
        # --- buttons ---
        # "MENU" button graphic method from tools
        self.menu_button = tools.Button(self.button_menu_st0, self.button_menu_st1, 375, 15)
        self.game_button = tools.Button(self.button_start_game_st0, self.button_start_game_st1, 197, 464)
        # --- battle's information ---
        with open("source/resources/data/sessions.json") as file:
            data = json.load(file)
        self.battlename = data["name"]  # stored battle's name
        self.battlemode = data["difficulty"]  # stored battle's mode
        self.time_saved = data["hour"]  # time when the battle was stored
        self.date_saved = data["date"]  # date when the battle was stored

    def scores(self):
        # method, sets the display to the best battle time display format
        self.screen_state = "scores"  # screen ID
        self.background = pygame.image.load("source/resources/gui/backgrounds/scores.jpg")  # background img
        # --- buttons ---
        # "MENU" button graphic method from tools
        self.menu_button = tools.Button(self.button_menu_st0, self.button_menu_st1, 375, 15)
        # --- information's graph-format class ---
        self.table = Table(self.screen)

    def help(self):
        # method, sets the display to the help screen format
        self.screen_state = "help"  # screen ID
        self.background = pygame.image.load("source/resources/gui/backgrounds/help.jpg")  # background img
        self.number_page = 0  # stores the current book page
        # --- buttons ---
        # "MENU" button graphic method from tools
        self.menu_button = tools.Button(self.button_menu_st0, self.button_menu_st1, 375, 15)
        self.left_button = tools.Button(self.b_page_0, self.b_page_L, 17, 175)  # button to go previous page
        self.right_button = tools.Button(self.b_page_0, self.b_page_R, 257, 175)  # button to go next page

    def credits(self):
        # method, sets the display to show information about the developers of the program
        self.screen_state = "credits"  # screen ID
        self.background = pygame.image.load("source/resources/gui/backgrounds/credits.jpg")  # background img
        # --- buttons ---
        # "MENU" button graphic method from tools
        self.menu_button = tools.Button(self.button_menu_st0, self.button_menu_st1, 375, 15)

    def start_game(self):
        # method, main function of the game screen, managing events and displaying objects on screen
        icon = pygame.image.load("source/resources/gui/props/icon.png")  # window's icon img
        pygame.display.set_icon(icon)  # window's icon
        pygame.display.set_caption("QALHALLA")  # window's title
        fps = pygame.time.Clock()  # handle events using the pygame-clock
        tools.music("source/resources/gui/sounds/bass.mp3", 0.3, -1)  # play main menu song theme
        while True:
            pygame.display.update()
            self.screen.blit(self.background, (0, 0))  # displays background img
            fps.tick(30)  # the events on this screen will be performed within 30 milliseconds

            for event in pygame.event.get():
                self.cursor.update()
                #  stops code execution by pressing the window button or the esc key
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # --- events ---
                # --- key-events ---
                elif self.screen_state == "player" and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:  # erase character
                        self.name_text = self.name_text[:-1]
                        self.name = self.name[:-1]
                    elif len(self.name) < 10 and (not event.key == pygame.K_RETURN):  # checks the name length
                        self.name += event.unicode  # records a letter in the name constant
                        self.name_text = self.name  # deletes the instruction text "Inserte nombre de batalla"

                # --- cursor events ---
                elif event.type == pygame.MOUSEBUTTONDOWN:  # mouse-click selection
                    tools.sounds("source/resources/gui/sounds/button.wav", 0.5)
                    if self.screen_state == "menu":  # cursor events on the main menu screen
                        if self.cursor.colliderect(self.play_button):
                            MenuScreen.select_difficulty(self)
                        elif self.cursor.colliderect(self.load_button):
                            MenuScreen.load(self)
                        elif self.cursor.colliderect(self.scores_button):
                            MenuScreen.scores(self)
                        elif self.cursor.colliderect(self.help_button):
                            MenuScreen.help(self)
                        elif self.cursor.colliderect(self.credits_button):
                            MenuScreen.credits(self)

                    elif self.screen_state == "select_difficulty":  # cursor events on the battle mode selection screen
                        if self.cursor.colliderect(self.menu_button):
                            MenuScreen.menu(self)
                        elif self.cursor.colliderect(self.easy_button):
                            self.difficulty = "MONJE"
                            self.easy_button = tools.Button(self.button_easy_1, self.button_easy_1, 127, 318)
                            self.regular_button = tools.Button(self.button_regular_0, self.button_regular_0, 217, 318)
                            self.hard_button = tools.Button(self.button_hard_0, self.button_hard_0, 308, 318)
                        elif self.cursor.colliderect(self.regular_button):
                            self.difficulty = "MAESTRO"
                            self.easy_button = tools.Button(self.button_easy_0, self.button_easy_0, 127, 318)
                            self.regular_button = tools.Button(self.button_regular_1, self.button_regular_1, 217, 318)
                            self.hard_button = tools.Button(self.button_hard_0, self.button_hard_0, 308, 318)
                        elif self.cursor.colliderect(self.hard_button):
                            self.difficulty = "AVATAR"
                            self.easy_button = tools.Button(self.button_easy_0, self.button_easy_0, 127, 318)
                            self.regular_button = tools.Button(self.button_regular_0, self.button_regular_0, 217, 318)
                            self.hard_button = tools.Button(self.button_hard_1, self.button_hard_1, 308, 318)
                        elif self.cursor.colliderect(self.next_window_button) and isinstance(self.difficulty, str):
                            self.screen_state = "player"
                            MenuScreen.player(self)

                    elif self.screen_state == "player":  # cursor events in the battle name entry screen
                        if self.cursor.colliderect(self.menu_button):
                            MenuScreen.menu(self)
                        elif self.cursor.colliderect(self.game_button) and self.check_box(self.name_text):
                            pygame.mixer.music.stop()  # stops the main menu song
                            tools.set_timer(0, 0)  # set the timer to 00:00
                            self.gems = 250  # initial amount of gems for new game
                            self.start_level = "lvl1"  # starting level for new game
                            self.screen_state = "game"  # return screen identifier

                    elif self.screen_state == "load_game":  # cursor events on the battle loading screen
                        if self.cursor.colliderect(self.menu_button):
                            MenuScreen.menu(self)
                        elif self.cursor.colliderect(self.game_button):
                            pygame.mixer.music.stop()
                            self.screen_state = "game"
                            self.game = tools.SessionManager().reload(self.screen, self)

                    elif self.screen_state == "scores":  # cursor events on the best battle times screen
                        if self.cursor.colliderect(self.menu_button):
                            MenuScreen.menu(self)

                    elif self.screen_state == "help":  # cursor events in the help screen
                        if self.cursor.colliderect(self.menu_button):
                            MenuScreen.menu(self)
                        elif self.cursor.colliderect(self.right_button) and (self.number_page < 7):
                            self.number_page += 1  # turn the page
                            tools.sounds("source/resources/gui/sounds/page.wav", 1)  # plays page sound
                        elif self.cursor.colliderect(self.left_button) and (self.number_page > 0):
                            self.number_page -= 1  # back to page
                            tools.sounds("source/resources/gui/sounds/page.wav", 1)  # plays page sound

                    elif self.screen_state == "credits":  # cursor events in the credits screen
                        if self.cursor.colliderect(self.menu_button):
                            MenuScreen.menu(self)

            # --- graphics ---
            if self.screen_state == "menu":  # main menu screen graphics
                self.play_button.update(self.screen, self.cursor)
                self.load_button.update(self.screen, self.cursor)
                self.scores_button.update(self.screen, self.cursor)
                self.help_button.update(self.screen, self.cursor)
                self.credits_button.update(self.screen, self.cursor)

            elif self.screen_state == "select_difficulty":  # battle mode screen graphics
                self.easy_button.update(self.screen, self.cursor)
                self.regular_button.update(self.screen, self.cursor)
                self.hard_button.update(self.screen, self.cursor)
                self.menu_button.update(self.screen, self.cursor)
                self.next_window_button.update(self.screen, self.cursor)

            elif self.screen_state == "player":  # battle name screen graphics
                self.menu_button.update(self.screen, self.cursor)
                self.game_button.update(self.screen, self.cursor)
                text = tools.PfefferMediaeval_font.render(self.name_text, True, tools.ink_color)  # battle's name text
                self.screen.blit(text, (132, 338))

            elif self.screen_state == "game":  # decides to create or load game
                if not self.game:
                    self.game = game.Game(self.name_text,self.screen, self.difficulty, self.gems, self.start_level, self)
                self.game.load_game()
                self.game.start_game()

            elif self.screen_state == "load_game":  # battle loading screen graphics
                self.menu_button.update(self.screen, self.cursor)
                self.game_button.update(self.screen, self.cursor)
                # --- battle's information ---
                battlename = tools.Insula_font_28.render(self.battlename, True, tools.blood_color)
                self.screen.blit(battlename, (130, 315))
                battlemode = tools.Insula_font_14.render(self.battlemode, True, tools.blood_color)
                self.screen.blit(battlemode, (130, 360))
                time_saved = tools.Insula_font_13.render(self.time_saved, True, tools.blood_color)
                self.screen.blit(time_saved, (345, 340))
                date_saved = tools.Insula_font_13.render(self.date_saved, True, tools.blood_color)
                self.screen.blit(date_saved, (315, 360))

            elif self.screen_state == "scores":  # best battle times screen graphics
                self.menu_button.update(self.screen, self.cursor)
                self.table.update()  # updates position table

            elif self.screen_state == "help":  # help screen graphics
                self.book_image = pygame.image.load("source/resources/gui/props/book_" + str(self.number_page) + ".png")
                self.menu_button.update(self.screen, self.cursor)
                self.screen.blit(self.book_image, (17, 175))
                self.left_button.update(self.screen, self.cursor)
                self.right_button.update(self.screen, self.cursor)

            elif self.screen_state == "credits":  # credits screen graphics
                self.menu_button.update(self.screen, self.cursor)


class Table:
    # scores display - graphic helper class , in order to receive, organize and display information on the best times
    # in secs and battle names in ascending order
    def __init__(self, screen):
        self.screen = screen
        self.labels = []
        self.create_labels()

    def load_data(self):
        # reads the player's name and the score obtained in the game in scores.txt
        file = open("source/resources/data/scores.txt", "r", encoding='utf-8')
        contents = file.read().split("\n")

        def sort_list(a, i, j, n):
            # organizes information
            if j == n:
                i = i + 1
                j = 0
            if i == n:
                return
            if a[i][1] > a[j][1]:
                temp = a[j]
                a[j] = a[i]
                a[i] = temp
                sort_list(a, i, j + 1, n)
            else:
                sort_list(a, i, j + 1, n)
            return a

        temp = []
        for element in contents:
            element = element.split(",")
            element[1] = int(element[1])
            temp.append(element)

        contents = temp
        contents = sort_list(contents, 0, 0, len(contents))
        file.close()
        return contents

    def create_labels(self):
        # creates text tag for data
        array = self.load_data()
        for i in array:
            a = tools.Insula_font_13.render(i[0], True, tools.blue)
            b = tools.Insula_font_13.render(str(i[1]), True, tools.blue)
            self.labels.append([a, b])
        self.labels = self.labels[::-1]

    def update(self):
        # display created labels
        for i in range(len(self.labels)):
            if i < 10:
                self.screen.blit(self.labels[i][0], (175, 260 + (i * 22)))
                self.screen.blit(self.labels[i][1], (275, 260 + (i * 22)))