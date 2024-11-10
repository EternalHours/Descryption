import pygame as pg
from data.const import Colour
from domain.screen import Screen
from video.vignettes import Scanlines, StaticVignette, ShadowVignette

class MenuScreen(Screen):
    def __init__(self, parent):
        super().__init__((420, 240), parent)
        self.draw_background()
        self.overlays.append(Scanlines(self))
        self.overlays.append(StaticVignette(self))
        self.overlays.append(ShadowVignette(self))
        self.state = "DEALING"
    
    @property
    def state(self): return self.__state
    
    @state.setter
    def state(self, state):
        states = {"DEALING"}
        if state not in states: raise ValueError(f"Unrecognised state of StartScreen: {state}")
        self.__state = state

    def draw_background(self):
        palette = self.get_palette()
        background = pg.Surface((420, 240))
        background.fill(palette['Light Block'])
        pg.draw.rect(background, palette['Dark Block'], pg.Rect((0, 0), (420, 46)))
        pg.draw.rect(background, Colour.black, pg.Rect((0, 46), (420, 4)))
        pg.draw.line(background, palette['Light Trim'], (0, 47), (420, 47))
        pg.draw.line(background, palette['Dark Trim'], (0, 48), (420, 48))
        pg.draw.rect(background, Colour.black, pg.Rect((0, 145), (420, 4)))
        pg.draw.line(background, palette['Light Trim'], (0, 146), (420, 146))
        pg.draw.line(background, palette['Dark Trim'], (0, 147), (420, 147))
        pg.draw.rect(background, palette['Dark Block'], pg.Rect((0, 149), (420, 91)))
        self.background = background