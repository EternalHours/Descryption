import os
from collections import Counter

class SaveFile:

    def create(filename, override=False):
        path = os.path.join('data', 'saves', f'{filename}.txt')
        if override and os.path.exists(path): return
        savefile = SaveFile(filename)
        savefile.save()

    def load(filename=None):
        '''Returns the save file with the specified name, or returns the most recent save if no name is given.'''
        if filename is None:
            files = [os.path.join('data', 'saves', file) for file in os.listdir(os.path.join('data', 'saves'))]
            file = max(files, key=os.path.getmtime)
            filename = os.path.splitext(os.path.basename(file))[0]
        path = os.path.join('data', 'saves', f'{filename}.txt')
        with open(path, 'r') as file:
            savefile = SaveFile(filename)
            data = file.readlines()
            #
            #
            #
        return savefile        

    def __init__(self, name):
        # Initialise Attributes:
        self.name = name
        self.path = os.path.join('data', 'saves', f'{name}.txt')
        self.__preference_manager = None
        self.__unlock_manager = None
        self.__rogue_manager = None
        
    @property
    def preference_manager(self):
        if self.__preference_manager is not None: return self.__preference_manager
        self.__preference_manager = PreferenceManager()
        return self.__preference_manager
        
    @property
    def unlock_manager(self):
        if self.__unlock_manager is not None: return self.__unlock_manager
        self.__unlock_manager = UnlockManager()
        return self.__unlock_manager
        
    @property
    def rogue_manager(self):
        if self.__rogue_manager is not None: return self.__rogue_manager
        self.__rogue_manager = RogueManager()
        return self.__rogue_manager
        
    def save(self):
        path = os.path.join('data', 'saves', f'{self.name}.txt')
        with open(path, 'w') as file:
            #
            #
            #
            pass

class PreferenceManager:
    def __init__(self):
        # Initialise Attributes
        self.resolution = (420, 240)
        self.monitor_offset = (10, 10)
        self.framerate = 60
            
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