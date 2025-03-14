import config as config

from data import Data
from renderer import Renderer

import pyglet as pg

data = Data()
renderer = Renderer(data)

renderer.debug.win.set_location(32, 64)
renderer.output.win.set_location(32, 64 + renderer.debug.win.height + 64)

pg.app.run()
