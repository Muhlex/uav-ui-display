from enum import Enum
from math import atan2, sin, cos

import pyglet as pg
import pyglet.gl as gl

from config import Config
from state import state

from .base import HUDBase

from components.battery import BatterySmall
from components.gesture import Gesture, GestureType

img_icon_uav = pg.resource.image("assets/images/icon/uav.png")
img_icon_uav.anchor_x = img_icon_uav.width // 2
img_icon_uav.anchor_y = img_icon_uav.height // 2
img_icon_target = pg.resource.image("assets/images/icon/target.png")
img_icon_target.anchor_x = img_icon_target.width // 2
img_icon_target.anchor_y = img_icon_target.height
img_icon_target_abort = pg.resource.image("assets/images/icon/target_abort.png")
img_icon_target_abort.anchor_x = img_icon_target_abort.width // 2
img_icon_target_abort.anchor_y = img_icon_target_abort.height


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

		self.battery = BatterySmall(width // 2 - BatterySmall.width // 2, 2, batch=self.batch)

		icon_operator = Gesture(
			0,
			0,
			GestureType.CONFIRM,
			Config.Colors.positive,
		)
		icon_uav = pg.sprite.Sprite(img_icon_uav, 0, 0, batch=self.batch)
		icon_uav.color = Config.Colors.white
		icon_target = pg.sprite.Sprite(img_icon_target, 0, 0, batch=self.batch)
		icon_target.color = Config.Colors.positive
		self.icons = {
			LandmarkType.OPERATOR: icon_operator,
			LandmarkType.UAV: icon_uav,
			LandmarkType.TARGET: icon_target,
		}

		def cycle_gesture(gesture_type: GestureType | None = None):
			if gesture_type is None:
				gesture_type = (
					GestureType.ABORT
					if icon_operator.type == GestureType.CONFIRM
					else GestureType.CONFIRM
				)

			color = {
				GestureType.ABORT: Config.Colors.negative,
				GestureType.CONFIRM: Config.Colors.positive,
			}.get(gesture_type, Config.Colors.white)

			icon_operator.type = gesture_type
			icon_operator.color = color
			icon_target.color = color
			icon_target.image = (
				img_icon_target_abort if gesture_type == GestureType.ABORT else img_icon_target
			)

		def on_cycle_operator_gesture_type(dt: float):
			if icon_operator.type == state.operator_gesture_type:
				return
			cycle_gesture()

		pg.clock.schedule_interval(on_cycle_operator_gesture_type, 1.5)

		def on_change_operator_gesture_type(value: GestureType):
			if value != GestureType.CONFIRM and value != GestureType.ABORT:
				return
			cycle_gesture(value)

		state.subscribe("operator_gesture_type", on_change_operator_gesture_type)

		self.obstacles: list[pg.shapes.Line] = []

		def on_change_obstacles(obstacles: list[tuple[pg.math.Vec3, pg.math.Vec3]]):
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

		state.subscribe("obstacles", on_change_obstacles, immediate=True)

	def update(self):
		max_scale = 0.06
		padding = [
			self.icons[LandmarkType.OPERATOR].radius + 10,
			self.icons[LandmarkType.OPERATOR].radius + 8,
		]

		def world_to_xz(pos: pg.math.Vec3):
			return pg.math.Vec2(pos.x, pos.z)

		origins = [
			world_to_xz(pos)
			for pos in [state.operator_origin, state.uav_origin, state.target_origin]
		]
		obstacles = [(world_to_xz(start), world_to_xz(end)) for start, end in state.obstacles]
		state.obstacles.copy()

		map_up = origins[LandmarkType.UAV.value] - origins[LandmarkType.OPERATOR.value]
		map_angle = atan2(map_up.x, map_up.y)

		def rotate_pos(pos: pg.math.Vec2, angle: float):
			s = sin(angle)
			c = cos(angle)
			return pg.math.Vec2(
				pos.x * c - pos.y * s,
				pos.x * s + pos.y * c,
			)

		origins = [rotate_pos(origin, map_angle) for origin in origins]
		min_x = min(origins, key=lambda origin: origin.x).x
		min_y = min(origins, key=lambda origin: origin.y).y
		max_x = max(origins, key=lambda origin: origin.x).x
		max_y = max(origins, key=lambda origin: origin.y).y
		center = pg.math.Vec2((min_x + max_x) / 2, (min_y + max_y) / 2)
		delta = pg.math.Vec2(max_x - min_x, max_y - min_y)

		scale_x = (self.width - padding[0] * 2) / delta.x if delta.x != 0 else float("inf")
		scale_y = (self.height - padding[1] * 2) / delta.y if delta.y != 0 else float("inf")
		scale = min(scale_x, scale_y, max_scale)
		if scale == float("inf"):
			scale = max_scale

		map_origin = pg.math.Vec2(self.width / 2, self.height / 2)

		def world_to_map(pos: pg.math.Vec2):
			pos_centered = pos - center
			pos_exact = pos_centered * scale + map_origin
			return pg.math.Vec2(round(pos_exact.x), round(pos_exact.y))

		for type, icon in self.icons.items():
			map_pos = world_to_map(origins[type.value])
			icon.position = (map_pos.x, map_pos.y, 0)

		for i, obstacle in enumerate(obstacles):
			map_pos_start = world_to_map(rotate_pos(obstacle[0], map_angle))
			map_pos_end = world_to_map(rotate_pos(obstacle[1], map_angle))
			self.obstacles[i].x = map_pos_start.x
			self.obstacles[i].y = map_pos_start.y
			self.obstacles[i].x2 = map_pos_end.x
			self.obstacles[i].y2 = map_pos_end.y

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)

		self.update()
		self.batch_bg.draw()
		self.batch.draw()
		self.icons[LandmarkType.OPERATOR].draw()

		self.buf.unbind()
