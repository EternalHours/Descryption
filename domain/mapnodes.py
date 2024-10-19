class MapNodeInfo:
    def __init__(self, name, node_id, **kwargs):
        # Identifiers:
        self.name = name
        self.node_id = node_id
        
        # Searchable Attributes:
        self.scrybes = scrbes if scrybes in kwargs else set()
        self.pools = pools if pools in kwargs else set()
        
        # Hidden Attributes:
        self.screen = None
        self.load_screen() 
        
    def load_screen(self):
        sigil = importlib.import_module(f"video.nodes.{self.name.lower().replace(' ', '_')}")
        try: self.screen = getattr(sigil, self.name.capitalize().replace(" ", ""))
        except: print(f"Warning: Could not load screen class of Map Node, {self.name}.")
        
class RepoSearchNode:
    def __init__(self):
        self.scrybes = None
        self.pools = None
        
    def match_any(self, other):
        if not isinstance(other, MapNodeInfo): raise TypeError(f"Unsupported types for 'match_any': {type(self)} and {type(other)}.")
        if self.scrybes is not None and not any([scrybe in other.scrybes for scrybe in self.scrybes]): return False
        if self.pools is not None and not any([pool in other.pools for pool in self.pools]): return False
        return True
        
    def __eq__(self, other):
        if not isinstance(other, MapNodeInfo): raise TypeError(f"Unsupported types for '==': {type(self)} and {type(other)}.")
        if self.scrybes is not None and self.scrybes != other.scrybes: return False
        if self.pools is not None and self.pools != other.pools: return False
        return True
    
    def __le__(self, other):
        if not isinstance(other, MapNodeInfo): raise TypeError(f"Unsupported types for '<=': {type(self)} and {type(other)}.")
        if self.scrybes is not None and not self.scrybes.issubset(other.scrybes): return False
        if self.pools is not None and not self.pools.issubset(other.pools): return False
        return True
    
    def __ge__(self, other):
        if not isinstance(other, MapNodeInfo): raise TypeError(f"Unsupported types for '>=': {type(self)} and {type(other)}.")
        if self.scrybes is not None and not self.scrybes.issuperset(other.scrybes): return False
        if self.pools is not None and not self.pools.issuperset(other.pools): return False
        return True
        
class MapNodeRepo:
    def __init__(self):
        self.nodes = set()
    
    def load_from_csv(self):
        path = os.path.join('data', 'nodes.csv')
        with open(path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                node = MapNodeInfo(
                    name = row["NAME"],
                    node_id = int(row["NODE_ID"]),
                    scrybes = set(row["SCRYBES"].split("; ")),
                    pools = set(row["POOLS"].split("; "))
                )
                self.add(node)
    
    def find_by_name(self, name):
        '''Finds a node with the given name. Returns None if none is found.'''
        for node in self.nodes:
            if node.name == name:
                return node
        return None
    
    def find_by_id(self, node_id):
        '''Returns a node with the given id. Returns None if none is found.'''
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None
    
    def add(self, node):
        '''Adds a given MapNodeInfo object to the repo.'''
        if not isinstance(node, MapNodeInfo): raise TypeError(f"Cannot add object of type {type(node)} to MapNodeRepo.")
        if node in self.nodes: return
        self.nodes.add(node)
    
    def __get_search_node(self, kwargs):
        rsn = RepoSearchNode()
        if "scrybes" in kwargs: rsn.scrybes = kwargs["scrybes"]
        if "pools" in kwargs: rsn.pools = kwargs["pools"]
        return rsn
        
    def match_any(self, **kwargs):
        rsn = self.__get_search_node(kwargs)
        results = {}
        for node in self.nodes:
            if rsn.match_any(node): results.add(node)
        mnr = MapNodeRepo()
        mnr.nodes = results
        return mnr
    
    def match_to(self, **kwargs):
        rsn = self.__get_search_node(kwargs)
        results = {}
        for node in self.nodes:
            if rsn == node: results.add(node)
        mnr = MapNodeRepo()
        mnr.nodes = results
        return mnr
        
    def exclude(self, **kwargs):
        rsn = self.__get_search_node(kwargs)
        results = {}
        for node in self.nodes:
            if rsn != node: results.add(node)
        mnr = MapNodeRepo()
        mnr.nodes = results
        return mnr
        
    def at_least(self, **kwargs):
        rsn = self.__get_search_node(kwargs)
        results = {}
        for node in self.nodes:
            if rsn <= node: results.add(node)
        mnr = MapNodeRepo()
        mnr.nodes = results
        return mnr
        
    def at_most(self, **kwargs):
        rsn = self.__get_search_node(kwargs)
        results = {}
        for node in self.nodes:
            if rsn >= node: results.add(node)
        mnr = MapNodeRepo()
        mnr.nodes = results
        return mnr
    
    def copy(self):
        mnr = MapNodeRepo()
        mnr.cards = self.cards
        return mnr
    
    def __add__(self, other):
        mnr = self.copy()
        if isinstance(other, MapNodeInfo):
            mnr.add(other)
            return mnr
        for node in other: mnr.add(card)
        return mnr
    