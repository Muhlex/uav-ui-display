import pyglet as pg
import pyglet.gl as gl

from config import Config
from state import state
from .base import HUDBase

from components.battery import BatterySmall
from components.gesture import GestureLarge, GestureType

img_icon_dropoff = pg.resource.image("assets/images/icon/dropoff_large.png")
img_icon_abort = pg.resource.image("assets/images/icon/abort_large.png")


class HUDMoveToTarget(HUDBase):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.batch = pg.graphics.Batch()

		self.battery = BatterySmall(width // 2 - BatterySmall.width // 2, 0, batch=self.batch)

		self.icon_gesture = GestureLarge(
			width // 2 - 24,
			height // 2 + 4,
			GestureType.CONFIRM,
			Config.Colors.positive,
		)
		self.icon_action = pg.sprite.Sprite(
			img_icon_dropoff,
			self.icon_gesture.x + self.icon_gesture.radius + 8,
			self.icon_gesture.y - img_icon_dropoff.height // 2,
			batch=self.batch,
		)
		self.icon_action.color = Config.Colors.positive

		def cycle_gesture(gesture_type: GestureType | None = None):
			if gesture_type is None:
				gesture_type = (
					GestureType.ABORT
					if self.icon_gesture.type == GestureType.CONFIRM
					else GestureType.CONFIRM
				)

			color = {
				GestureType.ABORT: Config.Colors.negative,
				GestureType.CONFIRM: Config.Colors.positive,
			}.get(gesture_type, Config.Colors.white)

			self.icon_gesture.type = gesture_type
			self.icon_gesture.color = color
			self.icon_action.color = color
			self.icon_action.image = (
				img_icon_abort if gesture_type == GestureType.ABORT else img_icon_dropoff
			)

		def on_cycle_operator_gesture_type(dt: float):
			if self.icon_gesture.type == state.operator_gesture_type:
				return
			cycle_gesture()

		pg.clock.schedule_interval(on_cycle_operator_gesture_type, 1.5)

		def on_change_operator_gesture_type(value: GestureType):
			if value != GestureType.CONFIRM and value != GestureType.ABORT:
				return
			cycle_gesture(value)

		state.subscribe("operator_gesture_type", on_change_operator_gesture_type)

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.icon_gesture.draw()
		self.buf.unbind()
