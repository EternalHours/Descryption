import pygame as pg
from domain.animation import Animation, AnimatedSprite

class Cursor(AnimatedSprite):
    def __init__(self, framerate, parent):
        super().__init__((0, 0), (30, 30), parent)
    
        # Initialise Attributes:
        self.state = "POINTER"
        self.hotspots = {"POINTER": (0, 0)}
        self.framerate = framerate
        self.__pos = (0, 0)
    
    @property
    def hotspot(self):
        try: return self.hotspots[self.state.upper()]
        except: return (0, 0)
    
    @property
    def pos(self):
        u, v = pg.mouse.get_pos()
        x, y = self.hotspot
        return (u - x, v - y)
    
    def add(self, name, hotspot):
        if name.upper() in self.animations: raise KeyError("Cursor already loaded!")
        path = os.path.join("images", "cursors", name.lower())
        self.animations[name.upper()] = Animation().load_from_dir(path)
        self.hotspots[name.upper()] = hotspot

    def on_idle(self):
        animation = self.animations[self.state.lower()]
        self.play_animation(animation, self.framerate)
    
    def updates(self):
        super().updates()