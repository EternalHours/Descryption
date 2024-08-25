import pygame as pg
from domain.animation import Animation, AnimatedSprite

class Cursor:
    def __init__(self):
        super().__init__(self, framerate)
    
        # Initialise Attributes:
        self.pos = (0, 0)
        self.state = "POINTER"
        self.hotspots = {}
        self.framerate = framerate
    
    @property
    def hotspot(self): return self.hotspots[self.state.lower()]
    
    def add(self, name, hotspot):
        if name.upper() in self.animations: raise KeyError("Cursor already loaded!")
        path = os.path.join("images", "cursors", name.lower())
        self.animations[name.upper()] = Animation().load_from_dir(path)
        self.hotspots[name.upper()] = hotspot

    def on_idle(self):
        animation = self.animations[self.state.lower()]
        self.play_animation(animation, self.framerate)
    
    def updates(self):
        u, v = pg.mouse.get_pos()
        x, y = self.hotspot
        self.pos = (u - x, v - y)
        super().updates()