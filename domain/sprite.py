import pygame as pg

class Sprite(pg.sprite.Sprite):
    def __init__(self, pos, size, parent):
        super().__init__()
        
        # Initialise Attributes:
        self.__surface = None
        self.parent = parent
        self.rect = pg.Rect(pos, size)
        self.cursor_state = None
        self.visible = True
    
    @property
    def surface(self):
        if self.__surface is not None: return self.__surface
        self.__surface = pg.Surface(self.size, pg.SRCALPHA)
        return self.__surface
    
    @surface.setter
    def surface(self, surface):
        if not isinstance(surface, pg.Surface): raise TypeError(f'Could not set surface of sprite to object of type {type(surface)}')
        self.__surface = surface
    
    @property
    def game(self):
        return self.parent.game
    
    @property
    def moused_over(self):
        '''Use to determine if the cursor is placed over the sprite.'''
        return self.rect.collidepoint(self.parent.cursor_pos)
    
    @property
    def pos(self):
        return self.rect.topleft
        
    @property
    def size(self):
        return self.rect.size
        
    @pos.setter
    def pos(self, pos):
        self.rect.topleft = pos
        
    @size.setter
    def size(self, size):
        self.rect.size = size
    
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
    
    def get_palette(self):
        '''Gets the colour palette from preferences.'''
        return self.parent.get_palette()
        
    def events(self, events):
        for event in events:
            if self.is_clicked(event):
                if event.button == 1: self.on_left_click()
                if event.button == 2: self.on_middle_click()
                if event.button == 3: self.on_right_click()
            
    def updates(self):
        try:
            if self.moused_over: self.game.cursor.state = self.cursor_state
        except: pass
        
    def draw(self, surface):
        if self.visible: surface.blit(self.surface, self.pos)

class HighlightableSprite(Sprite):
    def __init__(self, pos, size, parent):
        super().__init__(pos, size, parent)
        self.surfaces = {False: pg.Surface(size), True: pg.Surface(size)}
        
    @property
    def surface(self): return self.surfaces[self.moused_over]
    