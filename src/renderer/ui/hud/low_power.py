import pyglet as pg
import pyglet.gl as gl

from config import Config
from ...dynamic_texture import DynamicTexture

from assets.images.battery import BatteryLarge


class HUDLowPower(DynamicTexture):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.batch = pg.graphics.Batch()
		self.drawables = []

		self.drawables.append(
			pg.text.Label(
				"Low Battery",
				font_name=Config.Fonts.display.name,
				font_size=Config.Fonts.display_size * 2,
				color=Config.Colors.error,
				x=width // 2,
				y=height // 2 + Config.Fonts.display_size,
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
				x=width // 2,
				y=height // 2 + Config.Fonts.display_size,
				anchor_x="center",
				anchor_y="top",
				batch=self.batch,
			)
		)

		self.drawables.append(
			BatteryLarge(
				width // 2 - BatteryLarge.width // 2,
				height // 2 - BatteryLarge.height - Config.Fonts.display_size,
				batch=self.batch,
			)
		)

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.buf.unbind()
