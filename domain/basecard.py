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
        
    def is_subcost(self, other):
        '''Use to determine if this cost is encompassed by another. Should be used instead of < for comparison.'''
        if not isinstance(other, Cost): raise TypeError(f"Cannot be a subcost of objects of type: {type(other)}")
        if self.blood > other.blood: return False
        if self.bones > other.bones: return False
        if not self.gems.is_subcost(other.gems): return False
        if self.energy > other.energy: return False
        if self.links > other.links: return False
        if self.gold > other.gold: return False
        return True
    
    def __int__(self):
        '''Use only to quickly determine equality and sort order.'''
        return self.gold + self.links * 8 + self.energy * 64 + int(self.gems) * 256 + self.bones * 4192 + self.blood * 67072
        
    def __eq__(self, other):
        if not isinstance(other, Cost): raise TypeError(f"Unsupported types for '=': {type(self)} and {type(other)}")
        return int(self) == int(other)
        
    def __lt__(self, other):
        if not isinstance(other, Cost): raise TypeError(f"Unsupported types for '<': {type(self)} and {type(other)}")
        return int(self) == int(other)
        
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
        return int(self) == int(other)
              
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
        if self.card_id is not None and self.card_id != other.card_id: return False
        if self.name is not None and self.name != other.name: return False
        if self.cost is not None and self.cost != other.cost: return False
        if self.rarity is not None and self.rarity != other.rarity: return False
        if self.scrybes is not None and self.scrybes != other.scrybes: return False
        if self.tribes is not None and self.tribes != other.tribes: return False
        if self.sigils is not None and self.sigils != other.sigils: return False
        if self.traits is not None and self.traits != other.traits: return False
        if self.power is not None and self.power != other.power: return False
        if self.health is not None and self.health != other.health: return False
        return True
        
    def __rle__(self, other):
        # Note that this takes the form: other < self so the logic is inverted.
        if not isinstance(other, BaseCardInfo): raise TypeError(f"Unsupported types for '<': {type(other)} and {type(self)}")
        if self.card_id is not None and self.card_id < other.card_id: return False
        if self.name is not None and self.name < other.name: return False
        if self.cost is not None and not other.is_subcost(self.cost): return False
        if self.rarity is not None and self.rarity < other.rarity: return False
        if self.scrybes is not None and not other.scrybes.issubset(self.scrybes): return False
        if self.tribes is not None and other.tribes.issubset(self.tribes): return False
        if self.sigils is not None and other.sigils.issubset(self.sigils): return False
        if self.traits is not None and other.traits.issubset(self.traits): return False
        if isinstance(self.power, int) and isinstance(other.power, int) and self.power < other.power: return False
        if isinstance(self.health, int) is not None and isinstance(other.health, int) and self.health < other.health: return False
        return True

    def __rge__(self, other):
        # Note that this takes the form: other > self so the logic is inverted.
        if not isinstance(other, BaseCardInfo): raise TypeError(f"Unsupported types for '>': {type(other)} and {type(self)}")
        if self.card_id is not None and self.card_id > other.card_id: return False
        if self.name is not None and self.name > other.name: return False
        if self.cost is not None and not self.is_subcost(other.cost): return False
        if self.rarity is not None and self.rarity > other.rarity: return False
        if self.scrybes is not None and not other.scrybes.issuperset(self.scrybes): return False
        if self.tribes is not None and other.tribes.issuperset(self.tribes): return False
        if self.sigils is not None and other.sigils.issuperset(self.sigils): return False
        if self.traits is not None and other.traits.issuperset(self.traits): return False
        if isinstance(self.power, int) and isinstance(other.power, int) and self.power > other.power: return False
        if isinstance(self.health, int) is not None and isinstance(other.health, int) and self.health > other.health: return False
        return True
        
class BaseCardRepo:
    def __init__(self):
        self.cards = []
    
    def find_by_id(self, card_id):
        '''Returns a base card with the given id. Returns None if none exists.'''
        # Added just for completeness. This should never be necessary since all cards should point to their base info.
        for card in self.cards:
            if card.card_id == card_id: return card
        return None
    
    def __get_search_card(self, kwargs):
        '''Use to convert dictionary of kwargs into a RepoSearchCard object.'''
        # Pass the kwargs as a dictionary.
        rsc = RepoSearchCard()
        if 'card_id' in **kwargs: rsc.card_id = kwargs['card_id']
        if 'name' in **kwargs: rsc.name = kwargs['name']
        if 'cost' in kwargs: rsc.cost = kwargs['cost']
        elif 'blood' in kwargs: rsc.cost = Cost(blood = kwargs['blood'])
        elif 'bones' in kwargs: rsc.cost = Cost(bones = kwargs['bones'])
        elif 'gems' in kwargs: rsc.cost = Cost(gems = kwargs['gems'])
        elif 'energy' in kwargs: rsc.cost = Cost(energy = kwargs['energy'])
        elif 'links' in kwargs: rsc.cost = Cost(links = kwargs['links'])
        elif 'gold' in kwargs: rsc.cost = Cost(gold = kwargs['gold'])
        if 'rarity' in kwargs: rsc.rarity = kwargs['rarity']
        if 'scrybes' in kwargs: rsc.scrybes = kwargs['scrybes']
        if 'tribes' in kwargs: rsc.tribes = kwargs['tribes']
        if 'sigils' in kwargs: rsc.sigils = kwargs['sigils']
        if 'traits' in kwargs: rsc.traits = kwargs['traits']
        if 'power' in kwargs: rsc.power = kwargs['power']
        if 'health' in kwargs: rsc.health = kwargs['health']
        return rsc
    
    def match_to(self, **kwargs):
        '''Use to poll the repo for all cards which exactly match the specified criteria.'''
        results = []
        rsc = self.__get_search_card(kwargs)
        for card in self.cards:
            if card == rsc: results.append(card)
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
        
        