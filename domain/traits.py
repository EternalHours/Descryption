import pygame as pg

class Traits:

    def __init__(self):
        self.traits = {}
        self.visible = []
        
    def add_trait(self, name, description, imagename=False):
        '''Adds a trait with the specified name, description and cardblank to the repo. Will replace existing traits with the same name.'''
        image = None
        if imagename is not None:
            image = pg.image.load(os.path.join('images', 'cardblanks', imagename)
            visible.append(name)
        self.traits[name] = description, image
    
    def get_cardblank(self, traits, binder=None):
        '''Returns the surface to be used as a cardblank given a set of traits.'''
        # If card is rare, binder should not be None and pass the binder the card 'belongs' to.
        size = (44, 58); pos = (2, 2)
        if binder is None:
            size = (42, 56)
            pos = (0, 0)
        cardblank = pg.Surface(size, pg.SRCALPHA)
        for trait in visible:
            if trait in traits: cardblank.blit(image, pos)
        return cardblank