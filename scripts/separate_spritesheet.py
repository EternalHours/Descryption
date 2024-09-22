import pygame as pg

def separate_spritesheet(self, path, sprite_size):
    '''Assumes all spritesheets have margins of 1 px between sprites and against edges.'''
    path = os.path.join('images', path)
    sheet = pg.image.load(path).convert_alpha()
    X, Y = sheet.get_width(), sheet.get_height()
    x, y = sprite_size
    i = 1; j = 1
    sprites = []
    while j < X:
        while i < Y:
            sprite = pg.Surface(sprite_size, pg.SRCALPHA)
            sprite.blit(sheet, (-i, -j))
            sprites.append(sprite)
            i += x + 1
        j += y + 1
        i = 1
    return sprites