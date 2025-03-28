from enum import Enum
from pyglet.math import Vec3

from util import Observable


class UAVState(Enum):
	NONE = 0
	LOW_POWER = 1
	SEARCH = 2
	APPROACH = 3
	AWAIT_COMMAND = 4
	CANCEL_COMMAND = 5
	SELECT_TARGET = 6
	MOVE_TO_TARGET = 7


class State(Observable):
	has_operator = True
	has_target = False
	uav_state = UAVState.AWAIT_COMMAND
	uav_origin = Vec3(0.0, 0.0, 0.0)
	operator_origin = Vec3(0.0, 0.0, 0.0)
	target_origin = Vec3(0.0, 0.0, 0.0)
	battery_frac = 0.25

	operator_dir_yaw = 0.0
	operator_dir_pitch = 0.0
	target_dir_yaw = 0.0
	target_dir_pitch = 0.0

	def __init__(self):
		self.subscribe("operator_origin", self._update_operator_dir_yaw)
		self.subscribe("uav_origin", self._update_operator_dir_yaw)
		self.subscribe("target_origin", self._update_target_dir_yaw)
		self.subscribe("uav_origin", self._update_target_dir_yaw)

	def _update_operator_dir_yaw(self, _):
		dir = (self.operator_origin - self.uav_origin).normalize()
		pitch, yaw = dir.get_pitch_yaw()
		self.operator_dir_yaw = yaw
		self.operator_dir_pitch = pitch

	def _update_target_dir_yaw(self, _):
		dir = (self.target_origin - self.uav_origin).normalize()
		pitch, yaw = dir.get_pitch_yaw()
		self.target_dir_yaw = yaw
		self.target_dir_pitch = pitch


state = State()
