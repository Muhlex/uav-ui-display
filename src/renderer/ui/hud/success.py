import pyglet as pg
import pyglet.gl as gl

from config import Config
from .base import HUDBase

# from components.battery import BatterySmall

img_icon_success = pg.resource.image("assets/images/icon/success_large.png")


class HUDSuccess(HUDBase):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.yawspeed = -0.2

		self.batch = pg.graphics.Batch()

		# self.battery = BatterySmall(width // 2 - BatterySmall.width // 2, 0, batch=self.batch)

		self.icon = pg.sprite.Sprite(
			img_icon_success,
			width // 2 - img_icon_success.width // 2,
			height // 2 - img_icon_success.height // 2,
			batch=self.batch,
		)
		self.icon.color = Config.Colors.positive

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.buf.unbind()
