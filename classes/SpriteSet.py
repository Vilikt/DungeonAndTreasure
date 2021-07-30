import pygame

from classes.SpriteOfSpritesSheet import SpriteOfSpritesSheet
from constants import *


class SpriteSet:

    def __init__(self, sprite_set_filename, sprite_width=SPRITE_WIDTH, sprite_height=SPRITE_HEIGHT):
        self.sprite_set = pygame.image.load(sprite_set_filename)
        self.sprites = []
        self.spritesById = []

        self.sprite_width = sprite_width
        self.sprite_height = sprite_height

        sprite_id = -1
        line = -1
        for y in range(0, self.sprite_set.get_height(), sprite_height):
            line += 1
            self.sprites.insert(line, [])

            col = -1
            for x in range(0, self.sprite_set.get_width(), sprite_width):
                col += 1

                image = self.sprite_set.subsurface((x, y), (sprite_width, sprite_height))
                sprite_id += 1
                spriteOfSpritesSheet = SpriteOfSpritesSheet(image, sprite_id, line, col)

                self.sprites[line].insert(col, spriteOfSpritesSheet)
                self.spritesById.insert(sprite_id, spriteOfSpritesSheet)

    def getSprite(self, x, y):
        return self.sprites[y][x].image

    def getSpriteById(self, sprite_id):
        return self.spritesById[sprite_id].image
