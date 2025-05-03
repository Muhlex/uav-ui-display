from math import pi, radians, degrees
from pyglet.math import clamp
from util import map_range

import pyglet as pg
import pyglet.gl as gl

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

		def get_bystander_overlap(yaw: float, other_yaw: float, radius: float):
			delta = (yaw - other_yaw + pi) % (2 * pi) - pi
			distance = abs(delta)
			overlap = 2 * radius - distance
			if overlap <= 0:
				return None
			if delta < 0:
				overlap = -overlap
			return overlap

		def adjust_bystander_yaw(yaw: float, other_yaws: list[float], radius: float):
			if len(other_yaws) == 0:
				return yaw
			closest_yaw = min(other_yaws, key=lambda y: abs(y - yaw))
			overlap = get_bystander_overlap(yaw, closest_yaw, radius)
			if overlap is None:
				return yaw
			result = yaw + overlap + (0.001 if overlap >= 0 else -0.001)

			closest_yaw = min(other_yaws, key=lambda other_yaw: abs(other_yaw - result))
			overlap = get_bystander_overlap(result, closest_yaw, radius)
			if overlap is None:
				return result
			return None

		def on_change_bystander_dir_yaws(bystander_dir_yaws: list[float]):
			add_count = len(bystander_dir_yaws) - len(self.bystanders)
			if add_count > 0:
				for _ in range(add_count):
					self.bystanders.append(Person(0, 0, 4, batch=self.batch))
			elif add_count < 0:
				for _ in range(-add_count):
					bystander = self.bystanders.pop()
					bystander.delete()

			bystanders = zip(state.bystander_origins, bystander_dir_yaws)
			bystanders = [(origin.distance(state.uav_origin), yaw) for origin, yaw in bystanders]
			bystanders_near_to_far = sorted(bystanders, key=lambda b: b[0])

			visible_bystander_yaws: list[float] = []
			for i, (distance, yaw) in enumerate(bystanders_near_to_far):
				bystander = self.bystanders[i]
				if distance > MAX_DISTANCE:
					bystander.visible = False
					continue

				adjusted_yaw = adjust_bystander_yaw(yaw, visible_bystander_yaws, radius=radians(6))
				if adjusted_yaw is None:
					bystander.visible = False
					continue
				visible_bystander_yaws.append(adjusted_yaw)

				bystander.visible = True
				bystander.x = round(canvas.yaw_to_x(adjusted_yaw))
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
