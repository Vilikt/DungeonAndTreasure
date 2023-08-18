from classes.Printable import Printable
from constants import PrintableNames as Pn
from constants import *


class Side(Printable):
    def __init__(self, game, zoom=1, start_position=None, end_position=None):
        super().__init__(game, zoom, start_position, end_position)

        self.total_width_in_sprites = 10

    def getSurface(self):
        self.surface = self.getBorderSurface()
        self.surface.blit(self.getText(), (SPRITE_WIDTH, SPRITE_HEIGHT))

        return super().getSurface()

    def getBorderSurface(self):
        width = int((WINDOW_WIDTH - self.game.getPrintable(Pn.DUNGEON).getSurface().get_width()) / self.zoom)
        height = int((self.game.getPrintable(Pn.DUNGEON).getSurface().get_height()) / self.zoom)

        surface = pygame.Surface(
            (width, height)
        )

        surface.fill(TRANSPARENCY)

        # Corner up left
        surface.blit(self.game.getSpriteById(1052), (0, 0))
        # Corner up right
        surface.blit(self.game.getSpriteById(1055), (width - SPRITE_WIDTH, 0))
        # Corner down left
        surface.blit(self.game.getSpriteById(1244), (0, height - SPRITE_HEIGHT))
        # Corner down right
        surface.blit(
            self.game.getSpriteById(1247),
            (width - SPRITE_WIDTH, height - SPRITE_HEIGHT)
        )

        line_up = 1053
        line_down = 1245
        vert_left = 1116
        vert_right = 1119

        # width
        for x in range(SPRITE_WIDTH, width - SPRITE_WIDTH, SPRITE_WIDTH):
            surface.blit(self.game.getSpriteById(line_up), (x, 0))
            surface.blit(self.game.getSpriteById(line_down), (x, height - SPRITE_HEIGHT))

        # height
        for y in range(SPRITE_HEIGHT, height - SPRITE_HEIGHT, SPRITE_HEIGHT):
            surface.blit(self.game.getSpriteById(vert_left), (0, y))
            surface.blit(self.game.getSpriteById(vert_right), (width - SPRITE_WIDTH, y))

        return surface

    def getText(self):
        police = self.game.getPrintable(Pn.TEXT_ZONE).police
        player = self.game.getPrintable(Pn.PLAYER)

        width = int((WINDOW_WIDTH - self.game.getPrintable(Pn.DUNGEON).getSurface().get_width() - 2 * SPRITE_WIDTH * self.zoom) / self.zoom)
        height = int((self.game.getPrintable(Pn.DUNGEON).getSurface().get_height() - 2 * SPRITE_HEIGHT * self.zoom) / self.zoom)

        surface = pygame.Surface(
            (width, height)
        )

        surface.fill(COLOR_MAP_BG)

        full_heart = self.game.getSpriteById(1152)
        empty_heart = self.game.getSpriteById(1154)

        for x in range(player.life):
            surface.blit(full_heart, (2 + (x * SPRITE_WIDTH), 0))

        # for x in range(player.max_move - 4, PLAYER_MAX_MOVE - 4):
        for x in range(player.life, PLAYER_MAX_LIFE):
            surface.blit(empty_heart, (2 + x * SPRITE_WIDTH, 0))

        moves_surf = police.render('Mvt:' + str(player.rest_of_move), False, COLOR_BLACK)
        surface.blit(moves_surf, (2, SPRITE_HEIGHT + 2))

        if player.got_treasure:
            surface.blit(self.game.getSpriteById(208, 'overworldL'), (2, (SPRITE_HEIGHT + 2) * 2))

        return surface
