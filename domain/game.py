import os
import pygame as pg
from screeninfo import get_monitors
from domain.cursor import Cursor
from traits import TraitRepo
from basecard import BaseCardRepo
from sigils import SigilRepo

class Game:
	def __init__(self, resolution, savefile):
        # Inititialise Attributes:
        self.game = self
		self.window = None
        self.surface = pg.Surface(resolution)
        self.scale_factor = (1, 1)
        self.active_screens = None
        self.inactive_screens = []
        self.running = True
        self.cursor_pos = (0, 0)
        self.cursor = Cursor()
        self.savefile = savefile
        
        # Attributes for Window Creation:
        self.target_monitor = 0
        self.monitor_offset = [0, 30]
        self.fullscreen = None
        self.window_size = (100, 100)
        self.caption = ""
        self.icon_image_path = ""
        
        # Initialise Repositories
        self.basecards = BaseCardRepo()
        self.traits = TraitRepo()
        self.sigils = SigilRepo()
        
    @property
    def unlock_manager(self):
        return self.savefile.unlock_manager
    
    def create_window(self):
        '''Use to reshape/move the window.'''
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % tuple(self.monitor_offset)
        if self.fullscreen: self.window = pg.display.set_mode((info.current_w, info.current_h), pg.FULLSCREEN, display=self.target_monitor)
        else: self.window = pg.display.set_mode(self.window_size, display=self.target_monitor) 
        pg.display.set_caption(self.caption)
        pg.display.set_icon(pg.image.load(self.icon_image_path).convert_alpha())
        w1, w2 = self.window.get_width(), self.surface.get_width()
        h1, h2 = self.window.get_height(), self.surface.get_height()
        self.scale_factor = (w1/w2, h1/h2)
        
    def get_monitor_offset(self, target_monitor):
        '''Use to find the top left corner of the specified monitor.'''
        monitors = get_monitors()[:target_monitor]
        widths = [monitor.width for monitor in monitors]
        return sum(widths)

    def set_active_screen(screen):
        '''Use to toggle the active screen to the one specified.'''
        if screen is self.active_screen: raise KeyError(f"Screen already active: {screen}")
        if not screen in self.inactive_screens: raise KeyError(f"Unopened Screen: {screen}")
        self.inactive_screens = [self.active_screen] + self.inactive_screens
        self.inactive_screens.remove(screen)
        self.active_screen = screen
        return
    
    def events(self):
        '''Handles the events phase of the primary loop.'''
        self.cursor_pos = self.cursor.get_pos()
        keys = pg.key.get_pressed()
        events = pg.event.get()
        for event in events:
            ALT = (keys[pg.K_LALT] or keys[pg.K_RALT])
            if event.type == pg.QUIT: self.running = False
            elif ALT and keys[pg.K_DOWN]: pg.display.iconify()
            elif ALT and keys[pg.K_LEFT]:
                self.target_monitor = (self.target_monitor - 1) % len(get_monitors())
                self.monitor_offset[0] = self.get_monitor_offset(self.target_monitor)
                self.create_window()
            elif ALT and keys[pg.K_RIGHT]:
                self.target_monitor = (self.target_monitor + 1) % len(get_monitors())
                self.monitor_offset[0] = self.get_monitor_offset(self.target_monitor)
                self.create_window()
        self.active_screen.events(events)
        return
        
    def updates(self):
        '''Handles the updates phase of the primary loop.'''
        self.active_screen.updates()
        return
        
    def draw(self):
        '''Handles the draw phase of the primary loop.'''
        self.surface.fill((0, 0, 0))
        self.active_screen.draw(self.surface)
        self.window.blit(self.surface, (0, 0))
        pg.display.flip()
        return
        
    def main(self):
        while self.running:
            self.events()
            self.updates()
            self.draw()