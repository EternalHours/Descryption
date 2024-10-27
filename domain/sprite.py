import pygame as pg

class Sprite(pg.sprite.Sprite):
    def __init__(self, pos, size, parent):
        super().__init__()
        
        # Initialise Attributes:
        self.parent = parent
        self.surfaces = {False: pg.Surface(size), True: pg.Surface(size)}
        self.size = size
        self.rect = pg.Rect(pos, size)
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
    def pos(self): return self.rect.topleft
        
    @pos.setter
    def pos(self, pos): self.rect.topleft = pos
    
    def on_left_click(self):
        '''Exists to be overridden. Will be called if the sprite is left-clicked.'''
        pass
    
    def on_middle_click(self):
        '''Exists to be overridden. Will be called if the sprite is middle-clicked.'''
        pass    
    
    def on_right_click(self):
        '''Exists to be overridden. Will be called if the sprite is right-clicked.'''
        pass    
    
    def is_clicked(self, event, button=1):
        '''Use to determine if a given event represents a click on the sprite.'''
        if event.type != pg.MOUSEBUTTONDOWN: return False
        if event.button != button: return False
        return self.moused_over
        
    def events(self, events):
        for event in events:
            if self.is_clicked(event):
                if event.button == 1: self.on_left_click()
                if event.button == 2: self.on_middle_click()
                if event.button == 3: self.on_right_click()
            
    def updates(self):
        if self.mouse_over: self.game.cursor.state = self.cursor_state
        
    def draw(self, surface):
        surface.blit(self.surface, self.pos)