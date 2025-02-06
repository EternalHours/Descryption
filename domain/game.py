import os
import time
import multiprocessing
import pygame as pg
from screeninfo import get_monitors
from domain.cursor import Cursor
from domain.traits import TraitRepo
from domain.basecard import BaseCardRepo
from domain.sigils import SigilRepo

class Game:
    def __init__(self, savefile):
        resolution = savefile.preference_manager.resolution
        framerate = savefile.preference_manager.framerate
        monitor_offset = savefile.preference_manager.monitor_offset
        fullscreen = savefile.preference_manager.fullscreen
    
        # Inititialise Attributes:
        self.game = self
        self.__window = None
        self.surface = pg.Surface((420, 240))
        self.scale_factor = (1, 1)
        self.active_screen = None
        self.inactive_screens = []
        self.running = True
        self.cursor_pos = (0, 0)
        self.__cursor = None
        self.savefile = savefile
        self.clock = pg.time.Clock()
        self.framerate = framerate
        
        # Attributes for Window Creation:
        self.target_monitor = 0
        self.monitor_offset = monitor_offset
        self.fullscreen = fullscreen
        self.window_size = resolution
        self.caption = "Descryption"
        self.icon_image_path = os.path.join('images', 'icon.png')
        
        # Initialise Repositories
        self.basecards = BaseCardRepo()
        self.traits = TraitRepo()
        self.sigils = SigilRepo()
    
    @property
    def cursor(self):
        if self.__cursor is not None: return self.__cursor
        self.__cursor = Cursor(self.framerate, self)
        return self.__cursor
        
    @property
    def window(self):
        if self.__window is not None: return self.__window
        self.create_window()
        return self.__window
    
    @property
    def unlock_manager(self):
        return self.savefile.unlock_manager
    
    def create_window(self):
        '''Use to reshape/move the window.'''
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % tuple(self.monitor_offset)
        if self.fullscreen:
            monitor = get_monitors()[self.target_monitor]; monitor_size = monitor.width, monitor.height
            self.__window = pg.display.set_mode((monitor_size), pg.FULLSCREEN, display=self.target_monitor)
        else: self.__window = pg.display.set_mode(self.window_size, display=self.target_monitor) 
        pg.display.set_caption(self.caption)
        pg.display.set_icon(pg.image.load(self.icon_image_path).convert_alpha())
        w1, w2 = self.__window.get_width(), self.surface.get_width()
        h1, h2 = self.__window.get_height(), self.surface.get_height()
        self.scale_factor = (w1/w2, h1/h2)
        
    def get_monitor_offset(self, target_monitor):
        '''Use to find the top left corner of the specified monitor.'''
        monitors = get_monitors()[:target_monitor]
        widths = [monitor.width for monitor in monitors]
        return sum(widths)

    def set_active_screen(self, screen):
        '''Use to toggle the active screen to the one specified.'''
        if screen is self.active_screen: raise KeyError(f"Screen already active: {screen}")
        if not screen in self.inactive_screens: raise KeyError(f"Unopened Screen: {screen}")
        self.inactive_screens = [self.active_screen] + self.inactive_screens
        self.inactive_screens.remove(screen)
        self.active_screen = screen
        return
    
    def events(self):
        '''Handles the events phase of the primary loop.'''
        if not self.fullscreen: self.cursor_pos = self.cursor.pos
        else:
            x, y = pg.mouse.get_pos()
            x = x // self.scale_factor[0]
            y = y // self.scale_factor[1]
            self.cursor_pos = (x, y)
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
            elif ALT and keys[pg.K_RETURN]:
                self.fullscreen = not self.fullscreen
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
        if self.fullscreen:
            monitor = get_monitors()[self.target_monitor]; monitor_size = monitor.width, monitor.height
            self.cursor.updates()
            self.cursor.draw(self.surface)
            surface = pg.transform.scale(self.surface, monitor_size)
        else:
            self.cursor.updates()
            self.cursor.draw(self.surface)
            surface = pg.transform.scale(self.surface, (self.window_size))
        self.window.blit(surface, (0, 0))
        pg.display.flip()
        return
    
    def main(self):
        while self.running:
            self.clock.tick(self.framerate)
            self.events()
            self.updates()
            self.draw()
        pg.quit()
            
    def apply_prefs(self):
        self.window_size = self.savefile.preference_manager.resolution
        self.framerate = self.savefile.preference_manager.framerate
        self.monitor_offset = self.savefile.preference_manager.monitor_offset
        self.create_window()
        

