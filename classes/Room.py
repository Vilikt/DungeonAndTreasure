import pygame
from constants import PrintableNames as Pn
from constants import *


class Room:
    def __init__(self, dungeon, number):
        self.dungeon = dungeon
        self.number = number

        self.line = 0
        self.col = 0

        self.color = COLOR_BLACK

        # Walls states
        self.wall_up = WallStates.CLOSED
        self.wall_down = WallStates.CLOSED
        self.wall_left = WallStates.CLOSED
        self.wall_right = WallStates.CLOSED

        self.wall_up_actual = WallStates.UNSEEN
        self.wall_down_actual = WallStates.UNSEEN
        self.wall_left_actual = WallStates.UNSEEN
        self.wall_right_actual = WallStates.UNSEEN

        self.room_up = None
        self.room_down = None
        self.room_left = None
        self.room_right = None

        self.visited = False

    def getSurface(self):
        dragon = self.dungeon.game.getPrintable(Pn.DRAGON)
        player = self.dungeon.game.getPrintable(Pn.PLAYER)

        if not self.visited:
            return self.dungeon.game.getSpriteById(230)
        elif dragon.start_room is not None:
            if self.number == dragon.start_room.number and self.dungeon.treasure_discovered and not player.got_treasure:
                return self.dungeon.game.getSpriteById(808)

        surface = pygame.Surface((SPRITE_WIDTH, SPRITE_HEIGHT))

        pygame.draw.rect(surface, COLOR_MAP_BG, (0, 0, SPRITE_WIDTH, SPRITE_HEIGHT))
        pygame.draw.rect(surface, self.color, (1, 1, SPRITE_WIDTH - 2, SPRITE_HEIGHT - 2))

        if self.wall_up_actual == WallStates.OPEN:
            pygame.draw.line(surface, COLOR_BLACK, (3, 0), (4, 0))
        elif self.wall_up_actual == WallStates.UNSEEN:
            pygame.draw.line(surface, COLOR_WALL_UNSEEN, (3, 0), (4, 0))

        if self.wall_down_actual == WallStates.OPEN:
            pygame.draw.line(surface, COLOR_BLACK, (3, 7), (4, 7))
        elif self.wall_down_actual == WallStates.UNSEEN:
            pygame.draw.line(surface, COLOR_WALL_UNSEEN, (3, 7), (4, 7))

        if self.wall_left_actual == WallStates.OPEN:
            pygame.draw.line(surface, COLOR_BLACK, (0, 3), (0, 4))
        elif self.wall_left_actual == WallStates.UNSEEN:
            pygame.draw.line(surface, COLOR_WALL_UNSEEN, (0, 3), (0, 4))

        if self.wall_right_actual == WallStates.OPEN:
            pygame.draw.line(surface, COLOR_BLACK, (7, 3), (7, 4))
        elif self.wall_right_actual == WallStates.UNSEEN:
            pygame.draw.line(surface, COLOR_WALL_UNSEEN, (7, 3), (7, 4))

        return surface

    def isSideRevealed(self, direction):
        state_actual = None
        state = None

        if direction == Direction.UP:
            state_actual = self.wall_up_actual
            state = self.wall_up
        elif direction == Direction.DOWN:
            state_actual = self.wall_down_actual
            state = self.wall_down
        elif direction == Direction.LEFT:
            state_actual = self.wall_left_actual
            state = self.wall_left
        elif direction == Direction.RIGHT:
            state_actual = self.wall_right_actual
            state = self.wall_right

        return state_actual == state

    def revealSide(self, direction):
        if direction == Direction.UP:
            self.wall_up_actual = self.wall_up
            self.room_up.wall_down_actual = self.room_up.wall_down
        elif direction == Direction.DOWN:
            self.wall_down_actual = self.wall_down
            self.room_down.wall_up_actual = self.room_down.wall_up
        elif direction == Direction.LEFT:
            self.wall_left_actual = self.wall_left
            self.room_left.wall_right_actual = self.room_left.wall_right
        elif direction == Direction.RIGHT:
            self.wall_right_actual = self.wall_right
            self.room_right.wall_left_actual = self.room_right.wall_left

    def isARoomOnDirection(self, direction):
        if direction == Direction.UP:
            return self.room_up is not None
        elif direction == Direction.DOWN:
            return self.room_down is not None
        elif direction == Direction.LEFT:
            return self.room_left is not None
        elif direction == Direction.RIGHT:
            return self.room_right is not None
