import os
import pygame as pg
from PIL import Image
from domain.sprite import Sprite

class Animation:
    def __init__(self):
        # Initialise Attributes:
        self.frames = []
    
    def load_from_dir(self, path):
        '''Use to load all images in a given directory into the animation.'''
        # Path should be to a folder of images representing unique animation frames.
        self.frames = []
        for filename in sort(os.listdir(path)):
            if filename.endswith((".png", ".jpg")):
                image = pg.image.load(os.path.join(path, filename))
                image.convert_alpha()
                self.frames.append(image)
    
    def load_from_gif(self, path):
        '''Use to load all frames in a gif into the animation.'''
        self.frames = []
        gif = Image.open(path)
        for i in range(gif.n_frames):
            gif.seek(i)
            frame_rgba = gif.convert("RGBA")
            frame_image = pg.image.fromstring(frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode)
            self.frames.append(frame_image)
    
    def stretch_surface(self, right, down, left=0, up=0):
        '''Use to stretch the image surface by a desired number of pixels without resizing the image content.'''
        pos = (left, up)
        size = (left + right, up + down)
        for i in range(len(self.frames)):
            frame = self.frames[i]
            surface = pg.Surface(size).convert_alpha()
            surface.blit(frame, pos)
            self.frames[i] = surface
    
    def fit_duration(self, duration):
        '''Use to return the animation frames, stretched to match the specified duration in frames.'''
        # Assumes the duration is larger than the animation length.
        if duration == len(self): return self.frames
        stretch = duration // len(self)
        frames = self.frames * stretch
        remainder = duration - len(frames)
        step = duration // remainder
        anim_frames = []
        for i in range(len(frames)):
            anim_frames += frames[i] * (1 + (i % step == 0))
        return anim_frames
    
    def append(self, item): self.frames.append(item)
    def remove(self, item): self.frames.remove(item)
    def __getitem__(self, index): return self.frames[index]
    def __len__(self): return len(self.frames)
    def __iter__(self): return iter(Self.frames)
        
class AnimatedSprite(Sprite):
    def __init__(self, pos, size, parent):
        super().__init__(pos, size, parent)
        
        # Initialise Attributes:
        self.default_image = pg.Surface(size).convert_alpha()
        self.animations = {}
        self.frame_queue = []
        self.paused = False
    
    def on_idle(self):
        '''Exists to be overriden. Will be called every frame whilst sprite is idle.'''
        pass
    
    def queue_animation(self, animation, duration=None):
        if not animation in self.animations.values(): raise ValueError(f"Unrecognised Animation of {self}: {animation}")
        if not isinstance(animation, Animation): raise TypeError(f"Animation type unrecognised: {type(animation)}")
        if duration is None: duration = len(animation)
        frames = animation.fit_duration
        self.frame_queue += frames
    
    def play_animation(self, animation, duration=None):
        try:
            self.stop_animation()
            self.queue_animation(animation, duration)
            self.anim_paused = False
        except Error as e: raise e
    
    def stop_animation(self):
        self.frame_queue = []
        self.anim_paused = True
        
    def is_idle(self):
        '''Use to determine whether the sprite has naturally run out of frames and should call its on_idle.'''
        return len(self.frame_queue) == 0 and self.anim_paused
        
    def update_frame(self):
        '''Use during the updates phase to determine the image to display during the draw phase.'''
        if len(self.frame_queue) == 0 or self.anim_paused: self.surface = self.default_image
        else: self.surface = self.frame_queue.pop(0)
    
    def update(self):
        '''Overridden updates loop.'''
        super().updates()
        if self.is_idle: self.on_idle()
        self.update_frame()
            
            
            
        