import pygame.display
from pygame.locals import *
from classes.Printable import Printable
from constants import *
from constants import PrintableNames as Pn
from constants import DoNow as Dn


class Cursor(Printable):
    def __init__(self, game, zoom=1, start_position=None, end_position=None):
        super().__init__(game, zoom, start_position, end_position)

        self.sprite_index = 0
        self.actual_room = None

        self.sprites = {
            'up_left': {
                0: self.game.getSpriteById(1158),
                1: self.game.getSpriteById(1160)
            },
            'up_right': {
                0: self.game.getSpriteById(1159),
                1: self.game.getSpriteById(1161)
            },
            'down_left': {
                0: self.game.getSpriteById(1222),
                1: self.game.getSpriteById(1224)
            },
            'down_right': {
                0: self.game.getSpriteById(1223),
                1: self.game.getSpriteById(1225)
            }
        }

    def handleInput(self, event):
        if hasattr(event, 'key'):
            k = event.key
        elif hasattr(event, 'value'):
            k = event.value
        elif hasattr(event, 'button'):
            k = event.button

        if event.type == KEYUP or event.type == JOYBUTTONDOWN or event.type == JOYHATMOTION:
            if k == CONTROL_A:
                self.game.getPrintable(Pn.TEXT_ZONE).setNewText(TEXT_Q_SURE, True, Dn.SET_PLAYER_START_ROOM)
                event = pygame.event.Event(TEXT_ZONE_SHOW)
                pygame.event.post(event)
                self.game.sounds[Sounds.SELECT].play()
            elif k == CONTROL_UP and self.actual_room.room_up is not None:
                self.actual_room = self.actual_room.room_up
                self.game.sounds[Sounds.CURSOR].play()
            elif k == CONTROL_DOWN and self.actual_room.room_down is not None:
                self.actual_room = self.actual_room.room_down
                self.game.sounds[Sounds.CURSOR].play()
            elif k == CONTROL_LEFT and self.actual_room.room_left is not None:
                self.actual_room = self.actual_room.room_left
                self.game.sounds[Sounds.CURSOR].play()
            elif k == CONTROL_RIGHT and self.actual_room.room_right is not None:
                self.actual_room = self.actual_room.room_right
                self.game.sounds[Sounds.CURSOR].play()

    def update(self, frame):
        if frame in get_frequency_list(10):
            self.sprite_index += 1

        if self.sprite_index == len(self.sprites.get('up_left')):
            self.sprite_index = 0

        super().update(frame)

    def getSurface(self):
        self.surface = pygame.Surface((SPRITE_WIDTH * 2, SPRITE_HEIGHT * 2))

        self.surface.blit(self.sprites['up_left'][self.sprite_index], (0, 0))
        self.surface.blit(self.sprites['up_right'][self.sprite_index], (SPRITE_WIDTH, 0))
        self.surface.blit(self.sprites['down_left'][self.sprite_index], (0, SPRITE_HEIGHT))
        self.surface.blit(self.sprites['down_right'][self.sprite_index], (SPRITE_WIDTH, SPRITE_HEIGHT))

        return super().getSurface()

    def updateScreenPosition(self):
        if self.game.isOnStateOrOnTextWith(GameState.ROOM_SELECTION):
            dungeon = self.game.getPrintable(Pn.DUNGEON)
            position = [
                (self.actual_room.col + 1) * self.sprite_width,
                (self.actual_room.line + 1) * self.sprite_height
            ]
            offset = [
                dungeon.position[0] - (self.sprite_width / 2),
                dungeon.position[1] - (self.sprite_height / 2)
            ]
            self.setScreenPosition(position, offset)
        else:
            super().updateScreenPosition()
