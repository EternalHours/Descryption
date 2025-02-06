import os
import pygame as pg
from domain.animation import Animation, AnimatedSprite

class Cursor(AnimatedSprite):
    def __init__(self, framerate, parent):
        super().__init__((0, 0), (30, 30), parent)
    
        # Initialise Attributes:
        self.__state = None
        self.hotspots = {}
        self.framerate = framerate
        self.__pos = (0, 0)
        self.load_all()
        self.visible = True
        
    @property
    def state(self):
        if self.__state is None: self.__state = "POINTER"
        return self.__state
    
    @property
    def hotspot(self):
        try: return self.hotspots[self.state.upper()]
        except: return (0, 0)
    
    @property
    def pos(self):
        if self.parent.fullscreen: u, v = self.parent.cursor_pos
        else: u, v = pg.mouse.get_pos()
        x, y = self.hotspot
        return (u - x, v - y)
        
    @state.setter
    def state(self, state):
        if state not in self.hotspots: raise ValueError("Invalid cursor state!")
        self.__state = state
    
    def add(self, name):
        if name.upper() in self.animations: raise KeyError("Cursor already loaded!")
        path = os.path.join("images", "cursors", name.lower())
        with open(os.path.join(path, 'hotspot.txt')) as file:
            hotspot = tuple([int(x) for x in file.read().split(" ")])
        anim = Animation()
        anim.load_from_dir(path)
        self.animations[name.upper()] = anim
        self.hotspots[name.upper()] = hotspot
    
    def load_all(self):
        dir = os.path.join('images', 'cursors')
        for f in os.listdir(dir):
            path = os.path.join(dir, f)
            if os.path.isdir(path):
                self.add(f)

    def on_idle(self):
        animation = self.animations[self.state.upper()]
        if len(animation) > 1: self.play_animation(animation, self.framerate)
    
    def updates(self):
        super().updates()
        anim = self.animations[self.state.upper()]
        if len(anim) == 1: self.surface = anim.frames[0]