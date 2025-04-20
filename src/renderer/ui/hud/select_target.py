from enum import Enum
from math import atan2, sin, cos

import pyglet as pg
import pyglet.gl as gl

from config import Config
from state import state
from .base import HUDBase

from components.gesture import Gesture, GestureType


class LandmarkType(Enum):
	OPERATOR = 0
	UAV = 1
	TARGET = 2


class HUDSelectTarget(HUDBase):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.batch = pg.graphics.Batch()

		# self.gesture = Gesture(
		# 	width // 2,
		# 	height // 2,
		# 	GestureType.CONFIRM,
		# 	Config.Colors.positive,
		# )

		self.bg = pg.shapes.Box(0, 0, self.width, self.height, batch=self.batch)

		self.icons = {
			LandmarkType.OPERATOR: pg.shapes.Circle(
				0, 0, 3, color=Config.Colors.search, batch=self.batch
			),
			LandmarkType.UAV: pg.shapes.Circle(
				0, 0, 2, color=Config.Colors.positive, batch=self.batch
			),
			LandmarkType.TARGET: pg.shapes.Circle(
				0, 0, 1, color=Config.Colors.negative, batch=self.batch
			),
		}

	def update(self):
		padding = [8, 4]
		min_scale = 0.1
		origins = [state.operator_origin, state.uav_origin, state.target_origin]

		up = origins[LandmarkType.UAV.value] - origins[LandmarkType.OPERATOR.value]
		map_angle = atan2(up.x, up.z)

		def rotate_pos_xz(pos: pg.math.Vec3, angle: float):
			s = sin(angle)
			c = cos(angle)
			return pg.math.Vec3(
				pos.x * c - pos.z * s,
				pos.y,
				pos.x * s + pos.z * c,
			)

		origins = [rotate_pos_xz(origin, map_angle) for origin in origins]

		min_x = min(origins, key=lambda origin: origin.x).x
		min_z = min(origins, key=lambda origin: origin.z).z
		max_x = max(origins, key=lambda origin: origin.x).x
		max_z = max(origins, key=lambda origin: origin.z).z
		center = pg.math.Vec3((min_x + max_x) / 2, 0, (min_z + max_z) / 2)
		delta = pg.math.Vec3(max_x - min_x, 0, max_z - min_z)

		scale_x = (self.width - padding[0] * 2) / delta.x if delta.x != 0 else min_scale
		scale_z = (self.height - padding[1] * 2) / delta.z if delta.z != 0 else min_scale
		scale = min(scale_x, scale_z)

		map_origin = pg.math.Vec3(self.width / 2, 0, self.height / 2)

		def world_to_map(pos: pg.math.Vec3):
			pos_centered = pos - center
			return pos_centered * scale + map_origin

		for type, icon in self.icons.items():
			map_pos = world_to_map(origins[type.value])
			icon.position = (round(map_pos.x), round(map_pos.z))

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.update()
		# self.gesture.draw()
		self.buf.unbind()
