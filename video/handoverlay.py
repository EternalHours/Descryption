from domain.screen import Screen

class HandOverlay(Screen):
    def __init__(self, parent, object_size = (46, 60)):

        self.parent = parent
        self.object_size = object_size
        self.contents = []
        
    def add_sprite(self, sprite):
        self.contents.append(sprite)
        self.parent.sprites.append(sprite)
    
    def target_pos(self, item):
        if not item in self.contents: raise ValueError(f"Could not find {item} in contents")
        n = len(self.contents)
        i = self.contents.index(item)
        x = (420 - self.object_size[0]) * (i + 1) // (n + 1)
        y = (240 - self.object_size[1] - (87 - self.object_size[1]) // 2)
        return (x, y)
        
    def events(self): pass
    def updates(self): pass
    def draw(self, surface): pass