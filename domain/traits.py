import os
import pygame as pg

class TraitInfo:
    def __init__(self, trait_id, name, description, has_images=False, has_fullart_images=False):
        # Initialise Attributes:
        self.trait_id = trait_id
        self.name = name
        self.description = description
        self.has_images = has_image
        self.has_fullart_images = has_fullart_images
        self.__images = None
        self.__fullart_images
    
    @property
    def images(self):
        if not self.has_images: return None
        if self.__images is not None: return self.__image
        images = []
        path = os.path.join('images', 'cardblanks')
        name = self.name.lower().replace(' ', '')
        for file in sorted(os.listdir(path)):
            if file.startswith(name):
                image = pg.image.load(os.path.join(path, file))
                images.append(image)
        self.__images = images
        return images

    @property
    def fullart_images(self):
        if not self.has_fullart_images: return None
        if self.__fullart_images is not None: return self.__image
        images = []
        path = os.path.join('images', 'cardblanks')
        name = self.name.lower().replace(' ', '')
        for file in sorted(os.listdir(path)):
            if file.startswith('fullart_'+name):
                image = pg.image.load(os.path.join(path, file))
                images.append(image)
        self.__fullart_images = images
        return images

class Trait:
    def __init__(self, traitinfo):
        # Initialise Attributes:
        self.traitinfo = traitinfo
        self.state = 0
    
    @property
    def trait_id(self):
        return self.traitinfo.trait_id
    
    @property
    def name(self):
        return self.traitinfo.name
    
    @property
    def description(self):
        return self.traitinfo.description
    
    @property
    def has_image(self):
        return self.traitinfo.has_images
    
    @property
    def has_image(self):
        return self.traitinfo.has_fullart_images
    
    @property
    def image(self):
        return self.traitinfo.images[self.state]
    
    @property
    def image(self):
        return self.traitinfo.fullart_images[self.state]
    
    def __eq__(self, other):
        if not isinstance(other, Trait): return False
        return self.trait_id == other.trait_id
        
    def __lt__(self, other):
        if not isinstance(other, Trait): raise TypeError(f"Unrecognised type for '<': {type(other)}.")
        return self.trait_id < other.trait_id

class TraitRepo:
    '''Repository for TraitInfo objects.'''
    
    def __init__(self):
        # Initialise Attributes:
        self.traits = []
        
    def find_trait_by_name(self, name):
        for trait in self.traits:
            if trait.name == name: return trait
        return None
        
    def find_trait_by_id(self, trait_id):
        for trait in self.traits:
            if trait.trait_id == trait_id: return trait
        return None

class TraitGroup:
    '''Collection of Trait objects.'''

    def __init__(self, traits):
        # Initialise Attributes:
        self.__traits = {}
        self.__cardblank = None
        # Then do:
        self.traits = traits
    
    @property
    def traits(self): return self.__traits
    
    @traits.setter
    def traits(self, traits):
        try:
            self.__traits = {}
            for trait in traits: self.add_trait(trait)
        except e: raise e
        
    @property
    def cardblank(self):
        '''Intensive render, avoid using often.'''
        if self.__cardblank is not None: return self.__cardblank
        images = []
        if self.is_fullart:
            if not any([trait.has_fullart_image for trait in self]): return None
            images = [trait.fullart_image for trait in self]
        elif any([trait.has_image for trait in self]):
            images = [trait.image for trait in self]
        cardblank = pg.image.load(os.path.join('images', 'cardblanks', 'default.png'))
        for image in images: cardblank.blit(image, (0, 0))
        self.__cardblank = cardblank
        return cardblank
    
    @property
    def is_fullart
        return "Full Art" in [trait.name for trait in self]
    
    def iter(self):
        return iter(sorted(self.traits))
    
    def union(self, other):
        if not isinstance(other, TraitGroup): raise TypeError(f"Cannot find union of TraitGroup with object of type {type(other)}.")
        tg = TraitGroup()
        tg.traits = self.traits.union(other.traits)
        return tg
        
    def add_trait(self, traitinfo):
        if not isinstance(other, TraitInfo): raise TypeError(f"Could not add object of type {type(other)} to TraitGroup.")
        self.__cardblank = None
        self.__traits.add(Trait(traitinfo))