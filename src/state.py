from enum import Enum

from pyglet.math import Vec3

from util import Observable


class UAVState(Enum):
	NONE = 0
	LOW_POWER = 1
	SEARCH = 2
	AWAIT_CONTROL = 3
	AWAIT_COMMAND = 4
	SELECT_TARGET = 5
	MOVE_TO_TARGET = 6
	HOVER_TARGET = 7


class GestureType(Enum):
	NONE = 0
	ABORT = 1
	CONFIRM = 2
	POINT = 3
	WAVE = 4


class State(Observable):
	# external inputs:
	uav_state = UAVState.NONE
	operator_origin = Vec3(-100.0, 0.0, 0.0)
	uav_origin = Vec3(100.0, 0.0, 0.0)
	target_origin = Vec3(-200.0, 0.0, 200.0)
	battery_frac = 0.75

	operator_gesture_type = GestureType.NONE
	operator_gesture_progress = 0.0

	bystander_origins: list[Vec3] = [
		Vec3(40.0, 0.0, -40.0),
		Vec3(500.0, 0.0, 0.0),
		Vec3(800.0, 0.0, -1000.0),
		Vec3(810.0, 0.0, -1010.0),
	]
	# left_shoulder, left_elbow, right_shoulder, right_elbow:
	# (all relative to operator, not one another)
	bystander_arms_angles: list[tuple[float, float, float, float]] = []
	bystander_selected_index: int = -1

	obstacles: list[tuple[Vec3, Vec3]] = [
		(Vec3(40.0, 0.0, 40.0), Vec3(40.0, 0.0, 400.0)),
		(Vec3(40.0, 0.0, 400.0), Vec3(800.0, 0.0, 400.0)),
	]

	# computed:
	has_operator = False
	# TODO: Remove pitches if they stay unused
	operator_dir_pitch = 0.0
	operator_dir_yaw = 0.0
	target_dir_pitch = 0.0
	target_dir_yaw = 0.0
	bystander_dir_yaws: list[float] = []

	def __init__(self):
		self.subscribe("uav_state", self._update_has_operator, immediate=True)

		self.subscribe("operator_origin", self._update_operator_dir_yaw, immediate=True)
		self.subscribe("uav_origin", self._update_operator_dir_yaw, immediate=True)

		self.subscribe("target_origin", self._update_target_dir_yaw, immediate=True)
		self.subscribe("uav_origin", self._update_target_dir_yaw, immediate=True)

		self.subscribe("bystander_origins", self._update_bystander_dir_yaws, immediate=True)
		self.subscribe("uav_origin", self._update_bystander_dir_yaws, immediate=True)

	def _update_has_operator(self, _):
		self.has_operator = self.uav_state not in {
			UAVState.NONE,
			UAVState.SEARCH,
			UAVState.AWAIT_CONTROL,
			UAVState.LOW_POWER,
		}

	def _update_operator_dir_yaw(self, _):
		dir = (self.operator_origin - self.uav_origin).normalize()
		pitch, yaw = dir.get_pitch_yaw()
		self.operator_dir_pitch = pitch
		self.operator_dir_yaw = yaw

	def _update_target_dir_yaw(self, _):
		dir = (self.target_origin - self.uav_origin).normalize()
		pitch, yaw = dir.get_pitch_yaw()
		self.target_dir_pitch = pitch
		self.target_dir_yaw = yaw

	def _update_bystander_dir_yaws(self, _):
		self.bystander_dir_yaws = [
			(bystander_origin - self.uav_origin).normalize().get_pitch_yaw()[1]
			for bystander_origin in self.bystander_origins
		]


state = State()
