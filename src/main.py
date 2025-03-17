import pyglet as pg

import config as config
from renderer import Renderer

renderer = Renderer()

renderer.debug.win.set_location(32, 64)
renderer.output.win.set_location(32, 64 + renderer.debug.win.height + 64)

pg.app.run()
