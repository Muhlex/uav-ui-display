from itertools import chain

import pyglet as pg

from util import map_range, ease_in_cubic

from state import state, GestureType

from assets.images.gesture.person.point import point

# Of course pyglet's primitives never render uneven diameter circles, so use images:
img_outline = pg.resource.image("assets/images/gesture/outline.png")
img_fill = pg.resource.image("assets/images/gesture/fill.png")
icons = {
	GestureType.ABORT: pg.resource.image("assets/images/gesture/person/abort.png"),
	GestureType.CONFIRM: pg.resource.image("assets/images/gesture/person/confirm.png"),
	GestureType.POINT: point,
}

img_outline_large = pg.resource.image("assets/images/gesture/outline_large.png")
img_fill_large = pg.resource.image("assets/images/gesture/fill_large.png")
icons_large = {
	GestureType.ABORT: pg.resource.image("assets/images/gesture/person/abort_large.png"),
	GestureType.CONFIRM: pg.resource.image("assets/images/gesture/person/confirm_large.png"),
}

for img in chain(
	icons.values(),
	icons_large.values(),
	[img_outline, img_fill, img_outline_large, img_fill_large],
):
	if not isinstance(img, (pg.image.Texture, pg.image.TextureRegion)):
		continue
	img.anchor_x = img.width // 2
	img.anchor_y = img.height // 2


class Gesture:
	"""
	This class doesn't render to an existing batch because it needs to sometimes overlay everything.
	"""

	def __init__(
		self,
		x: float,
		y: float,
		type: GestureType,
		color: tuple[int, int, int],
	):
		self._type = type
		self.active = False

		self.batch = pg.graphics.Batch()

		self.expander = pg.shapes.Circle(x, y, 0, 32, color=color, batch=self.batch)
		self.expander.visible = False
		self.outline = pg.sprite.Sprite(img_outline, x, y, batch=self.batch)
		self.outline.color = color
		self.fill = pg.sprite.Sprite(img_fill, x, y, batch=self.batch)
		self.fill.color = color
		self.fill.visible = False

		self.icons = icons
		self.icon = pg.sprite.Sprite(self.icons[type], x, y, batch=self.batch)
		self.icon.color = color

		state.subscribe("operator_gesture_type", self.on_change_gesture_type, immediate=True)
		state.subscribe("operator_gesture_progress", self.on_change_gesture_progress)

	def on_change_gesture_type(self, value: GestureType):
		self.active = value == self._type
		if self.active:
			self.icon.color = (0, 0, 0)
			self.fill.visible = True
			self.expander.visible = True
			self.on_change_gesture_progress(state.operator_gesture_progress)
		else:
			self.icon.color = self.outline.color
			self.fill.visible = False
			self.expander.visible = False

	def on_change_gesture_progress(self, value: float):
		if not self.expander.visible:
			return
		self.expander.radius = map_range(ease_in_cubic(value), 0.0, 1.0, self.radius - 1, 128)

	@property
	def x(self):
		return self.outline.x

	@property
	def y(self):
		return self.outline.y

	@property
	def position(self):
		return self.outline.position

	@position.setter
	def position(self, pos: tuple[int, int, int]):
		self.outline.position = pos
		self.fill.position = pos
		self.expander.position = (pos[0], pos[1])
		self.icon.position = pos

	@property
	def radius(self):
		return self.outline.width / 2

	@property
	def visible(self):
		return self.outline.visible

	@visible.setter
	def visible(self, visible: bool):
		self.outline.visible = visible
		self.icon.visible = visible
		if self.active:
			self.fill.visible = visible
			self.expander.visible = visible

	@property
	def color(self):
		return self.outline.color

	@color.setter
	def color(self, color: tuple[int, int, int]):
		self.outline.color = color
		self.fill.color = color
		self.expander.color = color
		if not self.active:
			self.icon.color = color

	@property
	def type(self):
		return self._type

	@type.setter
	def type(self, type: GestureType):
		self._type = type
		self.icon.image = self.icons[type]
		self.on_change_gesture_type(state.operator_gesture_type)

	def draw(self):
		self.batch.draw()


class GestureLarge(Gesture):
	def __init__(
		self,
		x: float,
		y: float,
		type: GestureType,
		color: tuple[int, int, int],
	):
		super().__init__(x, y, type, color)
		self.icons = icons_large

		self.icon.image = icons_large[type]
		self.outline.image = img_outline_large
		self.fill.image = img_fill_large
