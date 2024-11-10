import pygame as pg
from data.const import ColourPalette

class Screen:
    def __init__(self, size, parent):
        # Initialise Attributes:
        self.parent = parent
        self.pos = (0, 0)
        self.size = size
        self.sprites = []
        self.overlays = []
        self.cursor_pos = (0, 0)
        self.background = None
        self.visible = True
        
    @property
    def game(self): return self.parent.game
        
    @property
    def moused_over(self):
        '''Use to determine whether the cursor is inside the screen.'''
        u, v = self.cursor_pos
        x, y = self.size
        return (0 <= u < x) and (0 <= v < y)
    
    def open(self):
        '''Use to open the screen in-game, either for the first or sequential times.'''
        if self is self.game.active_screen: raise RuntimeError("Tried to open the active screen!")
        if self not in self.game.inactive_screens: self.game.inactive_screens.append(self)
        self.game.set_active_screen(self)
        return
    
    def close(self):
        '''Use to permanently close the screen.'''
        # To deactivate this screen without closing, use game.set_active_screen(screen) or screen.open() on the desired screen.
        if self is self.game.active_screen: self.game.set_active_screen(self.game.inactive_screens[0])
        self.game.inactive_screens.remove(self)
        return
    
    def get_palette(self):
        '''Gets the colour palette from preferences.'''
        index = self.game.savefile.preference_manager.palette
        palette = ColourPalette.by_index[index]
        return palette
    
    def events(self, events):
        for sprite in self.sprites:
            sprite.events(events)
        return
                
    def updates(self):
        # Adjust cursor pos relative to new origin.
        u, v = self.pos
        x, y = self.parent.cursor_pos
        self.cursor_pos = (x-u, y-v)
        # Updates loop:
        for sprite in self.sprites:
            sprite.updates()
        for overlay in self.overlays:
            overlay.updates()
        return
    
    def draw(self, surface):
        if not self.visible: return
        self.surface = pg.Surface(self.size).convert_alpha()
        if self.background is not None: self.surface.blit(self.background, (0, 0))
        for sprite in self.sprites:
            sprite.draw(self.surface)
        for overlay in self.overlays:
            overlay.draw(self.surface)
        surface.blit(self.surface, self.pos)
        return