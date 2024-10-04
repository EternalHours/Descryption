import os
import csv
import pygame as pg
from collections import Counter
from domain.sigils import SigilInfoGroup
from scripts.separate_spritesheet import separate_spritesheet

class Cost:
    images = None
    
    def load_images():
        images = separate_spritesheet(os.path.join('images', 'costs.png'), (26, 15))
        binders = ['blood', 'bones', 'gems', 'energy', 'links', 'gold']
        cost_images = {binder: [] for binder in binders}
        for i in range(len(images)):
            binder = binders[i % 6]
            cost_images[binder].append(images[i])
        Cost.images = cost_images

    def __init__(self, *args, **kwargs):
        self.blood = kwargs['blood'] if 'blood' in kwargs else 0
        self.bones = kwargs['bones'] if 'bones' in kwargs else 0
        self.gems = kwargs['gems'] if 'gems' in kwargs else 0
        self.energy = kwargs['energy'] if 'energy' in kwargs else 0
        self.links = kwargs['links'] if 'links' in kwargs else 0
        self.gold = kwargs['gold'] if 'gold' in kwargs else 0
        if len(args) < 2: return
        if args[1].lower() in {'blood', 'bones', 'gems', 'energy', 'links', 'gold'}:
            setattr(self, args[1].lower(), args[0])
        
    @property
    def image(self):
        '''Returns the icon which represents this cost. Loads all into centralised memory to minimise repeat loads/data.'''
        if Cost.images is None: Cost.load_images()
        index = int(get)
        return Cost.images[self.cost_type.lower()][self.cost_value]
    
    @property
    def cost_type(self):
        '''Returns the name of the resource this cost requires.'''
        cost_types = ["Blood", "Bones", "Gems", "Energy", "Links", "Gold"]
        for cost_type in cost_types:
            if int(getattr(self, cost_type.lower())) > 0:
                return cost_type
        return None
    
    @property
    def cost_value(self):
        '''Returns the value of the resource this cost requires.'''
        return getattr(self, cost_type.lower())
        
    @property
    def gems(self):
        return self.__gems
        
    @gems.setter
    def gems(self, value):
        if isinstance(value, GemCost): self.__gems = value
        elif isinstance(value, int): self.__gems = GemCost.from_int(value)
        
    def is_subcost(self, other, exclusive=False):
        '''Use to determine if this cost is encompassed by another. Should be used instead of < or <= for comparison.'''
        if self == other: return not exclusive
        for attribute in ['blood', 'bones', 'gems', 'energy', 'links', 'gold']:
            if getattr(self, attribute) > getattr(other, attribute): return False
        return True
    
    def __iter__(self): return iter(self.blood, self.bones, self.gems, self.energy, self.links, self.gold)
    
    def __int__(self):
        '''Use only to quickly determine equality and sort order.'''
        return self.gold + self.blood * 3 + self.links * 12 + self.energy * 60 + int(self.gems) * 360 + self.bones * 4320
        
    def __eq__(self, other):
        if not isinstance(other, Cost): raise TypeError(f"Unsupported types for '=': {type(self)} and {type(other)}")
        return int(self) == int(other)
        
    def __lt__(self, other):
        '''Use only for sorting. Use is_subcost for comparison.'''
        if not isinstance(other, Cost): raise TypeError(f"Unsupported types for '<': {type(self)} and {type(other)}")
        return int(self) < int(other)
        
class GemCost:
    def from_int(value):
        '''Decodes GemCosts from their integer representation.'''
        black, green, orange, blue, plusone = [False] * 5
        if value > 0:
            black = value <= 2
            plusone = value % 2 == 0 and value <= 8
            green = value in {3, 4, 9, 10, 12}
            orange = value in {5, 6, 9, 11, 12}
            blue = value in {7, 8, 10, 11, 12}
        return GemCost(black, green, orange, blue, plusone)

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
    
    def __iter__(self):
        return iter((self.black, self.green, self.orange, self.blue, self.plusone))
    
    def __int__(self):
        '''Use only to determine equality and sort order. Also used to index for cost image.'''
        if not any(self): return 0
        if sum(tuple(self)[1:4]) < 2: return 1 + self.green * 2 + self.orange * 4 + self.blue * 6 + self.plusone
        return 6 + self.green + self.orange * 2 + self.blue * 3
        
    def __eq__(self, other):
        if not isinstance(other, GemCost): raise TypeError(f"Unsupported types for '=': {type(self)} and {type(other)}")
        return int(self) == int(other)
        
    def __lt__(self, other):
        if not isinstance(other, GemCost): raise TypeError(f"Unsupported types for '<': {type(self)} and {type(other)}")
        return int(self) < int(other)
              
class BaseCardInfo:
    def __init__(self, card_id, name, **kwargs):
        # Identifiers:
        self.card_id = card_id
        self.name = name
        
        # Searchable Attributes:
        self.cost = kwargs['cost'] if 'cost' in kwargs else Cost()
        self.rarity = kwargs['rarity'] if 'rarity' in kwargs else False
        self.binder = kwargs['binder'] if 'binder' in kwargs else 'Beasts'
        self.scrybes = kwargs['scrybes'] if 'scrybes' in kwargs else set()
        self.tribes = kwargs['tribes'] if 'tribes' in kwargs else set()
        self.sigils = kwargs['sigils'] if 'sigils' in kwargs else SigilInfoGroup()
        self.traits = kwargs['traits'] if 'traits' in kwargs else set()
        self.power = kwargs['power'] if 'power' in kwargs else 0
        self.health = kwargs['health'] if 'health' in kwargs else 1
        
        # Hidden Attributes
        self.evolution = kwargs['evolution'] if 'evolution' in kwargs else None
        self.elder_name = kwargs['elder_name'] if 'elder_name' in kwargs else None
        self.tail = kwargs['tail'] if 'tail' in kwargs else None
        self.pelt = kwargs['pelt'] if 'pelt' in kwargs else None
        self.sigil_targets = kwargs['sigil_targets'] if 'sigil_targets' in kwargs else {}
        self.__portraitpath = None
        
    @property
    def portrait(self):
        '''Dynamically loads portrait for memory save. Call sparingly.'''
        return pg.image.load(os.path.join('images', 'portraits', self.__portraitpath))
        
    @property
    def emission(self):
        '''Dynamically loads emission portrait for memory save. Call sparingly.'''
        return pg.image.load(os.path.join('images', 'portraits', self.__portraitpath+"_emission"))
    
    def set_image_path(self):
        self._portrait_path = self.name.lower().replace(" ", "").replace("(", "").replace(")", "")
        
    def __lt__(self, other):
        if not isinstance(other, BaseCardInfo): raise TypeError(f"Unsupported types for '<': {type(self)} and {type(other)}.")
        return self.card_id < other.card_id
        
    def __eq__(self, other):
        if isinstance(other, BaseCardInfo): return self.card_id == other.card_id
        raise TypeError(f"Unsupported types for '=': {type(self)} and {type(other)}")
        
    def __repr__(self):
        return self.name
        
    def __hash__(self):
        return hash(self.card_id)
        
class RepoSearchCard:
    def __init__(self):
        '''Exists to use as comparison to BaseCardInfo for filtering.'''
        self.cost = None
        self.rarity = None
        self.binder = None
        self.scrybes = None
        self.tribes = None
        self.sigils = None
        self.traits = None
        self.power = None
        self.health = None
        
    def __bool__(self):
        '''Used to determine if a query is trivial. ie. if the search card is empty.'''
        attributes = {'cost', 'rarity', 'binder', 'scrybes', 'tribes', 'sigils', 'traits', 'power', 'health'}
        return any([attribute is not None for attribute in attributes])

    def __eq__(self, other):
        if not isinstance(other, BaseCardInfo): raise TypeError(f"Unsupported types for '==': {type(self)} and {type(other)}.")
        attributes = {'cost', 'rarity', 'binder', 'scrybes', 'tribes', 'sigils', 'traits', 'power', 'health'}
        for attribute in attributes:
            this = getattr(self, attribute)
            that = getattr(other, attribute)
            if this is not None and this != that: return False
        return True
        
    def __ge__(self, other):
        if not isinstance(other, BaseCardInfo): raise TypeError(f"Unsupported types for '>=': {type(self)} and {type(other)}.")
        attributes = {'cost', 'scrybes', 'tribes', 'sigils', 'traits', 'power', 'health'}
        for attribute in attributes:
            this = getattr(self, attribute)
            that = getattr(other, attribute)
            if this is not None:
                if attribute == 'cost' and not that.is_subcost(this, exclusive=False): return False
                elif isinstance(attribute, set) and not that.issubset(this): return False
                elif not this >= that: return False
        return True

    def __le__(self, other):
        if not isinstance(other, BaseCardInfo): raise TypeError(f"Unsupported types for '<=': {type(self)} and {type(other)}.")
        attributes = {'cost', 'scrybes', 'tribes', 'sigils', 'traits', 'power', 'health'}
        for attribute in attributes:
            this = getattr(self, attribute)
            that = getattr(other, attribute)
            if this is not None:
                if attribute == 'cost' and not this.is_subcost(that, exclusive=False): return False
                elif isinstance(attribute, set) and not that.issubset(this): return False
                elif not this <= that: return False
        return True
        
class BaseCardRepo:
    def __init__(self):
        self.cards = set()
    
    def load_from_csv(self):
        path = os.path.join('data', 'cards.csv')
        with open(path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                bsc = BaseCardInfo(
                    card_id = row['CARD_ID'],
                    name = row['NAME'],
                    binder = row['BINDER'],
                    scrybes = set(row['BINDER'].split('; ')),
                    tribes = set(row['TRIBES'].split('; ')),
                    cost = Cost(int(row['COST_VALUE']), row['COST_TYPE']),
                    power = int(row['POWER']) if row['POWER'].isdigit() else row['POWER'],
                    health = int(row['HEALTH']) if row['HEALTH'].isdigit() else row['HEALTH'],
                    #sigils
                    #traits
                    rarity = row['IS_RARE'] == 'TRUE',
                    tail = row['TAIL'] if row['TAIL'] != '-' else None,
                    pelt = row['PELT'] if row['PELT'] != '-' else None,
                    evolution = row['EVOLUTION'] if row['EVOLUTION'] != '-' else None,
                    elder_name = row['ELDER_NAME'] if row['ELDER_NAME'] != '-' else None
                )
                self.add(bsc)
    
    def add(self, basecard):
        '''Adds a basecard to the repo.'''
        if not isinstance(basecard, BaseCardInfo): raise TypeError(f"Cannot add object of type {type(basecard)} to BaseCardRepo.")
        if basecard in self.cards: return
        self.cards.add(basecard)
    
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
        return rsc
    
    def match_to(self, **kwargs):
        '''Use to poll the repo for all cards which exactly match the specified criteria.'''
        results = []
        rsc = self.__get_search_card(kwargs)
        if not rsc: return self
        for card in self.cards:
            if rsc == card: results.append(card)
        bcr = BaseCardRepo()
        bcr.cards = results
        return bcr
        
    def exclude(self, **kwargs):
        '''Use to poll the repo for all cards which do not match the specified criteria.'''
        results = set()
        rsc = self.__get_search_card(kwargs)
        if not rsc: return self
        for card in self.cards:
            if not rsc == card: results.add(card)
        bcr = BaseCardRepo()
        bcr.cards = results
        return bcr
    
    def at_most(self, **kwargs):
        '''Use to poll the repo for all cards which have attributes at most the specified criteria.'''
        results = set()
        rsc = self.__get_search_card(kwargs)
        if not rsc: return self
        for card in self.cards:
            if rsc >= card: results.add(card)
        bcr = BaseCardRepo()
        bcr.cards = results
        return bcr
    
    def at_least(self, **kwargs):
        '''Use to poll the repo for all cards which have attributes at least the specified criteria.'''
        results = set()
        rsc = self.__get_search_card(kwargs)
        if not rsc: return self
        for card in self.cards:
            if rsc <= card: results.add(card)
        bcr = BaseCardRepo()
        bcr.cards = results
        return bcr
        
    def copy(self):
        bsc = BaseCardRepo()
        bsc.cards = self.cards
    
    def __iter__(self):
        return iter(self.cards)
    
    def __add__(self, other):
        bsc = self.copy()
        if isinstance(other, BaseCardInfo):
            bsc.add(other)
            return bsc
        for card in other: bsc.add(card)
        return bsc
        
        
        