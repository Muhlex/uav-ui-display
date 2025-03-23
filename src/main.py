import pyglet as pg

import config as config
from ue.receive import UEReceiver
from renderer import Renderer

UEReceiver("ws://127.0.0.1:30020", ["RCP_LED"]).init()
renderer = Renderer()
renderer.debug.win.set_location(32, 64)
renderer.output.win.set_location(32, 64 + renderer.debug.win.height + 64)

pg.app.run()
