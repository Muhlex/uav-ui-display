from math import ceil

import pyglet as pg

from util import Insets
from state import state

outline_small = pg.resource.image("assets/images/battery_outline_small.png")
outline_large = pg.resource.image("assets/images/battery_outline_large.png")


class BatteryBase:
	def __init__(
		self,
		outline_texture: pg.image.Texture,
		fill_margins: Insets,
		x: int,
		y: int,
		batch: pg.graphics.Batch | None = None,
	):
		self.batch = batch or pg.graphics.Batch()

		self.outline = pg.sprite.Sprite(outline_texture, x, y, batch=self.batch)
		self.fill_max_w = outline_texture.width - fill_margins.left - fill_margins.right
		self.fill = pg.shapes.Rectangle(
			x + fill_margins.left,
			y + fill_margins.bottom,
			self.fill_max_w,
			outline_texture.height - fill_margins.top - fill_margins.bottom,
			color=(0, 255, 255, 255),
			batch=self.batch,
		)

		def on_change_battery_frac(frac: float):
			self.fill.width = ceil(self.fill_max_w * frac)
			if frac < 0.3:
				self.fill.color = (255, 50, 0, self.fill.color[3])
			elif frac < 0.7:
				self.fill.color = (255, 220, 0, self.fill.color[3])
			else:
				self.fill.color = (25, 255, 255, self.fill.color[3])

		def blink(dt: float):
			if state.battery_frac <= 0.2 and self.fill.color[3] == 255:
				self.fill.color = self.fill.color[:3] + (0,)
			else:
				self.fill.color = self.fill.color[:3] + (255,)

		state.subscribe("battery_frac", on_change_battery_frac, immediate=True)
		pg.clock.schedule_interval(blink, 0.4)

	@property
	def x(self):
		return self.outline.x

	@property
	def y(self):
		return self.outline.y

	def draw(self):
		self.batch.draw()


class BatterySmall(BatteryBase):
	width = outline_small.width
	height = outline_small.height

	def __init__(self, x: int, y: int, batch: pg.graphics.Batch | None = None):
		super().__init__(
			outline_small,
			Insets(3, 4, 3, 3),
			x,
			y,
			batch=batch,
		)


class BatteryLarge(BatteryBase):
	width = outline_large.width
	height = outline_large.height

	def __init__(self, x: int, y: int, batch: pg.graphics.Batch | None = None):
		super().__init__(
			outline_large,
			Insets(3, 5, 3, 3),
			x,
			y,
			batch=batch,
		)
