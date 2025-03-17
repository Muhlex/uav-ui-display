import pyglet as pg
import pyglet.gl as gl

pg.image.Texture.default_mag_filter = gl.GL_NEAREST
pg.image.Texture.default_min_filter = gl.GL_NEAREST

@pg.app.event_loop.event
def on_window_close(window):
	pg.app.event_loop.exit()

pg.resource.add_font("assets/fonts/JetBrainsMono-Regular.ttf")
pg.resource.add_font("assets/fonts/JetBrainsMono-Bold.ttf")
pg.resource.add_font("assets/fonts/nihonium113.ttf")

class Config:
	class Fonts:
		debug = pg.font.load("JetBrains Mono")
		display = pg.font.load("Nihonium113")
		display_size = 12
