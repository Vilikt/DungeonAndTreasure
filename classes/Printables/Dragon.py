import random
from classes.Printable import Printable
from constants import PrintableNames as Pn
from constants import DoNow as Dn
from constants import *


class Dragon(Printable):
    def __init__(self, game, zoom=1, start_position=None, end_position=None):
        super().__init__(game, zoom, start_position, end_position)

        self.actual_room = None
        self.start_room = None
        self.last_strike_room = None
        self.asleep = True

        self.sprites = {
            0: self.game.getSpriteById(551)
        }

    def setDragonRoom(self):
        dungeon = self.game.getPrintable(Pn.DUNGEON)
        player = self.game.getPrintable(Pn.PLAYER)

        # first we choose a  room randomly
        room = player.actual_room
        while room == player.actual_room or dungeon.getDistanceBetween(room, player.start_room) < DUNGEON_MIN_DISTANCE_BTW_P_AND_D:
            line = random.randint(0, dungeon.max_height - 1)
            col = random.randint(0, dungeon.max_width - 1)
            room = self.game.getPrintable(Pn.DUNGEON).getRoom(col=col, line=line)

        self.actual_room = self.start_room = room

    def doDragonTurn(self):
        self.game.getPrintable(Pn.TEXT_ZONE).setNewText(TEXT_DRAGON_TURN, do_on_end_text=Dn.MOVE_DRAGON)
        event = pygame.event.Event(TEXT_ZONE_SHOW)
        pygame.event.post(event)
        self.game.sounds[Sounds.DRAGON_FLY].play()

    def move(self):
        player = self.game.getPrintable(Pn.PLAYER)

        if player.actual_room is not player.start_room:
            room_to_go = player.actual_room
        else:
            room_to_go = self.start_room

        diff_width = self.actual_room.col - room_to_go.col
        diff_height = self.actual_room.line - room_to_go.line

        # Dragon and player are on the same line but not the same column
        if diff_width != 0 and diff_height == 0:
            if diff_width > 0: # Dragon is at the right of player
                # Move on Room left
                self.actual_room = self.actual_room.room_left
            else: # Dragon is at the left of player
                # Move on Room right
                self.actual_room = self.actual_room.room_right
        # Dragon and player are on the same column but not the same line
        elif diff_width == 0 and diff_height != 0:
            if diff_height > 0: # Dragon is at the down of player
                # Move on Room up
                self.actual_room = self.actual_room.room_up
            else: # Dragon is at the up of player
                # Move on Room down
                self.actual_room = self.actual_room.room_down
        elif diff_width != 0 and diff_height != 0:
            # Dragon is at Down-Right of Player
            if diff_width > 0 and diff_height > 0:
                # Move on Room up
                self.actual_room = self.actual_room.room_up
                # Move on Room left
                self.actual_room = self.actual_room.room_left
            # Dragon is at Up-Right of Player
            elif diff_width > 0 > diff_height:
                # Move on Room down
                self.actual_room = self.actual_room.room_down
                # Move on Room left
                self.actual_room = self.actual_room.room_left
            # Dragon is at Down-Left of Player
            elif diff_width < 0 < diff_height:
                # Move on Room up
                self.actual_room = self.actual_room.room_up
                # Move on Room right
                self.actual_room = self.actual_room.room_right
            # Dragon is at Up-Left of Player
            elif diff_width < 0 and diff_height < 0:
                # Move on Room down
                self.actual_room = self.actual_room.room_down
                # Move on Room right
                self.actual_room = self.actual_room.room_right

        event = pygame.event.Event(DRAGON_TURN_FINISHED)
        pygame.event.post(event)

    def getSurface(self):
        self.surface = pygame.Surface((SPRITE_WIDTH, SPRITE_HEIGHT))
        self.surface.blit(self.sprites[0], (0, 0))

        return super().getSurface()

    def updateScreenPosition(self):
        if self.game.isOnStateOrOnTextWith(GameState.PLAY) and self.last_strike_room is not None:
            position = (
                self.last_strike_room.col * self.sprite_width,
                self.last_strike_room.line * self.sprite_height
            )
            offset = (
                self.sprite_width,
                self.sprite_height
            )
            self.setScreenPosition(position, offset)
        else:
            super().updateScreenPosition()
