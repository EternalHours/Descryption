import os
import pygame as pg

class Cost:
    def __init__(self, blood=None, bones=None, gems=None, energy=None, links=None, gold=None):
        self.blood = blood if blood else 0
        self.bones = bones if bones else 0
        self.gems = gems if gems else GemCost()
        self.energy = energy if energy else 0
        self.links = links if links else 0
        self.gold = gold if gold else 0
        
    def is_subcost(self, other, exclusive=False):
        '''Use to determine if this cost is encompassed by another. Should be used instead of < for comparison.'''
        if not isinstance(other, Cost): raise TypeError(f"Cannot be a subcost of objects of type: {type(other)}")
        if self.blood > other.blood: return False
        if self.bones > other.bones: return False
        if not self.gems.is_subcost(other.gems): return False
        if self.energy > other.energy: return False
        if self.links > other.links: return False
        if self.gold > other.gold: return False
        if exclusive: return not self == other
        return True
    
    def __int__(self):
        '''Use only to quickly determine equality and sort order.'''
        return self.gold + self.links * 8 + self.energy * 64 + int(self.gems) * 256 + self.bones * 4192 + self.blood * 67072
        
    def __eq__(self, other):
        if not isinstance(other, Cost): raise TypeError(f"Unsupported types for '=': {type(self)} and {type(other)}")
        return int(self) == int(other)
        
    def __lt__(self, other):
        '''Use only for sorting. Use is_subcost for comparison.'''
        if not isinstance(other, Cost): raise TypeError(f"Unsupported types for '<': {type(self)} and {type(other)}")
        return int(self) < int(other)
        
class GemCost:
    def __init__(self, black=False, green=False, orange=False, blue=False, plusone=False):
        self.black = black
        self.green = green
        self.orange = orange
        self.blue = blue
        self.plusone = plusone
        
    def n_gems(self):
        '''Use to determine the minimum number of gems which could pay this cost.'''
        n = sum(self.green, self.orange, self.blue)
        if self.black: n = max(n, 1)
        if self.plusone: n = max(n, 2)
        return n
        
    def is_subcost(self, other):
        '''Use to determine if this cost is encompassed by another. Should be used instead of <= for comparison.'''
        if self.n_gems > other.n_gems: return False
        if self.green and not other.green: return False
        if self.orange and not other.orange: return False
        if self.blue and not other.blue: return False
        return True
    
    def __int__(self):
        '''Use only to determine equality and sort order.'''
        return self.black + self.green * 4 + self.orange * 8 + self.blue * 16 + self.plusone
        
    def __eq__(self, other):
        if not isinstance(other, Cost): raise TypeError(f"Unsupported types for '=': {type(self)} and {type(other)}")
        return int(self) == int(other)
        
    def __lt__(self, other):
        if not isinstance(other, Cost): raise TypeError(f"Unsupported types for '<': {type(self)} and {type(other)}")
        return int(self) < int(other)
              
class BaseCardInfo:
    def __init__(self, card_id, name, cost, rarity, scrybes, tribes, sigils, traits, power, health, evolution, sigil_targets):
        # Note: Use sets instead of lists or tuples.
    
        # Initialise Attributes:
        self.card_id = card_id
        self.name = name
        self.cost = cost
        self.rarity = rarity
        self.scrybes = scrybes
        self.tribes = tribes
        self.sigils = sigils
        self.traits = traits
        self.power = power
        self.health = health
        # The following attributes cannot be searched for:
        self.evolution = evolution
        self.sigil_targets = sigil_targets
        self.__portraitpath = None
        
    @property
    def portrait(self):
        '''Dynamically loads portrait for memory save. Call sparingly.'''
        return pg.image.load(os.path.join('images', 'portraits', self.__portraitpath))
    
    def __lt__(self, other):
        if not isinstance(other, BaseCardInfo): raise TypeError(f"Unsupported types for '<': {type(self)} and {type(other)}.")
        return self.card_id < other.card_id
        
    def __eq__(self, other):
        if isinstance(other, BaseCardInfo): return self.card_id == other.card_id
        raise TypeError(f"Unsupported types for '=': {type(self)} and {type(other)}")
        
class RepoSearchCard:
    def __init__(self):
        '''Exists to use as comparison to BaseCardInfo for filtering.'''
        self.card_id = None
        self.name = None
        self.cost = None
        self.rarity = None
        self.scrybes = None
        self.tribes = None
        self.sigils = None
        self.traits = None
        self.power = None
        self.health = None

    def __req__(self, other):
        if not isinstance(other, BaseCardInfo): raise TypeError(f"Unsupported types for '=': {type(other)} and {type(self)}")
        attributes = {'card_id', 'name', 'cost', 'rarity', 'scrybes', 'tribes', 'sigils', 'traits', 'power', 'health'}
        for attribute in attributes:
            this = getattr(self, attribute)
            that = getattr(other, attribute)
            if this is not None and this != that: return False
        return True
        
    def __rle__(self, other):
        # Note that this takes the form: other <= self so the logic is inverted.
        if not isinstance(other, BaseCardInfo): raise TypeError(f"Unsupported types for '<=': {type(other)} and {type(self)}")
        attributes = {'card_id', 'name', 'cost', 'scrybes', 'tribes', 'sigils', 'traits', 'power', 'health'}
        for attribute in attributes:
            this = getattr(self, attribute)
            that = getattr(other, attribute)
            if this is not None:
                if isinstance(this, set) and that.issubset(this): return False
                elif isinstance(this, cost) and this.is_subcost(that, exclusive=True): return False
                elif this < that: return False
        return True

    def __rge__(self, other):
        # Note that this takes the form: other >= self so the logic is inverted.
        if not isinstance(other, BaseCardInfo): raise TypeError(f"Unsupported types for '>=': {type(other)} and {type(self)}")
        attributes = {'card_id', 'name', 'cost', 'scrybes', 'tribes', 'sigils', 'traits', 'power', 'health'}
        for attribute in attributes:
            this = getattr(self, attribute)
            that = getattr(other, attribute)
            if this is not None:
                if isinstance(this, set) and that.issuperset(this): return False
                elif isinstance(this, cost) and this.is_subcost(this, exclusive=True): return False
                elif this > that: return False
        return True 
        
class BaseCardRepo:
    def __init__(self):
        self.cards = []
    
    def find_by_id(self, card_id):
        '''Returns a base card with the given id. Returns None if none exists.'''
        # For use when loading from save.
        for card in self.cards:
            if card.card_id == card_id: return card
        return None
        
    def find_by_name(self, card_name):
        '''Returns a base card with the given name. Returns None if none exists.'''
        # For use when initialising from spreadsheet data.
        for card in self.cards:
            if card.name == card_name: return card
        return None
    
    def __get_search_card(self, kwargs):
        '''Use to convert dictionary of kwargs into a RepoSearchCard object.'''
        attributes = {'card_id', 'name', 'cost', 'blood', 'bones', 'energy', 'gems', 'links', 'gold', 'rarity', 'scrybes', 'tribes', 'sigils', 'traits', 'power', 'health'}
        rsc = RepoSearchCard()
        for kwarg in kwargs:
            if kwarg not in attributes: raise KeyError(f"Unrecognised attribute of RepoSearchCard: '{kwarg}'.")
            if kwarg not in {'blood', 'bones', 'energy', 'gems', 'links', 'gold'}: setattr(rsc, kwarg, kwargs[kwarg])
            else:
                cost = Cost()
                setattr(cost, kwarg, kwargs[kwarg])
                rsc.cost = cost
    
    def match_to(self, **kwargs):
        '''Use to poll the repo for all cards which exactly match the specified criteria.'''
        results = []
        rsc = self.__get_search_card(kwargs)
        for card in self.cards:
            if card == rsc: results.append(card)
        bcr = BaseCardRepo()
        bcr.cards = results
        return bcr
        
    def exclude(self, **kwargs):
        '''Use to poll the repo for all cards which do not match the specified criteria.'''
        results = []
        rsc = self.__get_search_card(kwargs)
        for card in self.cards:
            if not card == rsc: results.append(card)
        bcr = BaseCardRepo()
        bcr.cards = results
        return bcr
    
    def at_most(self, **kwargs):
        '''Use to poll the repo for all cards which have attributes at most the specified criteria.'''
        results = []
        rsc = self.__get_search_card(kwargs)
        for card in self.cards:
            if card <= rsc: results.append(card)
        bcr = BaseCardRepo()
        bcr.cards = results
        return bcr
    
    def at_least(self, **kwargs):
        '''Use to poll the repo for all cards which have attributes at least the specified criteria.'''
        results = []
        rsc = self.__get_search_card(kwargs)
        for card in self.cards:
            if card >= rsc: results.append(card)
        bcr = BaseCardRepo()
        bcr.cards = results
        return bcr
        
    def merge_search(self, basecardrepo):
        '''Use to collate the cards in two searches.'''
        bsc = BaseCardRepo()
        bsc.cards = self.cards.union(basecardrepo.cards)
        return bsc
        
        