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
        self.sprites.append(MenuCardCursor(self))
    
    @property
    def state(self): return self.__state
    
    @state.setter
    def state(self, state):
        states = {"DEALING", "READY"}
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
        
    def events(self, events):
        super().events(events)
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3 and MenuCard.selected_card is not None:
                    MenuCard.selected_card = None
                    
    def updates(self):
        self.game.cursor.state = "POINTER"
        super().updates()

class MenuSlot(Sprite):
    def __init__(self, menuscreen):
        pos = (186, 68); size = (48, 62)
        super().__init__(pos, size, parent=menuscreen)
        self.draw_surfaces()
        self.frame_index = 0
        self.frame = 0
        
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
        
    def updates(self):
        if self.parent.state == "READY" and MenuCard.selected_card is not None:
            if self.moused_over:
                self.game.cursor.state = "PLAY"
                self.frame = 0
                self.frame_index = 1
            else:
                if (self.frame // (self.game.framerate // 2)) % 2 == 0:
                    self.frame_index = 2
                else:
                    self.frame_index = 1
                self.frame = (self.frame + 1) % self.game.framerate
        
class MenuCard(Sprite):
    cards = []
    selected_card = None
    images = None
    names = {0: "Story",
            1: "Rogue",
            2: "Duels",
            3: "Puzzles",
            4: "Compendium",
            5: "Options",
            6: "Quit"}

    def __init__(self, index, menuscreen):
        if MenuCard.images is None: MenuCard.images = separate_spritesheet(os.path.join('menu', 'menucards.png'), (42, 56), m=0)
        pos = (0, 0); size = (42, 56)
        super().__init__(pos, size, parent=menuscreen)
        self.card_index = index
        self.name = MenuCard.names[index]
        self.draw_surface()
        self.frame_index = 0
        self.arc_index = 0
        self.frame = 0
        #
        self.nameimage = MenuCardName(self)
        self.parent.sprites.append(self.nameimage)
        MenuCard.cards.append(self)
    
    @property
    def surface(self):
        return self.__surfaces[self.frame_index]
    
    @property
    def selected(self):
        return MenuCard.selected_card is self
        
    @selected.setter
    def selected(self, boolean):
        if boolean == self.selected: return
        if boolean: MenuCard.selected_card = self
        else: MenuCard.selected_card = None
    
    def draw_surface(self):
        self.__surfaces = MenuCard.images[2*self.card_index : 2*self.card_index+2]
        
    def on_left_click(self):
        if not self.selected: self.selected = True
        print("I'm selected!")
        
    def updates(self):
        if self.parent.state == "READY":
            X, Y = self.parent.overlays[0].target_pos(self)
            self.nameimage.set_pos_from_menucard()
            self.frame_index = 0
            if not self.selected:
                self.frame_index = self.moused_over
                self.pos = X, Y
                self.arc_index = 0
                self.frame = 0
            else:
                if not self.frame >= self.game.framerate // 4: self.frame += 1
                else:
                    self.frame = 0
                    self.arc_index = (self.arc_index + 1) % 6
                arc = [-17, -20, -17, -13, -10, -13]
                Y += arc[self.arc_index]
                self.pos = (X, Y)
        
class MenuCardName(Sprite):
    def __init__(self, menucard):
        font_path = os.path.join('fonts', 'Marksman.otf')
        font = pg.font.Font(font_path, 16)
        #palette = menucard.get_palette()
        image = font.render(menucard.name.upper(), False, Colour.bone_white)
        size = image.get_size(); pos = (0, 0)
        super().__init__(pos, size, parent=menucard.parent)
        self.menucard = menucard
        self.surface = image
        
    def set_pos_from_menucard(self):
        x, y = self.menucard.pos
        x += self.menucard.size[0] // 2 - self.size[0] // 2
        y += self.menucard.size[1] + 4
        self.pos = (x, y)
        
    def updates(self):
        self.visible = False
        if self.parent.state == "READY":
            if self.pos == (0, 0): self.set_pos_from_menucard()
            self.visible = self.menucard.moused_over and not self.menucard.selected
        
class MenuCardCursor(Sprite):
    def __init__(self, menuscreen):
        size = (44, 58); pos = (0, 0)
        super().__init__(pos, size, parent=menuscreen)
        self.draw_surfaces()
        self.frame = 0
        self.frame_index = 0
        
    @property
    def surface(self):
        return self.__surfaces[self.frame_index]
    
    def draw_surfaces(self):
        path = os.path.join('menu', 'menucard_cursor.png')
        self.__surfaces = separate_spritesheet(path, self.size, 0)
        
    def updates(self):
        self.visible = False
        if self.parent.state == "READY":
            self.frame += 1
            if self.frame > self.game.framerate // 5:
                self.frame = 0
                self.frame_index = (self.frame_index + 1) % 5
            for card in MenuCard.cards:
                if card.moused_over and not card.selected:
                    x, y = card.pos
                    x -= 1; y -= 1
                    self.pos = (x, y)
                    self.visible = True