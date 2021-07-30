from enum import Enum, auto
import classes.ConfigHandler as Ch
import pygame

config = Ch.ConfigHandler()

# SPRITES
SPRITE_WIDTH = 8
SPRITE_HEIGHT = 8
SPRITE_BIG_WIDTH = 16
SPRITE_BIG_HEIGHT = 16

# ENVIRONMENT
FPS = 60
FREQUENCY = 10
FPS_RATIO = int(FPS / FREQUENCY)
SCALE = int(config.get('SCALE'))
TEXT_SIZE = 6
WINDOW_WIDTH = int(config.get('WINDOW_WIDTH'))
WINDOW_HEIGHT = int(config.get('WINDOW_HEIGHT'))
WINDOW_WIDTH_SCALED = WINDOW_WIDTH * SCALE
WINDOW_HEIGHT_SCALED = WINDOW_HEIGHT * SCALE

# PLAYER
PLAYER_MAX_MOVE = 8

# DUNGEON
DUNGEON_MAX_WIDTH = int(config.get('DUNGEON_MAX_WIDTH'))
DUNGEON_MAX_HEIGHT = int(config.get('DUNGEON_MAX_HEIGHT'))
DUNGEON_MIN_DISTANCE_BTW_P_AND_D = int(config.get('DUNGEON_MIN_DISTANCE_BTW_P_AND_D'))
DUNGEON_MIN_DISTANCE_DRAG_AWAKE = int(config.get('DUNGEON_MIN_DISTANCE_DRAG_AWAKE'))
DUNGEON_MAX_NBR_WALLS = int(config.get('DUNGEON_MAX_NBR_WALLS')) #(DUNGEON_MAX_WIDTH - 1) * (DUNGEON_MAX_HEIGHT - 1)

# COLORS
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_MAP_BG = (192, 192, 176)
COLOR_TEXT = COLOR_MAP_BG
COLOR_PLAYER_ROOM = (72, 160, 120)
COLOR_TREASURE_ROOM = (184, 144, 80)
COLOR_WALL_UNSEEN = (187, 90, 97)
TRANSPARENCY = (255, 0, 255)
BGCOLOR = COLOR_BLACK
BACKGROUND_COLOR_1 = (128, 37, 45)
BACKGROUND_COLOR_2 = (37, 115, 128)
BACKGROUND_COLOR_3 = (37, 128, 85)
BACKGROUND_COLOR_4 = (129, 70, 37)
BACKGROUND_COLOR_5 = (82, 37, 128)

# CONTROLS
try:
    temp = config.get('CONTROL_UP').replace('(', '').replace(')', '')
    CONTROL_UP = tuple(map(int, temp.split(', ')))
except (ValueError, AttributeError):
    CONTROL_UP = int(config.get('CONTROL_UP'))

try:
    temp = config.get('CONTROL_DOWN').replace('(', '').replace(')', '')
    CONTROL_DOWN = tuple(map(int, temp.split(', ')))
except (ValueError, AttributeError):
    CONTROL_DOWN = int(config.get('CONTROL_DOWN'))

try:
    temp = config.get('CONTROL_LEFT').replace('(', '').replace(')', '')
    CONTROL_LEFT = tuple(map(int, temp.split(', ')))
except (ValueError, AttributeError):
    CONTROL_LEFT = int(config.get('CONTROL_LEFT'))

try:
    temp = config.get('CONTROL_RIGHT').replace('(', '').replace(')', '')
    CONTROL_RIGHT = tuple(map(int, temp.split(', ')))
except (ValueError, AttributeError):
    CONTROL_RIGHT = int(config.get('CONTROL_RIGHT'))

CONTROL_A = int(config.get('CONTROL_A'))
CONTROL_B = int(config.get('CONTROL_B'))

# TEXT ZONE
TEXT_ZONE_HEIGHT_SPRITE = 5

# TEXTS
TEXT_YES = config.getL('TEXT_YES')
TEXT_NO = config.getL('TEXT_NO')
TEXT_HINT_CHOOSE_START_ROOM = config.getL('TEXT_HINT_CHOOSE_START_ROOM')
TEXT_Q_SURE = config.getL('TEXT_Q_SURE')
TEXT_DRAGON_PLACE = config.getL('TEXT_DRAGON_PLACE')
TEXT_DRAGON_TURN = config.getL('TEXT_DRAGON_TURN')
TEXT_DRAGON_AWAKE = config.getL('TEXT_DRAGON_AWAKE')
TEXT_DRAGON_ATTACK = config.getL('TEXT_DRAGON_ATTACK')
TEXT_TREASURE_FOUND = config.getL('TEXT_TREASURE_FOUND')
TEXT_TREASURE_TAKE = config.getL('TEXT_TREASURE_TAKE')
TEXT_WIN = config.getL('TEXT_WIN')
TEXT_LOSE = config.getL('TEXT_LOSE')
TEXT_NEED_CONFIG_CONTROLS_A = config.getL('TEXT_NEED_CONFIG_CONTROLS_A')
TEXT_NEED_CONFIG_CONTROLS_B = config.getL('TEXT_NEED_CONFIG_CONTROLS_B')
TEXT_NEED_CONFIG_CONTROLS_UP = config.getL('TEXT_NEED_CONFIG_CONTROLS_UP')
TEXT_NEED_CONFIG_CONTROLS_DOWN = config.getL('TEXT_NEED_CONFIG_CONTROLS_DOWN')
TEXT_NEED_CONFIG_CONTROLS_LEFT = config.getL('TEXT_NEED_CONFIG_CONTROLS_LEFT')
TEXT_NEED_CONFIG_CONTROLS_RIGHT = config.getL('TEXT_NEED_CONFIG_CONTROLS_RIGHT')

# CUSTOM EVENT
PLAYER_TURN_FINISHED = pygame.USEREVENT + 1
PLAYER_BLOCK = pygame.USEREVENT + 2
DRAGON_TURN_FINISHED = pygame.USEREVENT + 3
REFRESH_PLAYER_MOVE = pygame.USEREVENT + 4
END_TRANSLATION = pygame.USEREVENT + 5
PLAYER_DRAGON_ENCOUNTER = pygame.USEREVENT + 6
HURT_PLAYER = pygame.USEREVENT + 7
RESTART_GAME = pygame.USEREVENT + 8
TEXT_ZONE_DISMISS = pygame.USEREVENT + 9
TEXT_ZONE_ANSWER_YES = pygame.USEREVENT + 10
TEXT_ZONE_ANSWER_NO = pygame.USEREVENT + 11
TEXT_ZONE_SHOW = pygame.USEREVENT + 12


class AutoName(Enum):
    def _generate_next_value_(self, start, count, last_values):
        return self


class Sounds(AutoName):
    CURSOR = auto()
    SELECT = auto()
    TEXT_DONE = auto()
    LETTER = auto()
    WALL = auto()
    DRAGON_FLY = auto()
    DRAGON_AWAKE = auto()
    HURT_PLAYER = auto()
    TELEPORT_PLAYER = auto()
    WALK_PLAYER = auto()
    FOUND_TREASURE = auto()
    GET_ITEM = auto()
    WIN = auto()
    BOUNCE = auto()


class Direction(AutoName):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class WallStates(AutoName):
    OPEN = auto()
    CLOSED = auto()
    UNSEEN = auto()


class GameState(AutoName):
    TITLE = auto()
    ROOM_SELECTION = auto()
    INITIALISATION = auto()
    PLAY = auto()
    PAUSE = auto()
    TEXT_DISPLAY = auto()
    CONFIG_CONTROLS = auto()


class TextZoneReturn(AutoName):
    NOT_VISIBLE = auto()
    END_OF_TEXT = auto()
    DISPLAYING = auto()
    YES = auto()
    NO = auto()


class PrintableNames(AutoName):
    TITLE_SCREEN = auto()
    TEXT_ZONE = auto()
    BACKGROUND = auto()
    DUNGEON = auto()
    CURSOR = auto()
    PLAYER = auto()
    DRAGON = auto()
    SIDE = auto()


class DoNow(AutoName):
    SET_PLAYER_START_ROOM = auto()
    SET_PLAY_STATE = auto()
    MOVE_DRAGON = auto()
    AWAKE_DRAGON = auto()
    HURT_PLAYER = auto()
    TAKE_TREASURE = auto()
    END_WIN = auto()
    END_LOSE = auto()
    REDO_TRANSLATION = auto()
    SET_BUTTON_A = auto()
    SET_BUTTON_B = auto()
    SET_BUTTON_UP = auto()
    SET_BUTTON_DOWN = auto()
    SET_BUTTON_LEFT = auto()
    SET_BUTTON_RIGHT = auto()


def getFrequencyList(freq):
    global FPS

    ret = []
    for i in range(0, FPS, int(FPS / freq)):
        ret.append(i)

    return ret
