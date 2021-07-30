import pygame as pg
from pygame.locals import *
from pytmx import *
from constants import *
from classes.Printable import Printable


class Renderer(Printable):
    """
    This object renders tile maps from Tiled
    """
    def __init__(self, game, filename, zoom=1, start_position=None, end_position=None):
        super().__init__(game, zoom, start_position, end_position)

        tm = load_pygame(filename, pixelalpha=True)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm
        self.surface = pg.Surface(self.size)

        self.current_anim_index = 0

    def handleInput(self, event):
        if hasattr(event, 'key'):
            k = event.key
        elif hasattr(event, 'value'):
            k = event.value
        elif hasattr(event, 'button'):
            k = event.button

        if event.type == KEYUP or event.type == JOYBUTTONDOWN:
            if k == CONTROL_A:
                self.game.changeState(GameState.ROOM_SELECTION)

    def update(self, frame):
        if frame in get_frequency_list(6):
            self.current_anim_index += 1

        if self.current_anim_index == 4:
            self.current_anim_index = 0

    def getSurface(self):
        for layer in self.tmx_data.visible_layers:
            for x, y, image in layer.tiles():
                for gid, props in self.tmx_data.tile_properties.items():
                    image_comp = self.tmx_data.get_tile_image_by_gid(props['frames'][0].gid)
                    if image == image_comp:
                        image = self.tmx_data.get_tile_image_by_gid(props['frames'][self.current_anim_index].gid)

                pos_x = ((x * SPRITE_BIG_WIDTH) + layer.offsetx)
                pos_y = ((y * SPRITE_BIG_HEIGHT) + layer.offsety)

                self.surface.blit(image, (pos_x, pos_y))

        return super().getSurface()
