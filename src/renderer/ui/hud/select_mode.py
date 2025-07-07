import pyglet as pg
import pyglet.gl as gl

from config import Config
from .base import HUDBase

from components.battery import BatterySmall
from components.gesture import Gesture, GestureType

img_icon_dropoff = pg.resource.image("assets/images/icon/dropoff.png")
img_icon_abort = pg.resource.image("assets/images/icon/back.png")


class HUDSelectMode(HUDBase):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.batch = pg.graphics.Batch()

		self.battery = BatterySmall(width // 2 - BatterySmall.width // 2, 0, batch=self.batch)

		self.gesture_point = Gesture(
			width // 2 - 22,
			height - 32,
			GestureType.POINT,
			Config.Colors.white,
		)
		self.icon_point = pg.sprite.Sprite(
			img_icon_dropoff,
			self.gesture_point.x - img_icon_dropoff.width // 2,
			self.gesture_point.y - int(self.gesture_point.radius) - img_icon_dropoff.height - 6,
			batch=self.batch,
		)

		self.gesture_abort = Gesture(
			width // 2 + 22,
			self.gesture_point.y,
			GestureType.ABORT,
			Config.Colors.warn,
		)
		self.icon_abort = pg.sprite.Sprite(
			img_icon_abort,
			self.gesture_abort.x - img_icon_dropoff.width // 2,
			self.gesture_abort.y - int(self.gesture_abort.radius) - img_icon_dropoff.height - 6,
			batch=self.batch,
		)
		self.icon_abort.color = Config.Colors.warn

		self.gestures = [self.gesture_point, self.gesture_abort]

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()

		active_gestures = []
		for gesture in self.gestures:
			if gesture.active:
				active_gestures.append(gesture)
			else:
				gesture.draw()
		for gesture in active_gestures:
			gesture.draw()

		self.buf.unbind()
