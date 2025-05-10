from math import radians

import pyglet as pg

from util import rotate_around, map_range, ease_in_cubic


class Person:
	def __init__(
		self,
		x: int,
		y: int,
		scale: int = 5,
	):
		"""
		Origin is at the center of the person's feet.
		This class doesn't render to an existing batch because it needs to sometimes overlay everything.
		"""
		self._arm_left_upper_angle = radians(45)
		self._arm_right_upper_angle = radians(-45)
		self._arm_left_fore_angle = radians(90)
		self._arm_right_fore_angle = radians(-90)

		self.batch = pg.graphics.Batch()

		self.circle = pg.shapes.Circle(0, 0, 0, 32, batch=self.batch)

		self.legs = (
			pg.shapes.Line(0, 0, 0, 0, batch=self.batch),
			pg.shapes.Line(0, 0, 0, 0, batch=self.batch),
		)

		self.body = pg.shapes.Line(0, 0, 0, 0, batch=self.batch)

		arm_left_upper = pg.shapes.Line(0, 0, 0, 0, batch=self.batch)
		arm_left_fore = pg.shapes.Line(0, 0, 0, 0, batch=self.batch)
		arm_right_upper = pg.shapes.Line(0, 0, 0, 0, batch=self.batch)
		arm_right_fore = pg.shapes.Line(0, 0, 0, 0, batch=self.batch)
		self.arms = ((arm_left_upper, arm_left_fore), (arm_right_upper, arm_right_fore))

		self.head = pg.shapes.Arc(0, 0, 0, batch=self.batch)

		self._update_vertices(x, y, scale)

	def _update_vertices(self, x: int, y: int, scale: int):
		self.legs[0].x, self.legs[0].y = x - int(scale * 0.8), y
		self.legs[0].x2, self.legs[0].y2 = x, y + int(scale * 1.8)

		self.legs[1].x, self.legs[1].y = x + int(scale * 0.8) - 1, y
		self.legs[1].x2, self.legs[1].y2 = x - 1, y + int(scale * 1.8)

		self.body.x, self.body.y = self.legs[0].x2, self.legs[0].y2
		self.body.x2, self.body.y2 = self.legs[0].x2, self.legs[0].y2 + int(scale * 2.4)

		self.head.radius = scale
		self.head.x, self.head.y = self.body.x2, self.body.y2 + self.head.radius

		# self.circle.position = (x, y + int(scale * 2.8))
		self.circle.position = self.head.position

		self.set_arms_rotations(
			left_upper=self._arm_left_upper_angle,
			left_fore=self._arm_left_fore_angle,
			right_upper=self._arm_right_upper_angle,
			right_fore=self._arm_right_fore_angle,
		)

	@property
	def x(self):
		return int(self.body.x)

	@x.setter
	def x(self, value: int):
		offset = value - self.x

		self.head.x += offset
		self.body.x += offset
		self.body.x2 += offset
		for leg in self.legs:
			leg.x += offset
			leg.x2 += offset
		for arm in self.arms:
			for segment in arm:
				segment.x += offset
				segment.x2 += offset

	@property
	def y(self):
		return int(self.legs[0].y)

	@y.setter
	def y(self, value: int):
		offset = value - self.y

		self.head.y += offset
		self.body.y += offset
		self.body.y2 += offset
		for leg in self.legs:
			leg.y += offset
			leg.y2 += offset
		for arm in self.arms:
			for segment in arm:
				segment.y += offset
				segment.y2 += offset

	@property
	def scale(self):
		return int(self.head.radius)

	@scale.setter
	def scale(self, value: int):
		if value == self.scale:
			return
		self._update_vertices(self.x, self.y, value)

	@property
	def visible(self):
		return self.head.visible

	@visible.setter
	def visible(self, visible: bool):
		self.head.visible = visible
		self.body.visible = visible
		for leg in self.legs:
			leg.visible = visible
		for arm in self.arms:
			for segment in arm:
				segment.visible = visible

	@property
	def color(self):
		return self.head.color

	@color.setter
	def color(self, value: tuple[int, int, int]):
		self.circle.color = value
		self.head.color = value
		self.body.color = value
		for leg in self.legs:
			leg.color = value
		for arm in self.arms:
			for segment in arm:
				segment.color = value

	def set_gesture_progress(self, value: float):
		self.circle.radius = map_range(ease_in_cubic(value), 0.0, 1.0, 0, 128)

	def set_arms_rotations(
		self,
		left_upper: float | None = None,
		left_fore: float | None = None,
		right_upper: float | None = None,
		right_fore: float | None = None,
	):
		arms = self.arms

		def rotate_segment(arm_index: int, segment_index: int, angle: float):
			x2, y2 = rotate_around(
				arms[arm_index][segment_index].x2,
				arms[arm_index][segment_index].y2,
				arms[arm_index][segment_index].x,
				arms[arm_index][segment_index].y,
				angle,
			)
			arms[arm_index][segment_index].x2 = x2
			arms[arm_index][segment_index].y2 = y2
			if segment_index == 0:
				move_x = arms[arm_index][0].x2 - arms[arm_index][1].x
				move_y = arms[arm_index][0].y2 - arms[arm_index][1].y
				arms[arm_index][1].x += move_x
				arms[arm_index][1].y += move_y
				arms[arm_index][1].x2 += move_x
				arms[arm_index][1].y2 += move_y

		origin_y = self.body.y2 - int(self.scale * 0.6)
		origin_x_l = self.body.x2 - 1
		origin_x_r = self.body.x2

		if left_upper is not None:
			arms[0][0].x, arms[0][0].y = origin_x_l, origin_y
			arms[0][0].x2, arms[0][0].y2 = origin_x_l - int(self.scale * 0.8), origin_y
			rotate_segment(0, 0, left_upper)
			self._arm_left_upper_angle = left_upper
		if left_fore is not None:
			arms[0][1].x, arms[0][1].y = arms[0][0].x2, arms[0][0].y2
			arms[0][1].x2, arms[0][1].y2 = arms[0][0].x2 - self.scale, arms[0][0].y2
			rotate_segment(0, 1, left_fore)
			self._arm_left_fore_angle = left_fore
		if right_upper is not None:
			arms[1][0].x, arms[1][0].y = origin_x_r, origin_y
			arms[1][0].x2, arms[1][0].y2 = origin_x_r + int(self.scale * 0.8), origin_y
			rotate_segment(1, 0, right_upper)
			self._arm_right_upper_angle = right_upper
		if right_fore is not None:
			arms[1][1].x, arms[1][1].y = arms[1][0].x2, arms[1][0].y2
			arms[1][1].x2, arms[1][1].y2 = arms[1][0].x2 + self.scale, arms[1][0].y2
			rotate_segment(1, 1, right_fore)
			self._arm_right_fore_angle = right_fore

	def delete(self):
		for leg in self.legs:
			leg.delete()
		self.body.delete()
		for [arm_upper, arm_fore] in self.arms:
			arm_upper.delete()
			arm_fore.delete()
		self.head.delete()

	def draw(self):
		self.batch.draw()
