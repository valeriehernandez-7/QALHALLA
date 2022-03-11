import source.classes.menu as menu

import pygame

if __name__ == '__main__':
    game = menu.MenuScreen()
    game.start_game()
    pygame.quit()