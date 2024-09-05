import copy
from domain.basecard import Cost, BaseCard
from domain.sigils import SigilGroup

class RogueCard:
    '''Exists to be a container for attributes of cards which may change across the duration of a Rogue run.'''
    def __init__(self, basecard):
        # Initialise Attributes:
        self.basecard = basecard
        self.__name = None
        self.__cost = None
        self.__tribes = None
        self.sigils = SigilGroup(innate = self.basecard.sigils)
        self.__traits = None
        self.__power = None
        self.__health = None
        self.__evolution = None
        self.__sigil_targets = copy.deepcopy(self.basecard.sigil_targets)
        self.__portraitpath = None # TODO
        
    @property
    def name(self):
        if self.__name is None: return self.basecard.name
        return self.__name
    
    @property
    def cost(self):
        if self.__cost is None: return self.basecard.cost
        return self.__cost
    
    @property
    def rarity(self):
        # Note: has no setter.
        return self.basecard.rarity
    
    @property
    def scrybes(self):
        # Note: has no setter.
        return self.basecard.scrybes
    
    @property
    def tribes(self):
        if self.__tribes is None: return self.basecard.tribes
        return self.__tribes
    
    @property
    def traits(self):
        if self.__traits is None: return self.basecard.traits
        return self.__traits
    
    @property
    def power(self):
        if self.__power is None: return self.basecard.power
        return self.__power
        
    @property
    def health(self):
        if self.__health is None: return self.basecard.health
        return self.__health
    
    @property
    def evolution(self):
        if self.__evolution is None: return self.basecard.evolution
        return self.__evolution
        
    @name.setter
    def name(self, name):
        if name is None: self.__name = None
        elif not isinstance(name, str): raise TypeError(f"Could not set name of RogueCard to object of type {type(name)}.")
        else: self.__name = name
        
    @cost.setter
    def cost(self, cost):
        if cost is None: self.__cost = None
        elif not isinstance(cost, Cost): raise TypeError(f"Could not set cost of RogueCard to object of type {type(cost)}.")
        else: self.__cost = cost
        
    @traits.setter
    def traits(self, traits):
        #
        # TODO
        #
        pass
        
    @power.setter
    def power(self, power):
        if power is None: self.__power = None
        elif not isinstance(power, (str, int)): raise TypeError(f"Could not set power of RogueCard to object of type {type(power)}.")
        else: self.__power = power
        
    @health.setter
    def health(self, health):
        if health is None: self.__health = None
        elif not isinstance(health, (str, int)): raise TypeError(f"Could not set power of RogueCard to object of type {type(health)}.")
        else: self.__health = health
        
    @evolution.setter
    def evolution(self, evolution):
        if evolution is None: self.__evolution = None
        elif isinstance(evolution, BaseCard): self.__evolution = evolution.card_id
        elif not isinstance(evolution, (str, int)): raise TypeError(f"Could not set evolution of RogueCard to object of type {type(evolution)}.")
        else: self.__evolution = evolution

class RogueDeck:
    def __init__(self)