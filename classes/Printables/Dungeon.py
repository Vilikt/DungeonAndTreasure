import random
from classes.Printable import Printable
from classes.Room import Room
from constants import PrintableNames as Pn
from constants import DoNow as Dn
from constants import *


class Dungeon(Printable):
    def __init__(self, game, zoom=1, start_position=None, end_position=None):
        super().__init__(game, zoom, start_position, end_position)

        self.max_width = DUNGEON_MAX_WIDTH
        self.max_height = DUNGEON_MAX_HEIGHT
        self.target_wall_nbr = DUNGEON_MAX_NBR_WALLS
        self.treasure_discovered = False

        self.rooms = []

        self.create()
        self.setWalls()

    def getRoom(self, col, line):
        return self.rooms[line-1][col-1]

    def getDistanceBetween(self, room1, room2):
        if room1 is None or room2 is None:
            return None

        if room1 == room2 or (room1.col == room2.col and room1.line == room2.line):
            return 0

        if room1.col >= room2.col:
            diff_width = room1.col - room2.col
        else:
            diff_width = room2.col - room1.col

        if room1.line >= room2.line:
            diff_height = room1.line - room2.line
        else:
            diff_height = room2.line - room1.line

        return diff_width + diff_height

    def create(self):
        i = 0

        for line in range(self.max_height):
            self.rooms.insert(line, [])

            for col in range(self.max_width):
                i = i + 1

                self.rooms[line].insert(col, Room(self, i))
                self.rooms[line][col].line = line
                self.rooms[line][col].col = col

                # Close the UP side for the first line
                if line == 0:
                    self.rooms[line][col].wall_up = WallStates.CLOSED
                    self.rooms[line][col].wall_up_actual = WallStates.CLOSED

                # Close the DOWN side for the last line
                if line == self.max_height - 1:
                    self.rooms[line][col].wall_down = WallStates.CLOSED
                    self.rooms[line][col].wall_down_actual = WallStates.CLOSED

                # Close the right side for the the last column
                if col == self.max_width - 1:
                    self.rooms[line][col].wall_right = WallStates.CLOSED
                    self.rooms[line][col].wall_right_actual = WallStates.CLOSED

                # Close the left side for the the first column
                if col == 0:
                    self.rooms[line][col].wall_left = WallStates.CLOSED
                    self.rooms[line][col].wall_left_actual = WallStates.CLOSED

                if line > 0:  # we are not in the first line
                    # link room down
                    self.rooms[line - 1][col].room_down = self.rooms[line][col]
                    # link room up
                    self.rooms[line][col].room_up = self.rooms[line - 1][col]

                if col > 0:  # we are not in the first room of a line
                    # link room right
                    self.rooms[line][col - 1].room_right = self.rooms[line][col]
                    # link room left
                    self.rooms[line][col].room_left = self.rooms[line][col - 1]

    def setWalls(self):
        path = []

        # first we choose a  room randomly
        current_room_coords = (random.randint(0, self.max_height - 1), random.randint(0, self.max_width - 1))
        # we add it to the "path" table
        path.append(current_room_coords)

        # calculate the amount of walls in dungeon, sides not included (112 for an 8x8 dungeon)
        nb_of_walls = (((self.max_width * 2) - 1) * (self.max_height - 1)) + (self.max_width - 1)

        """
        We will now move from room to room.
        To choose the next room, we select one at random from the one accessible from the current room.
        A room is accessible if we have not yet passed through it.
        This is what deleteWall do.
        """

        # multiple call of deleteWall
        while current_room_coords is not None:
            nb_of_walls, current_room_coords = self.deleteWall(current_room_coords, path, nb_of_walls, False)

        while nb_of_walls != self.target_wall_nbr:
            current_room_coords = (random.randint(0, self.max_height - 1), random.randint(0, self.max_width - 1))
            nb_of_walls, current_room_number = self.deleteWall(current_room_coords, [], nb_of_walls, True)

        # Reset the "visited" to False for all rooms
        for line in range(self.max_height):
            for col in range(self.max_width):
                self.rooms[line][col].visited = False

    def deleteWall(self, current_room_coords, path, nb_of_walls, avoid_visited):
        t_directions = []
        next_current_room_coords = current_room_coords

        line = current_room_coords[0]
        col = current_room_coords[1]

        # we set room as visited
        self.rooms[line][col].visited = True

        # we get the possible directions and populate the t_directions array.
        #
        if self.rooms[line][col].room_up is not None and self.rooms[line][col].wall_up == WallStates.CLOSED and \
                (not self.rooms[line][col].room_up.visited or avoid_visited):
            t_directions.append(Direction.UP)

        if self.rooms[line][col].room_down is not None and self.rooms[line][col].wall_down == WallStates.CLOSED and \
                (not self.rooms[line][col].room_down.visited or avoid_visited):
            t_directions.append(Direction.DOWN)

        if self.rooms[line][col].room_right is not None and self.rooms[line][col].wall_right == WallStates.CLOSED and \
                (not self.rooms[line][col].room_right.visited or avoid_visited):
            t_directions.append(Direction.RIGHT)

        if self.rooms[line][col].room_left is not None and self.rooms[line][col].wall_left == WallStates.CLOSED and \
                (not self.rooms[line][col].room_left.visited or avoid_visited):
            t_directions.append(Direction.LEFT)

        if len(t_directions) >= 1:  # if there is at least one direction possible (no, not the band...)
            # we randomly choose a direction
            index = random.randint(0, len(t_directions) - 1)
            direction = t_directions[index]

            # we set the new current room number and open the wall
            if direction == Direction.UP:
                next_current_room_coords = (self.rooms[line][col].room_up.line, self.rooms[line][col].room_up.col)
                self.rooms[line][col].wall_up = WallStates.OPEN
                self.rooms[line][col].room_up.wall_down = WallStates.OPEN
            elif direction == Direction.DOWN:
                next_current_room_coords = (self.rooms[line][col].room_down.line, self.rooms[line][col].room_down.col)
                self.rooms[line][col].wall_down = WallStates.OPEN
                self.rooms[line][col].room_down.wall_up = WallStates.OPEN
            elif direction == Direction.LEFT:
                next_current_room_coords = (self.rooms[line][col].room_left.line, self.rooms[line][col].room_left.col)
                self.rooms[line][col].wall_left = WallStates.OPEN
                self.rooms[line][col].room_left.wall_right = WallStates.OPEN
            elif direction == Direction.RIGHT:
                next_current_room_coords = (self.rooms[line][col].room_right.line, self.rooms[line][col].room_right.col)
                self.rooms[line][col].wall_right = WallStates.OPEN
                self.rooms[line][col].room_right.wall_left = WallStates.OPEN

            nb_of_walls = nb_of_walls - 1
            path.append(next_current_room_coords)
        else:  # we come back to the last room
            if len(path) > 1:
                path.pop()  # remove last elt of path list
                next_current_room_coords = path[-1]
            else:
                next_current_room_coords = None

        return nb_of_walls, next_current_room_coords

    def update(self, frame):
        dragon = self.game.getPrintable(Pn.DRAGON)
        player = self.game.getPrintable(Pn.PLAYER)

        distance = self.getDistanceBetween(dragon.actual_room, player.actual_room)

        if distance is not None and distance <= DUNGEON_MIN_DISTANCE_DRAG_AWAKE and dragon.asleep:
            self.game.getPrintable(Pn.TEXT_ZONE).setNewText(TEXT_DRAGON_AWAKE, do_on_end_text=Dn.AWAKE_DRAGON)
            event = pygame.event.Event(TEXT_ZONE_SHOW)
            pygame.event.post(event)
            dragon.asleep = False
            self.game.sounds[Sounds.DRAGON_AWAKE].play()

        super().update(frame)

    def getSurface(self):
        self.surface = self.getMapBorderSurface()
        self.surface.blit(self.getRoomGridSurface(), (SPRITE_WIDTH, SPRITE_HEIGHT))

        return super().getSurface()

    def getMapBorderSurface(self):
        surface = pygame.Surface((SPRITE_WIDTH * (self.max_width + 2), SPRITE_HEIGHT * (self.max_height + 2)))

        # Corner up left
        surface.blit(self.game.getSpriteById(46), (0, 0))
        # Corner up right
        surface.blit(self.game.getSpriteById(51), (SPRITE_WIDTH * (self.max_width + 1), 0))
        # Corner down left
        surface.blit(self.game.getSpriteById(366), (0, SPRITE_HEIGHT * (self.max_height + 1)))
        # Corner down right
        surface.blit(self.game.getSpriteById(371),
                     (SPRITE_WIDTH * (self.max_width + 1), SPRITE_HEIGHT * (self.max_height + 1)))

        line_up = (47, 48)
        line_down = (367, 368)
        vert_left = (110, 174)
        vert_right = (115, 179)

        # width
        current_index = 0
        for x in range(self.max_width):
            surface.blit(self.game.getSpriteById(line_up[current_index]), (SPRITE_WIDTH * x + SPRITE_WIDTH, 0))
            surface.blit(self.game.getSpriteById(line_down[current_index]), (SPRITE_WIDTH * x + SPRITE_WIDTH,
                                                                             SPRITE_HEIGHT * (self.max_height + 1)))

            current_index += 1
            if current_index == len(line_up):
                current_index = 0

        # height
        current_index = 0
        for y in range(self.max_height):
            surface.blit(self.game.getSpriteById(vert_left[current_index]), (0, SPRITE_HEIGHT * y + SPRITE_HEIGHT))
            surface.blit(self.game.getSpriteById(vert_right[current_index]), (SPRITE_WIDTH * (self.max_width + 1),
                                                                              SPRITE_HEIGHT * y + SPRITE_HEIGHT))

            current_index += 1
            if current_index == len(vert_left):
                current_index = 0

        return surface

    def getRoomGridSurface(self):
        surface = pygame.Surface((SPRITE_WIDTH * self.max_width, SPRITE_HEIGHT * self.max_height))

        for lineOfRooms in self.rooms:
            for room in lineOfRooms:
                surface.blit(room.getSurface(), [room.col * SPRITE_HEIGHT, room.line * SPRITE_WIDTH])

        return surface
