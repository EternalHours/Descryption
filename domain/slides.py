import os
import pygame as pg
from data.const import Colour
from scripts.centre_div import centre_div

class SlidePuzzle:
    def __init__(self):
        pass
        
class SlideTile:
    images = {}
    
    def loadtilecolour(colour):
        '''Loads the tileblank with the specified colour.'''
        if colour not in SlideTile.images.keys():
            tileblank = pg.image.load(os.path.join('images', 'cardblanks', f'tile_{colour.lower()}.png'))
            Colour.images[colour] = tileblank

    def __init__(self, basecard, colour="Gold"):
        # Initialise Attributes
        self.basecard = basecard
        self.tile_colour = colour
        self.__image = None
        
    @property
    def image(self):
        if self.__image is not None: return self.__image
        SlideTile.loadtilecolour(self.tile_colour)
        tileblank = SlideTile.images[self.tile_colour]
        power, health = None, None
        width, height = tileblank.get_size()
        if isinstance(self.basecard.power, int):
            font = pg.font.Font(os.path.join("fonts", "Marksman.otf"), 16)
            power = font.render(self.basecard.power)
        else: power = self.basecard.power.image
        if isinstance(self.basecard.health, int):
            font = pg.font.Font(os.path.join("fonts", "Marksman.otf"), 16)
            health = font.render(self.basecard.health)
        else: health = self.basecard.health.image
        ppos = (6, height - power.get_height() - 6)
        hpos = (width - health.get_width() - 6, height - health.get_height - 6)
        tileblank.blit(power, ppos)
        tileblank.blit(health, hpos)
        if len(self.basecard.sigils) == 1:
            sigil = self.basecard.sigils[0].image
            spos = centre_div((width, height), sigil.get_size())
            tileblank.blit(sigil, spos)
        elif len(self.basecard.sigils) > 1:
            sigils = [sigil.image for sigil in self.basecard.sigils[:2]]
            #
            # TODO rendering logic if basecard has more than 1 sigil.
            #
        self.__image = tileblank
        return tileblank
            
            