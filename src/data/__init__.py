from enum import Enum
from math import pi

import pyglet as pg
from pyglet.math import Vec3


class UAV_State(Enum):
	NONE = 0
	LOW_POWER = 1
	SEARCH = 2
	AWAIT_CONTROL = 3
	APPROACH = 4
	AWAIT_COMMAND = 5
	CANCEL_COMMAND = 6
	SELECT_TARGET = 7


class Data:
	has_operator = False
	uav_state = UAV_State.SEARCH
	uav_origin = Vec3(0.0, 0.0, 0.0)
	operator_origin = Vec3(0.0, 0.0, 0.0)
	operator_yaw = 0.0
	target_origin = Vec3(0.0, 0.0, 0.0)

	scroll_yawspeed = -0.05
	scroll_yaw = 0.0

	def __init__(self):
		pg.clock.schedule_interval(self.tick, 1 / 30)

	def update(
		self,
		*,
		has_operator=None,
		uav_state=None,
		uav_origin=None,
		target_origin=None,
		operator_origin=None,
	):
		if has_operator is not None:
			self.has_operator = uav_state
		if uav_state is not None:
			self.uav_state = uav_state
		if uav_origin is not None:
			self.uav_origin = uav_origin
		if target_origin is not None:
			self.target_origin = target_origin
		if operator_origin is not None:
			self.operator_origin = operator_origin

		if uav_origin is not None or operator_origin is not None:
			operator_dir = (self.operator_origin - self.uav_origin).normalize()
			self.operator_yaw = operator_dir.get_pitch_yaw()[1]

	def tick(self, dt: float):
		unclamped = self.scroll_yaw + dt * self.scroll_yawspeed
		self.scroll_yaw = (unclamped + pi) % (2 * pi) - pi
