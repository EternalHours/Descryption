import os
import copy
import pygame as pg
from domain.basecard import Cost, BaseCard
from domain.sigils import SigilGroup
from domain.traits import TraitGroup
from data.const import Colour

class RogueCard:
    '''Exists to be a container for attributes of cards which may change across the duration of a Rogue run.'''
    
    def __init__(self, basecard, game):
        # Initialise Attributes:
        self.game = game
        self.basecard = basecard
        self.__name = None
        self.__cost = None
        self.__tribes = None
        self.sigils = SigilGroup(innate = self.basecard.sigils)
        self.__traits = TraitGroup(self.basecard.traits)
        self.__power = None
        self.__health = None
        self.__evolution = None
        self.__sigil_targets = copy.deepcopy(self.basecard.sigil_targets)
        self.__portraitpath = None # TODO
        self.__image = None
        
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
        
    @property
    def image(self)
        if self.__image is None: self.render()
        return self.__image
    
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
        if traits is None: self.__traits = None
        if not isinstance(traits, TraitGroup): raise TypeError(f"Could not set traits of RogueCard to object of type {type(traits)}.")
        else: self.__traits = traits
        
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
    
    def render(self):
        costicon = self.cost.image
        cardblank = self.traits.cardblank
        portrait = self.basecard.portrait
        colour = [Colour.black, Colour.white][self.traits.is_fullart]
        font = pg.font.Font(os.path.join("fonts", "Marksman.otf"), 16)
        power, ppos, health, hpos = None, None, None, None
        if isinstance(self.power, int):
            power = font.render(self.power, False, colour)
            ppos = (2, 58 - power.get_height())
        else:
            power = self.power.image
            ppos = (3, 57 - power.get_height())
        if isinstance(self.health, int):
            health = font.render(self.health, False, colour)
            hpos = (44 - health.get_width(), 58 - health.get_height())
        else:
            health = self.health.image
            hpos = (43 - health.get_width(), 57 - health.get_height())
        card = pg.Surface((44, 58))
        card.blit(cardblank, (2, 2))
        card.blit(portrait, (3, 3))
        card.blit(costicon, (card.get_width() - costicon.get_width() - 1, 2))
        card.blit(power, ppos)
        card.blit(health, hpos)
        #
        # TODO: sigil rendering
        #
        
        return card
        
        
    def copy(self):
        '''Creates a new copy of this rogue card with all the same modifications.'''
        card = RogueCard(self.basecard)
        card.name = self.name
        card.cost = self.cost
        card.traits = self.traits
        card.power = self.power
        card.health = self.health
        card.evolution = self.evolution
        return card
    
    def __repr__(self): return self.name

class RogueDeck:
    '''Exists as a list of cards accumulated and modified over a single Rogue Run. Only used outside of duels.'''
    
    def __init__(self, name=None, scrybe=None, tier=None):
        # Initialise Attributes:
        self.name = name
        self.scrybe = scrybe
        self.tier = tier
        self.side_deck = []
        self.main_deck = []
        self.__icon = None
    
    @property
    def icon(self):
        if self.__icon is not None: return self.__icon
        self.__icon = pg.image.load(os.path.join('images', 'roguedecks', f'{self.name.lower()}.png'))
        return self.__icon
    
    def preview(self):
        '''Renders deck preview for the selection screen. Call only once per deck.'''
        offset
        height = 58
        width = 44 + (44 + offset) * (len(self.main_deck) - 1)
        surface = pg.Surface((width, height), pg.SRCALPHA)
        for i in range(len(self.main_deck)):
            surface.blit(self.main_deck[i].render(), ((44 + offset) * i, 0))
        return surface
    
    def add_card(self, card, main=True):
        '''Adds the specified card to the Rogue Deck. Will create a RogueCard to add if BaseCard is supplied.'''
        if isinstance(card, BaseCard): card = RogueCard(card)
        if not isinstance(card, RogueCard): raise TypeError(f'Could not add object of type {type(card)} to RogueDeck.')
        if main and card not in self.main_deck: self.main_deck.append(card)
        elif card not in self.side_deck: self.side_deck.append(card)
        else: raise ValueError(f"{card} already exists in RogueDeck")
    
    def remove_card(self, card):
        '''Removes the specified card from the Rogue Deck. Returns True if a card was removed and False if none was found.'''
        removed = False
        for i in range(len(self.main_deck)):
            if self.main_deck[i] is card:
                self.main_deck = self.main_deck[:i] + self.main_deck[i+1:]
                removed = True
        for i in range(len(self.side_deck)):
            if self.side_deck[i] is card:
                self.side_deck = self.side_deck[:i] + self.side_deck[i+1:]
                removed = True
        return removed