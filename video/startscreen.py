import os
import pygame as pg
from data.const import Colour
from domain.sprite import Sprite
from domain.screen import Screen
from domain.animation import Animation, AnimatedSprite
from video.menuscreen import MenuScreen
from video.vignettes import Scanlines, StaticVignette, ShadowVignette
from scripts.centre_div import centre_div
from scripts.separate_spritesheet import separate_spritesheet as sep_sheet

class StartScreen(Screen):
    def __init__(self, parent):
        super().__init__((420, 240), parent)
        self.draw_background()
        self.overlays.append(ImpactFlash(self))
        self.overlays.append(Scanlines(self))
        self.overlays.append(StaticVignette(self))
        self.overlays.append(ShadowVignette(self))
        self.state = "BOOTING"
        self.sprites.append(Title(self))
        self.sprites.append(StartDialogue(self))
        self.sprites.append(GlitchedTitle(self))
        self.sprites.append(UpperBlind(self))
        self.sprites.append(LowerBlind(self))
    
    @property
    def state(self): return self.__state
    
    @state.setter
    def state(self, state):
        states = {"BOOTING", "FLASHING", "GLITCHING", "READY", "CLOSING"}
        if state not in states: raise ValueError(f"Unrecognised state of StartScreen: {state}")
        self.__state = state

    def draw_background(self):
        palette = self.get_palette()
        colour = palette['Light Block']
        background = pg.Surface((420, 240))
        background.fill(colour)
        self.background = background
        
    def events(self, events):
        for event in events:
            if event.type in {pg.KEYUP, pg.MOUSEBUTTONUP}:
                if self.state in {"BOOTING", "FLASHING"}: self.state = "GLITCHING"
                if self.state == "READY": self.state = "CLOSING"
        super().events(events)
        
    def updates(self):
        super().updates()

class Title(Sprite):
    def __init__(self, startscreen):
        pos = (0, 59); size = (420, 88) 
        super().__init__(pos, size, parent=startscreen)
        self.surfaces = sep_sheet('startscreen_title.png', size, m=0)
        self.surfaces.reverse()
        print(self.surfaces)
        self.frame_index = 0
        self.frame_count = 0
        self.Y = None; self.Ypos = (196, -43)
        self.draw_Y()
        
    @property
    def surface(self):
        return self.surfaces[self.frame_index]
        
    def draw_Y(self):
        self.Y = pg.Surface((28, 43), pg.SRCALPHA)
        self.Y.blit(self.surfaces[-1], (-196, -22))
    
    def updates(self):
        if self.parent.state == "BOOTING":
            if self.frame_count > self.game.framerate // 2:
                self.frame_index += 1
                self.frame_count = 0
            if self.frame_index == 4:
                # s = 43 + 59 + 22 = 124
                # s = ut + 1/2 at^2
                # s = 124; u = 0; v = /; a = ?; t = FR/2
                # 124 = 1/2 (a) (FR/2)^2
                # 248 = a * FR/2^2
                a = 248 / (self.game.framerate / 2)**2 
                # s = ?; u = 0; v = /; a = a; t = frame_count
                # s = ut + 1/2 at^2
                s = (a * self.frame_count ** 2) // 2
                self.Ypos = (self.Ypos[0], s - 43)
                self.frame_count += 1
            elif self.frame_index == 5: self.parent.state = "FLASHING"
            else: self.frame_count += 1
        else: self.Ypos = (163, 81)
        if self.parent.state in {"GLITCHING", "READY", "CLOSING"}: self.visible = False
    
    def draw(self, surface):
        super().draw(surface)
        if self.frame_index == 4: surface.blit(self.Y, self.Ypos)

class ImpactFlash(Sprite):
    def __init__(self, startscreen):
        self.parent = startscreen
        self.rect = pg.Rect((0, 0), startscreen.size)
        self.frame = 0
        self.visible = False
        self.draw_surface()
        self.alpha = 255
        
    def draw_surface(self):
        self.surface = pg.Surface(self.size, pg.SRCALPHA)
        self.surface.fill(Colour.bone_white)
    
    def updates(self):
        if self.parent.state != "FLASHING":
            self.frame = 0
            self.visible = False
            return
        self.visible = True
        if self.alpha > 0:
            deci_perc = self.frame / (self.game.framerate // 3)
            self.alpha = 255 - int(deci_perc * 255)
            self.surface.set_alpha(self.alpha)
        self.frame += 1
        if self.frame > (self.game.framerate * 2) // 3: self.parent.state = "GLITCHING"
        
class StartDialogue(Sprite):
    def __init__(self, startscreen):
        self.parent = startscreen
        self.draw_surfaces()
        self.frame_count = 0
        self.frame_index = 0
        self.rect = pg.Rect((0, 0), self.surface.get_size())
        self.pos = (centre_div(420, self.size[0]), 158)
        self.visible = False
    
    @property
    def surface(self):
        return self.surfaces[self.frame_index]
    
    def draw_surfaces(self):
        self.surfaces = []
        font_path = os.path.join('fonts', 'Marksman.otf')
        font = pg.font.Font(font_path, 16)
        dialogue = "PRESS ANY BUTTON TO START"
        colour = Colour.black
        for i in range(2): self.surfaces.append(font.render(dialogue, False, colour))
        self.surfaces[1].set_alpha(63)
    
    def updates(self):
        if self.parent.state in {"GLITCHING", "READY"}:
            self.visible = True
            self.frame_count = (self.frame_count + 1) % int(self.game.framerate  * 0.75)
            if self.frame_count == 0: self.frame_index = 1 - self.frame_index
        else: self.visible = False

class GlitchedTitle(AnimatedSprite):
    def __init__(self, startscreen):
        pos = (0, 59); size = (420, 88) 
        super().__init__(pos, size, parent=startscreen)
        self.load_animation()
        self.done = False
        
    def load_animation(self):
        path = os.path.join('images', 'menu', 'glitchlogo.gif')
        anim = Animation()
        anim.load_from_gif(path)
        self.animations["idle"] = anim
        self.default_image = anim.frames[-1]
        
    def on_idle(self):
        if self.parent.state in {"BOOTING", "FLASHING"}: self.visible = False
        elif not self.parent.state == "GLITCHING": return
        elif len(self.frame_queue) == 0:
            if self.done:
                self.parent.state = "READY"
                return
            self.visible = True
            anim = self.animations["idle"]
            duration = (self.game.framerate * len(anim)) // 10
            self.play_animation(anim, duration)
            self.done = True

class UpperBlind(Sprite):
    def __init__(self, startscreen):
        pos = (0, -50); size = (420, 50)
        super().__init__(pos, size, parent=startscreen)
        self.draw_surface()
        self.frame = 0
    
    def draw_surface(self):
        palette = self.get_palette()
        surface = pg.Surface(self.size)
        surface.fill(palette['Dark Block'])
        trim = pg.Surface((420, 4))
        trim.fill(Colour.black)
        pg.draw.line(trim, palette['Light Trim'], (0, 1), (420, 1))
        pg.draw.line(trim, palette['Dark Trim'], (0, 2), (420, 2))
        surface.blit(trim, (0, 46))
        self.surface = surface
        
    def updates(self):
        if self.parent.state == "CLOSING":
            self.visible = True
            deciperc = self.frame / (self.game.framerate // 3)
            self.pos = (0, int(deciperc*50 -50))
            self.frame += 1
            if self.frame > self.game.framerate // 3:
                menu = MenuScreen(self.game)
                menu.open()
                self.parent.close()
        else: self.visible = False
            
class LowerBlind(Sprite):
    def __init__(self, startscreen):
        pos = (0, 240); size = (420, 91)
        super().__init__(pos, size, parent=startscreen)
        self.draw_surface()
        self.frame = 0
    
    def draw_surface(self):
        palette = self.get_palette()
        surface = pg.Surface(self.size)
        surface.fill(palette['Dark Block'])
        trim = pg.Surface((420, 4))
        trim.fill(Colour.black)
        pg.draw.line(trim, palette['Light Trim'], (0, 1), (420, 1))
        pg.draw.line(trim, palette['Dark Trim'], (0, 2), (420, 2))
        surface.blit(trim, (0, 0))
        self.surface = surface
        
    def updates(self):
        if self.parent.state == "CLOSING":
            self.visible = True
            deciperc = self.frame / (self.game.framerate // 3)
            self.pos = (0, int(240 - deciperc*91))
            self.frame += 1
        else: self.visible = False