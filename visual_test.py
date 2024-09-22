import os
import pygame as pg

pg.init()
window = pg.display.set_mode((200, 200))

default = pg.image.load(os.path.join('images', 'cardblanks', 'default.png'))
power = pg.font.Font(os.path.join('fonts', 'Marksman.otf'), 16).render("1", False, (0, 0, 0))
default.blit(power, (2, 56 - power.get_height()))
portrait = pg.image.load(os.path.join('images', 'portraits', 'pixelportrait_amateurmage.png'))
default.blit(portrait, (0, 1))
costs = pg.image.load(os.path.join('images', 'costs.png')).convert_alpha()
costicon = pg.Surface((26, 15), pg.SRCALPHA)
costicon.blit(costs, (-55, -49))
default.blit(costicon, (default.get_width() - costicon.get_width() -1, 0))


default = pg.transform.scale(default, (default.get_width()*3, default.get_height()*3))


window.blit(default, (10, 10))
pg.display.flip()

print(power.get_height())
