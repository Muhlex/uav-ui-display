from enum import Enum
from pyglet.math import Vec3

from util import Observable


class UAVState(Enum):
	NONE = 0
	LOW_POWER = 1
	SEARCH = 2
	AWAIT_CONTROL = 3
	APPROACH = 4
	AWAIT_COMMAND = 5
	CANCEL_COMMAND = 6
	SELECT_TARGET = 7


class State(Observable):
	has_operator = False
	uav_state = UAVState.LOW_POWER
	uav_origin = Vec3(0.0, 0.0, 0.0)
	operator_origin = Vec3(0.0, 0.0, 0.0)
	operator_dir_yaw = 0.0
	target_origin = Vec3(0.0, 0.0, 0.0)
	battery_frac = 0.25

	def __init__(self):
		self.subscribe("operator_origin", self._update_operator_dir_yaw)
		self.subscribe("uav_origin", self._update_operator_dir_yaw)

	def _update_operator_dir_yaw(self, _):
		operator_dir = (self.operator_origin - self.uav_origin).normalize()
		self.operator_dir_yaw = operator_dir.get_pitch_yaw()[1]


state = State()
