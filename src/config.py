import pyglet as pg
import pyglet.gl as gl

pg.image.Texture.default_mag_filter = gl.GL_NEAREST
pg.image.Texture.default_min_filter = gl.GL_NEAREST

pg.resource.add_font("assets/fonts/JetBrainsMono-Regular.ttf")
pg.resource.add_font("assets/fonts/JetBrainsMono-Bold.ttf")
pg.resource.add_font("assets/fonts/nihonium113.ttf")

class Config:
	class Fonts:
		debug = pg.font.load("JetBrains Mono")
		display = pg.font.load("Nihonium113")
		display_size = 12
	class Colors:
		white = (255, 255, 255)
		positive = (75, 255, 225)
		negative = (255, 75, 75)
		warn = (255, 180, 50)
		search = (25, 75, 255)
