import pygame as pg
from datetime import datetime
from domain.game import Game
from domain.savemanagers import SaveFile
from video.startscreen import StartScreen

pg.init()

# Load the most recent save file or create one if none exists.
savefile = None
datetime = datetime.now().strftime('%Y%m%d%H%M%S')
try: savefile = SaveFile.load()
except Exception as e:
    SaveFile.create(datetime, override=True)
    savefile = SaveFile.load(datetime)
    print(e)

# Ready game with loaded save file.
game = Game(savefile)
game.create_window()
start = StartScreen(game)
start.open()

game.main()
