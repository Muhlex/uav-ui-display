import pyglet as pg
import pyglet.gl as gl

from config import Config
from .base import HUDBase

from components.battery import BatterySmall
from components.gesture import GestureLarge, GestureType

img_icon_abort = pg.resource.image("assets/images/icon/back_large.png")


class HUDMoveToTarget(HUDBase):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.batch = pg.graphics.Batch()

		self.battery = BatterySmall(width // 2 - BatterySmall.width // 2, 0, batch=self.batch)

		self.icon_gesture = GestureLarge(
			width // 2 - 24,
			height // 2 + 4,
			GestureType.ABORT,
			Config.Colors.warn,
		)
		self.icon_action = pg.sprite.Sprite(
			img_icon_abort,
			self.icon_gesture.x + self.icon_gesture.radius + 8,
			self.icon_gesture.y - img_icon_abort.height // 2,
			batch=self.batch,
		)
		self.icon_action.color = Config.Colors.warn

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.icon_gesture.draw()
		self.buf.unbind()
