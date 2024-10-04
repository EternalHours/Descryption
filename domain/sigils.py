import importlib
import pygame as pg
from collections import Counter
from scripts.separate_spritesheet import separate_spritesheet

class SigilInfo:
    def __init__(self, sigil_id, name, scrybes, description, triggers, is_mox, is_conduit, has_mirror, can_stack):
        # Initialise Attributes:
        func = lambda *args: None
        self.sigil_id = sigil_id
        self.name = name
        self.scrybes = scrybes
        self.description = description
        self.is_mox = is_mox
        self.is_conduit = is_conduit
        self.is_power = False
        self.is_active = False
        self.has_mirror = has_mirror
        self.can_stack = can_stack
        # Derived Attributes:
        self.effects = {trigger: func for trigger in triggers}
        self.load_effects()
        self.image = None
        self.__mirrored = None
    
    @property
    def triggers(self): return set(self.effects.keys())
    
    @property
    def mirrored(self):
        # Note that the mirrored sprite is for when opponents have sigil on their cards and not for horizontal flipping.
        if self.__mirrored is None: return self.image
        return self.__mirrored
        
    @property
    def mirrored(self, image):
        self.__mirrored = image
    
    def load_effects(self):
        sigil = importlib.import_module(f"scripts.sigils.{self.name.lower().replace(' ', '_')}")
        for trigger in self.triggers:
            try: self.effects[trigger] = getattr(sigil, "on_"+trigger)
            except: print(f"Warning: Could not load effect for trigger, {trigger} of Sigil, {self.name}.")
            
    def __repr__(self):
        return self.name

class PowerSigilInfo:
    def __init__(self):
        # Initialise Attributes:
        def func(*args): return 1
        self.sigil_id = sigil_id
        self.name = name
        self.scrybes = scrybes
        self.description = description
        self.is_power = True
        self.is_active = False
        # Derived Attributes:
        self.valuefunc = func
        self.load_valuefunc()
        self.image = None
    
    def load_valuefunc(self):
        try:
            sigil = importlib.import_module(f"scripts.power.{self.name.lower().replace(' ', '_')}")
            self.valuefunc = getattr(sigil, "get_value")
        except: print(f"Warning: could not load value function of Power Sigil, {self.name}.")

    def __repr__(self):
        return self.name
        
class ActiveSigilInfo:
    def __init__(self):
        # Initialise Attributes:
        def func(*args): pass
        self.sigil_id = sigil_id
        self.name = name
        self.scrybes = scrybes
        self.description = description
        self.is_power = False
        self.is_active = True
        # Derived Attributes:
        self.effect = func
        self.load_effect()
        self.image = None
    
    def load_effect(self):
        try:
            sigil = importlib.import_module(f"scripts.active.{self.name.lower().replace(' ', '_')}")
            self.effect = getattr(sigil, "on_press")
        except: print(f"Warning: could not load effect of Active Sigil, {self.name}.")
    
    def __repr__(self):
        return self.name
        
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
    
    def get_search_sigil(self, kwargs):
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
        
    def load_images(self):
        '''Updates all the sigil info with their relevant sprites taken from spritesheets.'''
        sprites = separate_spritesheet(os.path.join('images', 'sigils'), (17, 17))
        flipped = separate_spritesheet(os.path.join('images', 'sigils_flipped'), (17, 17))
        powers = separate_spritesheet(os.path.join('images', 'power_sigils'), (11, 13))
        actives = separate_spritesheet(os.path.join('images', 'active_sigils'), (17, 11))
        if len(sprites) != len(flipped): raise RuntimeError("Sigils and Flipped Sigils spritesheets do not match in size.")
        for sigil in self.sigils:
            if sigil.is_active: sigil.image = actives[sigil.sigil_id]
            elif sigil.is_power: sigil.image = powers[sigil.sigil_id]
            else:
                if sigil.has_mirror: sigil.mirrored = flipped[sigil.sigil_id]
                sigil.image = sprites[sigil.sigil_id]

class SigilInfoGroup:
    def __init__(self, innate=None, patched=None):
        # Initialise Attributes
        self.__innate = None; self.innate = innate
        self.__patched = None; self.patched = patched
        
    @property
    def innate(self):
        return self.__innate
        
    @property
    def patched(self):
        return self.__patched
        
    @innate.setter
    def innate(self, innate=None):
        if innate is None: return
        sigils = SigilInfoGroup()
        for sigil in innate: sigils.add(sigil, "innate")
        self.__innate = sigils.innate
    
    @patched.setter
    def patched(self, patched=None):
        if patched is None: return
        sigils = SigilInfoGroup()
        for sigil in patched: sigils.add(sigil, "patched")
        self.__patched = sigils.patched
    
    def add(self, sigil, category="patched"):
        if not isinstance(sigil, SigilInfo): raise TypeError(f"Could not add object of type {type(sigil)} to SigilInfoGroup.")
        if category.lower() not in ["innate", "patched"]: raise ValueError("Category must be Innate or Patched.")
        if sigil in self and not sigil.can_stack: raise AttributeError("Sigil already exists within group and cannot stack.")
        if category.lower() == "innate": self.__innate = sorted(self.__innate + [sigil])
        else: self.__patched = self.__patched + [sigil]
        # Note that whilst innate sigils are sorted by id, patched sigils are sorted chronologically.
    
    def remove(self, sigil, category="patched"):
        if sigil not in getattr(self, category.lower()): raise ValueError(f"Sigil not found in category.")
        if category.lower() not in ["innate", "patched"]: raise ValueError("Category must be Innate or Patched.")
        if category.lower() == "innate": self.__innate.remove(sigil)
        else: self.__patched.remove(sigil)
    
    def __iter__(self):
        return iter(sorted(self.innate + self.patched))
    
    def __lt__(self, other):
        this = Counter(self)
        that = Counter(other)
        le = [this[sigil] <= that[sigil] for sigil in this]
        eq = [this[sigil] == that[sigil] for sigil in this]
        return all(le) and not all(eq)
    
    def __gt__(self, other):
        this = Counter(self)
        that = Counter(other)
        ge = [this[sigil] >= that[sigil] for sigil in that]
        eq = [this[sigil] == that[sigil] for sigil in that]
        return all(ge) and not all(eq)

    def __le__(self, other):
        this = Counter(self)
        that = Counter(other)
        le = [this[sigil] <= that[sigil] for sigil in this]
        return all(le)
    
    def __ge__(self, other):
        this = Counter(self)
        that = Counter(other)
        ge = [this[sigil] >= that[sigil] for sigil in that]
        return all(ge)
        
    def __eq__(self, other):
        this = Counter(self)
        that = Counter(self)
        return this == that