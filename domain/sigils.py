import importlib
import pygame as pg
from scripts.separate_spritesheet import separate_spritesheet

class SigilInfo:
	def __init__(self, sigil_id, name, scrybes, description, triggers, is_mox, is_conduit, is_active, has_mirror, can_stack):
        # Initialise Attributes:
        def func(*args): pass
        self.sigil_id = sigil_id
        self.name = name
        self.scrybes = scrybes
        self.description = description
        self.effects = {trigger: func for trigger in triggers}
        self.is_mox = is_mox
        self.is_conduit = is_conduit
        self.is_active = is_active
        self.has_mirror = has_mirror
        self.can_stack = can_stack
        # Import Sigil Effects:
        self.load_effects()
        self.image = None
        self.mirrored = None
    
    @property
    def triggers(self): return set(self.effects.keys())
    
    def load_effects(self):
        sigil = importlib.import_module(f"scripts.sigils.{self.name.lower().replace(" ", "_")}')
        for trigger in self.triggers:
            self.effects[trigger] = getattr(sigil, "on_"+trigger)
    
class RepoSearchSigil:
    def __init__(self):
        self.sigil_id = None
        self.name = None
        self.scrybes = None
        self.triggers = None
        self.is_mox = None
        self.is_conduit = None
        self.is_active = None
        self.has_mirror = None
        self.can_stack = None

    def __req__(self, other):
        if not isinstance(other, SigilInfo): raise TypeError(f"Unsupported types for '=': {type(other)} and {type(self)}")
        attributes = {'sigil_id', 'name', 'scrybes', 'triggers', 'is_mox', 'is_conduit', 'has_mirror', 'can_stack'}
        for attribute in attributes:
            this = getattr(self, attribute)
            that = getattr(other, attribute)
            if this is not None and this != that: return False
        return True
        
    def __rle__(self, other):
        # Note that this takes the form: other <= self so the logic is inverted.
        if not isinstance(other, SigilInfo): raise TypeError(f"Unsupported types for '<=': {type(other)} and {type(self)}")
        attributes = {'sigil_id', 'name', 'scrybes', 'triggers'}
        for attribute in attributes:
            this = getattr(self, attribute)
            that = getattr(other, attribute)
            if this is not None:
                if isinstance(this, set) and this.issubset(that): return False
                elif this < that: return False

    def __rge__(self, other):
        # Note that this takes the form: other >= self so the logic is inverted.
        if not isinstance(other, SigilInfo): raise TypeError(f"Unsupported types for '>=': {type(other)} and {type(self)}")
        attributes = {'sigil_id', 'name', 'scrybes', 'triggers'}
        for attribute in attributes:
            this = getattr(self, attribute)
            that = getattr(other, attribute)
            if this is not None:
                if isinstance(this, set) and this.issuperset(that): return False
                elif this > that: return False

class SigilRepo:
    def __init__(self):
        self.sigils = []
    
    def find_by_id(self, sigil_id):
        '''Returns a sigil with the given id. Returns None if none exists.'''
        # For use when loading from save.
        for sigil in self.sigils:
            if sigil.sigil_id == sigil_id: return sigil
        return None
        
    def find_by_name(self, sigil_name):
        '''Returns a sigil with the given name. Returns None if none exists.'''
        # For use when initialising from spreadsheet data.
        for sigil in self.sigils:
            if sigil.name == sigil_name: return sigil
        return None
    
    def __get_search_sigil(self, kwargs):
        '''Use to convert dictionary of kwargs into a RepoSearchCard object.'''
        attributes = {'sigil_id', 'name', 'scrybes', 'triggers', 'is_mox', 'is_conduit', 'has_mirror', 'can_stack'}
        rss = RepoSearchSigil()
        for kwarg in kwargs:
            if kwarg not in attributes: raise KeyError(f"Unrecognised attribute of RepoSearchSigil: '{kwarg}'.")
            setattr(self, kwarg, kwargs[kwarg])
        return rss
    
    def match_to(self, **kwargs):
        '''Use to poll the repo for all sigils which exactly match the specified criteria.'''
        results = []
        rscs = self.__get_search_sigil(kwargs)
        for sigil in self.sigil:
            if sigil == rss: results.append(sigil)
        sr = SigilRepo()
        sr.sigils = results
        return rs
        
    def exclude(self, **kwargs):
        '''Use to poll the repo for all sigils which do not match the specified criteria.'''
        results = []
        rscs = self.__get_search_sigil(kwargs)
        for sigil in self.sigil:
            if sigil != rss: results.append(sigil)
        sr = SigilRepo()
        sr.sigils = results
        return sr
    
    def at_most(self, **kwargs):
        '''Use to poll the repo for all sigils which have attributes at most the specified criteria.'''
        results = []
        rscs = self.__get_search_sigil(kwargs)
        for sigil in self.sigil:
            if sigil <= rss: results.append(sigil)
        sr = SigilRepo()
        sr.sigils = results
        return sr
    
    def at_least(self, **kwargs):
        '''Use to poll the repo for all sigils which have attributes at least the specified criteria.'''
        results = []
        rscs = self.__get_search_sigil(kwargs)
        for sigil in self.sigil:
            if sigil >= rss: results.append(sigil)
        sr = SigilRepo()
        sr.sigils = results
        return sr
        
    def merge_search(self, sigilrepo):
        '''Use to collate the sigils in two searches.'''
        sr = SigilRepo()
        sr.sigils = self.sigils.union(sigilrepo.sigils)
        return sr
        
    def load_images(self, path, flip):
        '''Updates all the sigil info with their relevant sprites taken from specified spritesheets.'''
        sprites = separate_spritesheet(path)
        flipped = separate_spritesheet(flip)
        m = len(self.sigils)
        n = len(sprites)
        o = len(flipped)
        if m != n: raise ValueError("Repo and spritesheet have different sizes; cannot collate their images.")
        if m != o: raise ValueError("Repo and flipped spritesheet have different sizes; cannot collate their images.")
        for i in range(n):
            self.sigils[i].image = sprites[i]
            self.sigils[i].mirrored = sprites[i]
            if self.sigils[i].has_mirror: self.sigils[i].mirrored = flipped[i]