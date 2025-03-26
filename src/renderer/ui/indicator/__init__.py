from math import pi
from util import clamp, map_range

import pyglet as pg
import pyglet.gl as gl

from ..base import UIBase
from assets.images.eyes import Eyes

from state import state


class Indicator(UIBase):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.radius = height // 2
		self.search_yawspeed = -1.5

		self.batch = pg.graphics.Batch()
		self.eyes = Eyes(width // 2, height // 2, width, batch=self.batch)

		pg.clock.schedule_interval(self.tick, 1 / 60)

	def tick(self, dt: float):
		def pitch_to_y_frac(pitch: float):
			return clamp(map_range(pitch, -pi / 4, 0, 0, 0.6), 0, 0.6)

		if state.has_operator:
			self.yaw = state.operator_dir_yaw
			self.y_frac = pitch_to_y_frac(state.operator_dir_pitch)
		elif state.has_target:
			self.yaw = state.target_dir_yaw
			self.y_frac = pitch_to_y_frac(state.target_dir_pitch)
		else:
			unclamped_yaw = self.yaw + dt * self.search_yawspeed
			self.yaw = (unclamped_yaw + pi) % (2 * pi) - pi
			self.y_frac = 0.0

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.buf.unbind()
