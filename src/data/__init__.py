from enum import Enum


class UAV_State(Enum):
	SERACH = 0


class Data:
	uav_state = UAV_State.SERACH
	uav_origin = (0.0, 0.0, 0.0)
	target_origin = (0.0, 0.0, 0.0)
	operator_origin = (0.0, 0.0, 0.0)
