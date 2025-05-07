from dataclasses import dataclass

from math import pi, radians
from pyglet.math import clamp
from util import map_range

import pyglet as pg
import pyglet.gl as gl

from config import Config
from state import state, UAVState

from ..led_matrix_canvas import LEDMatrixCanvas
from .base import UIBase

from components.person import Person

MIN_DIST = 250
MAX_DIST = 1_500


class AwaitControl360(UIBase):
	def __init__(self, canvas: LEDMatrixCanvas, height: int):
		super().__init__(canvas.width, height)
		self.y_frac = 0.0

		self.batch = pg.graphics.Batch()

		def on_change_uav_state(uav_state: UAVState):
			self.visible = uav_state == UAVState.AWAIT_CONTROL

		state.subscribe("uav_state", on_change_uav_state, immediate=True)

		self.bystanders_icons: list[Person] = []

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
			new_len = len(bystander_dir_yaws)
			add_count = new_len - len(self.bystanders_icons)
			if add_count > 0:
				for i in range(add_count):
					self.bystanders_icons.append(Person(i, 0, 0))
			elif add_count < 0:
				for _ in range(-add_count):
					icon = self.bystanders_icons.pop()
					icon.delete()

			@dataclass
			class Bystander:
				index: int
				yaw: float
				distance: float

			bystanders = [
				Bystander(
					i, bystander_dir_yaws[i], state.bystander_origins[i].distance(state.uav_origin)
				)
				for i in range(new_len)
			]

			bystanders_near_to_far = sorted(bystanders, key=lambda b: b.distance)

			visible_bystander_yaws: list[float] = []
			for bystander in bystanders_near_to_far:
				yaw = bystander.yaw
				distance = bystander.distance
				icon = self.bystanders_icons[bystander.index]
				if distance > MAX_DIST:
					icon.visible = False
					continue

				adjusted_yaw = adjust_bystander_yaw(yaw, visible_bystander_yaws, radius=radians(6))
				if adjusted_yaw is None:
					icon.visible = False
					continue
				visible_bystander_yaws.append(adjusted_yaw)

				icon.visible = True
				icon.x = round(canvas.yaw_to_x(adjusted_yaw))
				icon.y = round(max(0, map_range(distance, MIN_DIST, MAX_DIST, 0, 48)))
				icon.scale = round(clamp(map_range(distance, MIN_DIST, MAX_DIST, 9, 2), 2, 9))

		state.subscribe("bystander_dir_yaws", on_change_bystander_dir_yaws, immediate=True)

		def on_change_bystander_arms_angles(
			bystander_arms_angles: list[tuple[float, float, float, float]],
		):
			for i, angles in enumerate(bystander_arms_angles):
				icon = self.bystanders_icons[i]
				icon.set_arms_rotations(*angles)

		state.subscribe("bystander_arms_angles", on_change_bystander_arms_angles, immediate=True)

		def on_change_bystander_selected_index(index: int):
			for icon in self.bystanders_icons:
				icon.color = (255, 255, 255)
				icon.set_gesture_progress(0.0)
			if index >= 0 and index < len(self.bystanders_icons):
				self.bystanders_icons[index].color = Config.Colors.positive
				self.bystanders_icons[index].set_gesture_progress(state.operator_gesture_progress)

		state.subscribe(
			"bystander_selected_index", on_change_bystander_selected_index, immediate=True
		)

		def on_change_operator_gesture_progress(frac: float):
			index = state.bystander_selected_index
			if index >= 0 and index < len(self.bystanders_icons):
				self.bystanders_icons[index].set_gesture_progress(frac)

		state.subscribe("operator_gesture_progress", on_change_operator_gesture_progress)

	def render(self):
		self.buf.bind()

		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()

		active_icon: Person | None = None
		for i, icon in enumerate(self.bystanders_icons):
			if state.bystander_selected_index == i:
				active_icon = icon
			else:
				icon.draw()
		if active_icon is not None:
			active_icon.draw()

		self.buf.unbind()
