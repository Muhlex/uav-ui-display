import pyglet as pg

from config import Config
from .base import HudBase


class HudSearch(HudBase):
	def activate(self, tex):
		pass

	def draw(self, tex):
		rect = pg.shapes.Rectangle(1, 1, tex.width - 2, tex.height - 2, color=(50, 50, 150, 255))
		rect.draw()
		label = pg.text.Label(
			"Wave to\ncontrol",
			font_name=Config.Fonts.display.name,
			font_size=Config.Fonts.display_size * 2,
			align="center",
			x=tex.width // 2,
			y=tex.height // 2,
			width=tex.width,
			anchor_x="center",
			anchor_y="center",
			multiline=True,
		)
		label.draw()
