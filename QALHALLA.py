import pygame

import source.classes.menu as menu

if __name__ == '__main__':
    game = menu.MenuScreen()
    game.start_game()
    pygame.quit()


