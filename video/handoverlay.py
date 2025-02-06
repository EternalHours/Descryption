from domain.screen import Screen

class HandOverlay(Screen):
    def __init__(self, parent, object_size = (46, 60)):

        self.parent = parent
        self.object_size = object_size
        self.contents = []
        self.deal_queue = []
        self.dealing = []
        
    def add_sprite(self, sprite):
        self.contents.append(sprite)
        self.parent.sprites.append(sprite)
        sprite.pos = (420, self.target_pos(sprite)[1])
        sprite.deal_delay = len(self.deal_queue) * self.game.framerate // 6
        self.deal_queue.append(sprite)
    
    def target_pos(self, item):
        if not item in self.contents: raise ValueError(f"Could not find {item} in contents")
        n = len(self.contents)
        i = self.contents.index(item)
        w, h = self.object_size
        #x = (420 - self.object_size[0]) * (i + 1) // (n + 1)
        s = (420 - self.object_size[0]*n)
        if n == 1: x = (420 - w) // 2
        else:
            k = s // (n + 3)
            m = (s - k * (n - 1)) // 2
            x = m + (w + k) * i
        y = (240 - h - (87 - h) // 2)
        return (x, y)
        
    def events(self): pass
    
    def updates(self):
        if self.parent.state == "DEALING":
            for card in self.deal_queue:
                if card.deal_delay > 0: card.deal_delay -= 1
                elif card.deal_delay == 0:
                    self.deal_queue.remove(card)
                    self.dealing.append(card)
            for card in self.dealing:
                x, y = card.pos; X = self.target_pos(card)[0]
                if x >= X:
                    x -= 32 # Speed of Deal
                    if x < X - 10: x = X - 10 # Overshoot margin
                elif x < X:
                    x += 5 # Speed of Bounce back
                    if x >= X:
                        card.pos = (X, y)
                        self.dealing.remove(card)
                else: print(f"How did we get here? {x}, {X}")
                card.pos = (x, y)
            if len(self.dealing) == 0 and len(self.deal_queue) == 0: self.parent.state = "READY"
            
                
        
    def draw(self, surface): pass