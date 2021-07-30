import pygame.sprite


class SpriteOfSpritesSheet(pygame.sprite.Sprite):
    def __init__(self, image, ID, line, col):
        pygame.sprite.Sprite.__init__(self)

        self.image = image

        self.ID = ID
        self.line = line
        self.col = col
