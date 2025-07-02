import pyglet as pg
import pyglet.gl as gl

# from config import Config
from .base import HUDBase

from components.battery import BatteryLarge


class HUDLowPower(HUDBase):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.yawspeed = -0.08

		self.batch = pg.graphics.Batch()

		self.battery = BatteryLarge(
			width // 2 - BatteryLarge.width // 2,
			height // 2 - BatteryLarge.height // 2,
			batch=self.batch,
		)

		# self.title_label = pg.text.Label(
		# 	"Low Battery",
		# 	font_name=Config.Fonts.display.name,
		# 	font_size=Config.Fonts.display_size * 2,
		# 	color=Config.Colors.negative,
		# 	x=width // 2,
		# 	y=self.battery.y - 8,
		# 	anchor_x="center",
		# 	anchor_y="top",
		# 	batch=self.batch,
		# )

		# self.status_label = pg.text.Label(
		# 	"Returning to base.",
		# 	font_name=Config.Fonts.display.name,
		# 	font_size=Config.Fonts.display_size,
		# 	color=(255, 255, 255, 255),
		# 	x=width // 2,
		# 	y=self.title_label.y - self.title_label.font_size - 4,
		# 	anchor_x="center",
		# 	anchor_y="top",
		# 	batch=self.batch,
		# )

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.buf.unbind()
