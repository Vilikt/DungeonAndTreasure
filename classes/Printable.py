from constants import *
import copy


class Printable:
    def __init__(self, game, zoom=1, start_position=None, end_position=None):
        self.game = game
        # each pixel of printable is multiply by zoom, so 8x8 sprite takes actually (8*ZOOM)x(8*ZOOM) pixels
        self.zoom = zoom
        self.surface = None
        self.visible = False
        if start_position is None:
            self.position = [0, 0]
        else:
            self.position = start_position
        if end_position is None:
            self.end_position = self.position
        else:
            self.end_position = end_position
        self.start_position = self.position
        self.offset = [0, 0]
        self.translate_x = ''
        self.translate_y = ''
        self.animation_speed = 1
        self.in_motion = False
        self.freeze = False
        self.do_after = None
        self.sprite_width = SPRITE_WIDTH * zoom
        self.sprite_height = SPRITE_HEIGHT * zoom

    def setScreenPosition(self, start_position, offset=None):
        if offset is not None:
            self.offset = offset

        self.position = start_position

    def getScreenPosition(self, withOffset=True):
        position = self.position

        if withOffset:
            position[0] = self.offset[0]
            position[1] = self.offset[1]

        return position

    def updateScreenPosition(self):
        self.setScreenPosition(self.position)

    def handleInput(self, event):
        return

    def update(self, frame):
        if self.in_motion:
            self.moveIfNeeded()

    def getSurface(self):
        self.surface.set_colorkey(TRANSPARENCY)

        surface = pygame.transform.scale(
            self.surface,
            (self.surface.get_width() * self.zoom, self.surface.get_height() * self.zoom)
        )

        return surface

    def initialiseTranslation(self, translate_x, translate_y, start, end, animation_speed=1, doAfter=None):
        self.in_motion = True
        self.translate_x = translate_x
        self.translate_y = translate_y
        self.end_position = end
        self.position = start
        self.start_position = copy.copy(start)
        self.animation_speed = animation_speed
        self.do_after = doAfter

    def redoTranslation(self):
        self.position = copy.copy(self.start_position)
        self.in_motion = True

    def moveIfNeeded(self):
        moved = False

        if self.translate_x == Direction.RIGHT and (self.position[0] < self.end_position[0]):
            self.position[0] += self.animation_speed
            moved = True
        if self.translate_x == Direction.LEFT and (self.position[0] > self.end_position[0]):
            self.position[0] -= self.animation_speed
            moved = True
        if self.translate_y == Direction.UP and (self.position[1] > self.end_position[1]):
            self.position[1] -= self.animation_speed
            moved = True
        if self.translate_y == Direction.DOWN and (self.position[1] < self.end_position[1]):
            self.position[1] += self.animation_speed
            moved = True

        if not moved:
            self.in_motion = False
            event = pygame.event.Event(END_TRANSLATION, doNow=self.do_after, printable=self)
            pygame.event.post(event)
            self.position = self.end_position
