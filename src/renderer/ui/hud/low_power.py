import pyglet as pg
import pyglet.gl as gl
from pgext import ColorFramebuffer

from config import Config
from .base import HudBase

from assets.images.battery import BatteryLarge


class HUDLowPower(HudBase):
	def __init__(self, w: int, h: int):
		self.buf = ColorFramebuffer(w, h)
		self.batch = pg.graphics.Batch()
		self.drawables = []

		self.drawables.append(
			pg.text.Label(
				"Low Battery",
				font_name=Config.Fonts.display.name,
				font_size=Config.Fonts.display_size * 2,
				color=(255, 80, 80, 255),
				x=w // 2,
				y=h // 2 + Config.Fonts.display_size,
				anchor_x="center",
				anchor_y="bottom",
				batch=self.batch,
			)
		)

		self.drawables.append(
			pg.text.Label(
				"Returning to base.",
				font_name=Config.Fonts.display.name,
				font_size=Config.Fonts.display_size,
				color=(255, 255, 255, 255),
				x=w // 2,
				y=h // 2 + Config.Fonts.display_size,
				anchor_x="center",
				anchor_y="top",
				batch=self.batch,
			)
		)

		self.drawables.append(
			BatteryLarge(
				w // 2 - BatteryLarge.width // 2,
				h // 2 - BatteryLarge.height - Config.Fonts.display_size,
				batch=self.batch,
			)
		)

	@property
	def texture(self):
		return self.buf.texture

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.buf.unbind()
