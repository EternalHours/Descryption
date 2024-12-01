import os
import pygame as pg
from data.const import Colour
from domain.screen import Screen
from domain.sprite import Sprite
from video.handoverlay import HandOverlay
from video.vignettes import Scanlines, StaticVignette, ShadowVignette
from scripts.separate_spritesheet import separate_spritesheet
from scripts.transition_colour import transition_colour

class MenuScreen(Screen):
    def __init__(self, parent):
        super().__init__((420, 240), parent)
        self.draw_background()
        self.overlays.append(HandOverlay(self, (42, 70)))
        self.overlays.append(Scanlines(self))
        self.overlays.append(StaticVignette(self))
        self.overlays.append(ShadowVignette(self))
        self.state = "DEALING"
        self.sprites.append(MenuSlot(self))
        self.add_menucards()
    
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
        
    def add_menucards(self):
        for i in range(7): self.overlays[0].add_sprite(MenuCard(i, self))

class MenuSlot(Sprite):
    def __init__(self, menuscreen):
        pos = (186, 68); size = (48, 62)
        super().__init__(pos, size, parent=menuscreen)
        self.draw_surfaces()
        self.frame_index = 0
        
    @property
    def surface(self):
        return self.surfaces[self.frame_index]
        
    def draw_surfaces(self):
        image = pg.image.load(os.path.join('images', 'menu', 'menuslot.png')).convert_alpha()
        palette = self.get_palette()
        colours = [palette['Light Block'], palette['Light Trim']]
        colours.append(transition_colour(colours[0], colours[1]))
        surfaces = []
        for i in range(3):
            surfaces.append(pg.Surface(self.size))
            surfaces[i].fill(colours[i])
        pg.draw.rect(surfaces[0], (31, 32, 40, 168), pg.Rect((0, 2), (48, 60)))
        pg.draw.rect(surfaces[0], Colour.black, pg.Rect((3, 3), (42, 46)))
        pg.draw.line(surfaces[0], colours[0], (3, 59), (44, 59))
        for i in range(3): surfaces[i].blit(image, (0, 0))
        self.surfaces = surfaces
        
class MenuCard(Sprite):
    cards = None
    names = {0: "Story",
            1: "Rogue",
            2: "Duels",
            3: "Puzzles",
            4: "Compendium",
            5: "Options",
            6: "Quit"}

    def __init__(self, index, menuscreen):
        if MenuCard.cards is None: MenuCard.cards = separate_spritesheet(os.path.join('menu', 'menucards.png'), (42, 56), m=0)
        pos = (0, 0); size = (42, 56)
        super().__init__(pos, size, parent=menuscreen)
        self.card_index = index
        self.name = MenuCard.names[index]
        self.draw_surface()
        self.frame_index = 0
    
    @property
    def surface(self):
        return self.__surfaces[self.frame_index]
    
    def draw_surface(self):
        self.__surfaces = MenuCard.cards[2*self.card_index : 2*self.card_index+2]
        
    def updates(self):
        self.pos = self.parent.overlays[0].target_pos(self)
        self.frame_index = self.moused_over