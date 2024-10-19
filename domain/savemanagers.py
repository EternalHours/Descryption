import os
from collections import Counter

class SaveFile:

    def create(filename, override=False):
        savefile = SaveFile(filename)
        if override and os.path.exists(savefile.path): return
        savefile.save()

    def load(filename):
        path = os.path.join('data', 'saves', f'{filename}.txt')
        with file as open(path, 'r'):
            #
            #
            #
            pass

	def __init__(self, name):
        # Initialise Attributes:
        self.name = name
        self.path = os.path.join('data', 'saves', f'{name}.txt')
        self.__unlock_manager = None
        self.__rogue_manager = None
    
    @property
    def unlock_manager(self):
        if self.__unlock_manager is not None: return self.__unlock_manager
        self.__unlock_manager = UnlockManager()
        
    def save(self):
        with file as open(path, 'w'):
            #
            #
            #
            pass
            
class UnlockManager:
        def __init__(self):
        
        # ROGUE
        self.roguetiers = {scrybe: 0 for scrybe in {"Leshy", "Grimora", "Magnificus", "P03", "Galliard", "Challenge"}}
        self.__challenge_tier = 0
        self.__challenge_cap = 10
        
        # CARDS
        self.card_ids = set()
        self.collection = Counter()
        
    @property
    def challenge_tier(self):
        return self.challenge_tier
    
    @property
    def challenge_cap(self):
        return self.__challenge_cap
    
    @challenge_cap.setter
    def maxchallenge(self, value):
        if not isinstance(value, int): raise TypeError(f"Max Challenge Rating must be an integer.")
        if not 10 <= value <= 250: raise ValueError(f"Max Challenge Rating must be between 10 and 250 inclusive.")
        self.__challenge_cap = value
        self.__challenge_tier = sum([n <= value for n in [30, 50, 70, 90, 110, 130]])

class RogueManager:
    def __init__(self):
        # Initialise Attributes:
        self.genseed = None
        self.eventseed = None
        self.current_map = None
        self.map_number = None
        self.playerpos = None
        self.deck = None
        self.items = None
        self.equips = None
        self.spellbook = None