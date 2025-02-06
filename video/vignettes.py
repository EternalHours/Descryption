import pygame as pg
from random import random
from domain.sprite import Sprite

class Scanlines(Sprite):
    def __init__(self, parent):
        self.parent = parent
        self.rect = pg.Rect((0, 0), parent.size)
        self.draw_scanlines()
        self.visible = True
        
    def draw_scanlines(self):
        width, height = self.size
        scanlines = pg.Surface(self.size, pg.SRCALPHA)
        for x in range(width):
            for y in range(height // 2):
                scanlines.set_at((x, 2*y), (0, 0, 0, 32))
        self.surface = scanlines
    
    def updates(self):
        pass
    
    def draw(self, surface):
        super().draw(surface)
        
    def __repr__(self):
        return "Scanlines"
        
class StaticVignette(Sprite):
    def __init__(self, parent):
        self.parent = parent
        self.rect = pg.Rect((0, 0), parent.size)
        self.frame = 0
        self.draw_static()
        self.visible = True
    
    @property
    def surface(self):
        return self.surfaces[self.frame]
    
    def draw_static(self):
        width, height = self.size
        static = []
        n = 5
        for i in range(n): static.append(pg.Surface(self.size, pg.SRCALPHA))
        for x in range(width // 2):
            for y in range(height // 2):
                for i in range(n):
                    if random() < 0.14: static[i].set_at((2*x, 2*y+1), (0, 0, 0, 14))
        self.surfaces = static
    
    def updates(self):
        self.frame = (self.frame + 1) % 5
        
    def draw(self, surface):
        super().draw(surface)
        
    def __repr__(self):
        return "Static"

class ShadowVignette(Sprite):
    def __init__(self, parent, tol=40):
        self.parent = parent
        self.rect = pg.Rect((0, 0), parent.size)
        self.draw_shadow(tol)
        self.visible = True
    
    def draw_shadow(self, tol):
        width, height = self.size
        surface = pg.Surface(self.size, pg.SRCALPHA)
        def shade(x, y):
            d = min(x, width-x, y, height-y)
            if d > tol: return 0
            a = (255 * 1.2) / (tol**2)
            a = int(0.5 * a * ((tol - d) ** 2))
            return a
        for x in range(width):
            for y in range(height):
                a = shade(x, y)
                surface.set_at((x, y), (0, 0, 0, a))
        self.surface = surface
        
    def __repr__(self):
        return "Shadow"