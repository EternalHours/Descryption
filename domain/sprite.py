import pygame as pg

class Sprite(pg.sprite.Sprite):
    def __init__(self, pos, size, parent):
        super().__init__()
        
        # Initialise Attributes:
        self.parent = parent
        self.surfaces = {False: pg.Surface(size), True: pg.Surface(size)}
        self.size = size
        self.rect = pg.Rect(size)
        self.rect.top_left = pos
        self.on_click = {1: None, 2: None}
        self.cursor_state = None
    
    @property
    def game(self): return self.parent.game
    
    @property
    def moused_over(self):
        '''Use to determine if the cursor is placed over the sprite.'''
        return self.rect.collidepoint(self.parent.cursor)
    
    @property
    def surface(self): return self.surfaces[self.moused_over]
    
    @property
    def pos(self): return self.rect.top_left
        
    @pos.setter
    def pos(self, pos): self.rect.top_left = pos
    
    def is_clicked(self, event, button=1):
        '''Use to determine if a given event represents a click on the sprite.'''
        if event.type != pg.MOUSEBUTTONDOWN: return False
        if event.button != button: return False
        return self.moused_over
        
    def events(self, events):
        for event in events:
            if self.is_clicked(event): self.on_click[event.button](self)
            
    def updates(self):
        if self.mouse_over: self.game.cursor.state = self.cursor_state
        
    def draw(self, surface):
        surface.blit(self.surface, self.pos)