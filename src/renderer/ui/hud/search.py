import pyglet as pg

from config import Config
from ...dynamic_texture import DynamicTexture


class HUDSearch(DynamicTexture):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.batch = pg.graphics.Batch()
		drawables = []

		drawables.append(
			pg.text.Label(
				"Searching...",
				font_name=Config.Fonts.display.name,
				font_size=Config.Fonts.display_size * 2,
				color=(155, 175, 255, 255),
				x=width // 2,
				y=height // 2,
				anchor_x="center",
				anchor_y="center",
				batch=self.batch,
			)
		)
		self.buf.bind()
		self.batch.draw()
		self.buf.unbind()

	def render(self):
		pass
