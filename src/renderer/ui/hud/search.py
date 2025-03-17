import pyglet as pg
from pgext import ColorFramebuffer

from config import Config
from .base import HudBase


class HUDSearch(HudBase):
	def __init__(self, w: int, h: int):
		self.buf = ColorFramebuffer(w, h)
		self.batch = pg.graphics.Batch()
		drawables = []

		drawables.append(
			pg.text.Label(
				"Searching...",
				font_name=Config.Fonts.display.name,
				font_size=Config.Fonts.display_size * 2,
				color=(155, 175, 255, 255),
				x=w // 2,
				y=h // 2,
				anchor_x="center",
				anchor_y="center",
				batch=self.batch,
			)
		)
		self.buf.bind()
		self.batch.draw()
		self.buf.unbind()

	@property
	def texture(self):
		return self.buf.texture

	def render(self):
		pass
