from classes.Printable import Printable
from constants import *


class Background(Printable):
    def __init__(self, game, zoom=1, start_position=None, end_position=None):
        super().__init__(game, zoom, start_position, end_position)

        self.color = BACKGROUND_COLOR_1

    def getSurface(self):
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        temp_surface = pygame.Surface((SPRITE_WIDTH * 2, SPRITE_HEIGHT * 2))

        temp_surface.blit(self.game.getSpriteById(154), (0, 0))
        temp_surface.blit(self.game.getSpriteById(155), (SPRITE_WIDTH, 0))
        temp_surface.blit(self.game.getSpriteById(218), (0, SPRITE_HEIGHT))
        temp_surface.blit(self.game.getSpriteById(219), (SPRITE_WIDTH, SPRITE_HEIGHT))

        for x in range(0, WINDOW_WIDTH, SPRITE_WIDTH * 2):
            for y in range(0, WINDOW_HEIGHT, SPRITE_HEIGHT * 2):
                self.surface.blit(temp_surface, (x, y))

        initial = (128, 37, 45)
        threshold = (0, 0, 0)

        pygame.transform.threshold(self.surface, self.surface, initial, threshold, self.color, 1, None, True)

        return super().getSurface()
