from enum import Enum
from math import atan2, sin, cos

import pyglet as pg
import pyglet.gl as gl

from config import Config
from state import state
from .base import HUDBase

from components.gesture import Gesture, GestureType

img_icon_uav = pg.resource.image("assets/images/icon/uav.png")
img_icon_uav.anchor_x = img_icon_uav.width // 2
img_icon_uav.anchor_y = img_icon_uav.height // 2
img_icon_target = pg.resource.image("assets/images/icon/target.png")
img_icon_target.anchor_x = img_icon_target.width // 2
img_icon_target.anchor_y = img_icon_target.height // 2


class LandmarkType(Enum):
	OPERATOR = 0
	UAV = 1
	TARGET = 2


class HUDSelectTarget(HUDBase):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.batch_bg = pg.graphics.Batch()
		self.batch = pg.graphics.Batch()

		# self.bg = pg.shapes.Box(0, 0, self.width, self.height, batch=self.batch)

		icon_operator = Gesture(
			0,
			0,
			GestureType.CONFIRM,
			Config.Colors.positive,
		)
		icon_uav = pg.sprite.Sprite(img_icon_uav, 0, 0, batch=self.batch)
		icon_uav.color = Config.Colors.white
		icon_target = pg.sprite.Sprite(img_icon_target, 0, 0, batch=self.batch)
		icon_target.color = Config.Colors.active
		self.icons = {
			LandmarkType.OPERATOR: icon_operator,
			LandmarkType.UAV: icon_uav,
			LandmarkType.TARGET: icon_target,
		}

		self.obstacles: list[pg.shapes.Line] = []

		def update_obstacles(obstacles):
			add_count = len(obstacles) - len(self.obstacles)
			if add_count > 0:
				for _ in range(add_count):
					self.obstacles.append(
						pg.shapes.Line(
							0, 0, 0, 0, color=Config.Colors.negative, batch=self.batch_bg
						)
					)
			elif add_count < 0:
				for _ in range(-add_count):
					obstacle = self.obstacles.pop()
					obstacle.delete()

		state.subscribe("obstacles", update_obstacles, immediate=True)

	def update(self):
		padding = [self.icons[LandmarkType.OPERATOR].radius, self.icons[LandmarkType.OPERATOR].radius]
		origins = [state.operator_origin, state.uav_origin, state.target_origin]
		obstacles = state.obstacles.copy()

		map_up = origins[LandmarkType.UAV.value] - origins[LandmarkType.OPERATOR.value]
		map_angle = atan2(map_up.x, map_up.z)

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

		scale_x = (self.width - padding[0] * 2) / delta.x if delta.x != 0 else float("inf")
		scale_z = (self.height - padding[1] * 2) / delta.z if delta.z != 0 else float("inf")
		scale = min(scale_x, scale_z)
		if scale == float("inf"):
			scale = 1.0

		map_origin = pg.math.Vec3(self.width / 2, 0, self.height / 2)

		def world_to_map(pos: pg.math.Vec3):
			pos_centered = pos - center
			pos_exact = pos_centered * scale + map_origin
			return pg.math.Vec3(round(pos_exact.x), round(pos_exact.y), round(pos_exact.z))

		for type, icon in self.icons.items():
			map_pos = world_to_map(origins[type.value])
			icon.position = (map_pos.x, map_pos.z, 0)

		for i, obstacle in enumerate(obstacles):
			map_pos_start = world_to_map(rotate_pos_xz(obstacle[0], map_angle))
			map_pos_end = world_to_map(rotate_pos_xz(obstacle[1], map_angle))
			self.obstacles[i].x = map_pos_start.x
			self.obstacles[i].y = map_pos_start.z
			self.obstacles[i].x2 = map_pos_end.x
			self.obstacles[i].y2 = map_pos_end.z

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)

		self.update()
		self.batch_bg.draw()
		self.batch.draw()
		self.icons[LandmarkType.OPERATOR].draw()

		self.buf.unbind()
