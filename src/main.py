import pyglet as pg

from data import Data
from renderer import Renderer

pg.resource.add_font("assets/fonts/JetBrainsMono-Regular.ttf")
pg.resource.add_font("assets/fonts/JetBrainsMono-Bold.ttf")
pg.resource.add_font("assets/fonts/upheavtt.ttf")


@pg.app.event_loop.event
def on_window_close(window):
	pg.app.event_loop.exit()


data = Data()
renderer = Renderer(data)

pg.app.run()
