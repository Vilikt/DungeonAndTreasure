from pygame.constants import *
from classes.Printable import Printable
from constants import *
from constants import PrintableNames as Pn
from constants import DoNow as Dn
from constants import GameState as Gs


class Player(Printable):
    def __init__(self, game, zoom=1, start_position=None, end_position=None):
        super().__init__(game, zoom, start_position, end_position)

        self.sprite_index = 0
        self.actual_room = None
        self.max_move = PLAYER_MAX_MOVE
        self.rest_of_move = self.max_move
        self.life = PLAYER_MAX_LIFE
        self.start_room = None

        self.sprites = {
            0: self.game.getSpriteById(556),
            1: self.game.getSpriteById(557)
        }

        self.got_treasure = False

    def setPlayerStartRoom(self):
        cursor = self.game.getPrintable(Pn.CURSOR)

        self.start_room = cursor.actual_room
        self.start_room.visited = True
        self.start_room.color = COLOR_PLAYER_ROOM
        self.actual_room = cursor.actual_room

    def hurt(self):
        self.max_move -= 2
        self.life -= 1
        self.rest_of_move = self.max_move
        if self.life > 0:
            self.game.sounds[Sounds.TELEPORT_PLAYER].play()
            self.actual_room = self.start_room
        else:
            self.actual_room = None
            self.visible = False
        self.got_treasure = False

    def handleInput(self, event):
        if hasattr(event, 'key'):
            k = event.key
        elif hasattr(event, 'button'):
            k = event.button
        elif hasattr(event, 'value'):
            k = event.value

        if k == CONTROL_UP:
            if self.whatIsOnPlayerDirection(Direction.UP) == WallStates.OPEN:
                self.processMovePlayer(Direction.UP)
            elif self.whatIsOnPlayerDirection(Direction.UP) == WallStates.CLOSED:
                if not self.isOnPlayerDirectionRevealed(Direction.UP):
                    self.processBlockPlayer(Direction.UP)
                else:
                    self.game.sounds[Sounds.BOUNCE].play()
        elif k == CONTROL_DOWN:
            if self.whatIsOnPlayerDirection(Direction.DOWN) == WallStates.OPEN:
                self.processMovePlayer(Direction.DOWN)
            elif self.whatIsOnPlayerDirection(Direction.DOWN) == WallStates.CLOSED:
                if not self.isOnPlayerDirectionRevealed(Direction.DOWN):
                    self.processBlockPlayer(Direction.DOWN)
                else:
                    self.game.sounds[Sounds.BOUNCE].play()
        elif k == CONTROL_LEFT:
            if self.whatIsOnPlayerDirection(Direction.LEFT) == WallStates.OPEN:
                self.processMovePlayer(Direction.LEFT)
            elif self.whatIsOnPlayerDirection(Direction.LEFT) == WallStates.CLOSED:
                if not self.isOnPlayerDirectionRevealed(Direction.LEFT):
                    self.processBlockPlayer(Direction.LEFT)
                else:
                    self.game.sounds[Sounds.BOUNCE].play()
        elif k == CONTROL_RIGHT:
            if self.whatIsOnPlayerDirection(Direction.RIGHT) == WallStates.OPEN:
                self.processMovePlayer(Direction.RIGHT)
            elif self.whatIsOnPlayerDirection(Direction.RIGHT) == WallStates.CLOSED:
                if not self.isOnPlayerDirectionRevealed(Direction.RIGHT):
                    self.processBlockPlayer(Direction.RIGHT)
                else:
                    self.game.sounds[Sounds.BOUNCE].play()
        elif k == CONTROL_B:
            event = pygame.event.Event(PLAYER_TURN_FINISHED)
            pygame.event.post(event)

    def update(self, frame):
        if frame in get_frequency_list(10):
            self.sprite_index += 1

        if self.sprite_index == 2:
            self.sprite_index = 0

        self.updateScreenPosition()

        super().update(frame)

    def getSurface(self):
        self.surface = pygame.Surface((SPRITE_WIDTH, SPRITE_HEIGHT))

        self.surface.blit(self.sprites[self.sprite_index], (0, 0))

        return super().getSurface()

    def updateScreenPosition(self):
        if self.game.isOnStateOrOnTextWith(Gs.ROOM_SELECTION):
            position = (self.actual_room.col * self.sprite_width, self.actual_room.line * self.sprite_height)
            self.setScreenPosition(position)
        elif self.game.isOnStateOrOnTextWith(Gs.INITIALISATION) or self.game.isOnStateOrOnTextWith(Gs.PLAY):
            dungeon = self.game.getPrintable(Pn.DUNGEON)
            position = (
                self.actual_room.col * self.sprite_width + 2 * self.sprite_width,
                self.actual_room.line * self.sprite_height + 2 * self.sprite_height
            )
            offset = (
                dungeon.position[0] - self.sprite_width,
                dungeon.position[1] - self.sprite_height
            )
            self.setScreenPosition(position, offset)
        else:
            super().updateScreenPosition()

    def whatIsOnPlayerDirection(self, direction):
        if self.actual_room.isARoomOnDirection(direction):
            if direction == Direction.UP:
                return self.actual_room.wall_up
            elif direction == Direction.DOWN:
                return self.actual_room.wall_down
            elif direction == Direction.LEFT:
                return self.actual_room.wall_left
            elif direction == Direction.RIGHT:
                return self.actual_room.wall_right

        return None

    def isOnPlayerDirectionRevealed(self, direction):
        return self.actual_room.isSideRevealed(direction)

    def processMovePlayer(self, direction):
        self.game.sounds[Sounds.WALK_PLAYER].play()

        self.actual_room.revealSide(direction)

        if direction == Direction.UP:
            self.actual_room = self.actual_room.room_up
        elif direction == Direction.DOWN:
            self.actual_room = self.actual_room.room_down
        elif direction == Direction.LEFT:
            self.actual_room = self.actual_room.room_left
        elif direction == Direction.RIGHT:
            self.actual_room = self.actual_room.room_right

        self.rest_of_move -= 1

        if self.rest_of_move == 0:
            event = pygame.event.Event(PLAYER_TURN_FINISHED)
            pygame.event.post(event)

        self.actual_room.visited = True

    def processBlockPlayer(self, direction):
        self.actual_room.revealSide(direction)
        self.rest_of_move = 0
        event = pygame.event.Event(PLAYER_BLOCK)
        pygame.event.post(event)
        self.freeze = True
        self.game.sounds[Sounds.WALL].play()

    def refreshPlayerMove(self):
        if self.got_treasure:
            self.rest_of_move = 4
        else:
            self.rest_of_move = self.max_move
