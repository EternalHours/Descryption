import os
import pygame as pg

def separate_spritesheet(path, sprite_size, m=1):
    '''Assumes all spritesheets have margins of 1 px between sprites and against edges.'''
    path = os.path.join('images', path)
    sheet = pg.image.load(path).convert_alpha()
    X, Y = sheet.get_width(), sheet.get_height()
    x, y = sprite_size
    i = m; j = m
    sprites = []
    while j < Y:
        while i < X:
            sprite = pg.Surface(sprite_size, pg.SRCALPHA)
            sprite.blit(sheet, (-i, -j))
            sprites.append(sprite)
            i += x + m
        j += y + m
        i = m
    return sprites