import pygame as pg
from datetime import datetime
from domain.game import Game
from domain.savemanagers import SaveFile
from video.startscreen import StartScreen

pg.init()

# Load the most recent save file or create one if none exists.
savefile = None
dtstring = datetime.now().strftime('%Y%m%d%H%M%S')
try: savefile = SaveFile.load()
except Exception as e:
    SaveFile.create(dtstring, override=True)
    savefile = SaveFile.load(dtstring)
    print(e)

# Ready game with loaded save file.
game = Game(savefile)
game.create_window()
start = StartScreen(game)
start.open()

game.main()

def display(surface):
    w = pg.display.set_mode(surface.get_size())
    w.blit(surface, (0, 0))
    pg.display.flip()
