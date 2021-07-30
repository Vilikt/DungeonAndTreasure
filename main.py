import sys
from pygame.locals import *  # import pygame constant, like KEYUP, K_ESCAPE for examples
from classes.Game import *
from constants import config

"""
This is the main entry of the game. The game loop is wrote at the end.
The main mechanic is based on 4 functions. It is near from PICO-8 system.
On the main function, _init() is first executed for only one time.
Then, in the game loop, the other three functions _handleInputs(), _update() and _draw() are successively executed.
"""

assert WINDOW_WIDTH_SCALED % 8 == 0, "The width of the screen must be a multiple of 8"
assert WINDOW_HEIGHT_SCALED % 8 == 0, "The height of the screen must be a multiple of 8"
assert DUNGEON_MAX_WIDTH > 0, "The width of the Dungeon (map) must be greater than 0"
assert DUNGEON_MAX_HEIGHT > 0, "The height of the Dungeon (map) must be greater than 0"
assert DUNGEON_MAX_NBR_WALLS <= (DUNGEON_MAX_WIDTH - 1) * (DUNGEON_MAX_HEIGHT - 1), "DUNGEON_NBR_WALLS is too high. " \
                                                                                    "All " \
                                                                                    "rooms must be accessible "

# pygame and global elements initialisation
pygame.init()

CURRENT_FRAME = 0
FPSCLOCK = pygame.time.Clock()
WINDOW = pygame.display.set_mode((WINDOW_WIDTH_SCALED, WINDOW_HEIGHT_SCALED))
JOYSTICKS = None
GAME = Game()


def _init():
    global GAME

    initJoystick()

    pygame.display.set_caption('Dungeon & Treasure')

    if not config.needConfigControls:
        GAME.changeState(GameState.TITLE)
    else:
        GAME.changeState(GameState.CONFIG_CONTROLS)


def initJoystick():
    global JOYSTICKS

    # Create a list of available joysticks and initialize them.
    JOYSTICKS = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for joystick in JOYSTICKS:
        joystick.init()


def _update():
    global CURRENT_FRAME

    CURRENT_FRAME += 1
    if CURRENT_FRAME > FPS:
        CURRENT_FRAME = 0

    GAME.update(CURRENT_FRAME)
    pygame.display.flip()
    FPSCLOCK.tick(FPS)


def _draw():
    game_surface = GAME.getSurface()
    game_surface = pygame.transform.scale(game_surface, (WINDOW_WIDTH_SCALED, WINDOW_HEIGHT_SCALED))
    WINDOW.fill(COLOR_BLACK)
    WINDOW.blit(game_surface, (GAME.offset_x, GAME.offset_y))


def _handleEvents():
    global CURRENT_FRAME, GAME, JOYSTICKS

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == RESTART_GAME:
            GAME = Game()
            GAME.changeState(GameState.TITLE)
        else:
            GAME.handleEvents(event)


def main():
    _init()

    while True:
        _handleEvents()
        _update()
        _draw()


if __name__ == '__main__':
    main()
