class MapNodeInfo
    def __init__(self, name, node_id, **kwargs):
        # Identifiers:
        self.name = name
        self.node_id = node_id
        
        # Searchable Attributes:
        self.scrybes = scrbes if scrybes in kwargs else set()
        
class MapNodeRepo
    def __init__(self):
        self.nodes =set()
    
    def load_from_csv(self):
        path = os.path.join('data', 'nodes.csv')
        with open(path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                node = MapNodeInfo(
                    name = row["NAME"],
                    node_id = int(row["NODE_ID"])
                )
                self.add(node)
    
    def find_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None
    
    def find_by_id(self, node_id):
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None
    
    def add(self, node):
        if not isinstance(node, MapNodeInfo): raise TypeError(f"Cannot add object of type {type(node)} to MapNodeRepo.")
        if node in self.nodes: return
        self.nodes.add(node)