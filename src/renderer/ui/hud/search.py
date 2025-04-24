import pyglet as pg

from config import Config
from .base import HUDBase


class HUDSearch(HUDBase):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.yawspeed = 2.2

		self.batch = pg.graphics.Batch()

		line_count = 4
		gap = 6
		x = 1
		self.lines: list[pg.shapes.Line] = []
		for i in range(line_count):
			thickness = i * 2 + 1
			line = pg.shapes.Line(x, 0, x, height, thickness, Config.Colors.search, batch=self.batch)
			line.anchor_x = 0.0
			self.lines.append(line)
			x += thickness + gap

		self.buf.bind()
		self.batch.draw()
		self.buf.unbind()

	def render(self):
		pass
