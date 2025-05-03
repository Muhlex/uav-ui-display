import pyglet as pg
import pyglet.gl as gl

from pyglet.math import clamp
from util import map_range

from state import state, UAVState

from ..led_matrix_canvas import LEDMatrixCanvas
from .base import UIBase

from components.person import Person

MIN_DISTANCE = 250
MAX_DISTANCE = 1_500


class AwaitControl360(UIBase):
	def __init__(self, canvas: LEDMatrixCanvas, height: int):
		super().__init__(canvas.width, height)
		self.y_frac = 0.0

		self.batch = pg.graphics.Batch()

		def on_change_uav_state(uav_state: UAVState):
			self.visible = uav_state == UAVState.AWAIT_CONTROL

		state.subscribe("uav_state", on_change_uav_state, immediate=True)

		self.bystanders: list[Person] = []

		def on_change_bystander_dir_yaws(bystander_dir_yaws: list[float]):
			add_count = len(bystander_dir_yaws) - len(self.bystanders)
			if add_count > 0:
				for _ in range(add_count):
					self.bystanders.append(Person(0, 0, 4, batch=self.batch))
			elif add_count < 0:
				for _ in range(-add_count):
					obstacle = self.bystanders.pop()
					obstacle.delete()

			bystanders = zip(state.bystander_origins, bystander_dir_yaws)
			bystanders = [(origin.distance(state.uav_origin), yaw) for origin, yaw in bystanders]
			bystanders_near_to_far = sorted(bystanders, key=lambda b: b[0])
			for i, (distance, yaw) in enumerate(bystanders_near_to_far):
				bystander = self.bystanders[i]
				bystander.visible = distance <= MAX_DISTANCE
				bystander.x = round(canvas.yaw_to_x(yaw))
				bystander.y = round(max(0, map_range(distance, MIN_DISTANCE, MAX_DISTANCE, 0, 48)))
				bystander.scale = round(
					clamp(map_range(distance, MIN_DISTANCE, MAX_DISTANCE, 9, 2), 2, 9)
				)

		state.subscribe("bystander_dir_yaws", on_change_bystander_dir_yaws, immediate=True)

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.buf.unbind()
