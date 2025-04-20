import pyglet as pg

from util import map_range, ease_in_cubic

from state import state, GestureType

# Of course pyglet's primitives never render uneven diameter circles, so use images:
img_outline = pg.resource.image("assets/images/gesture/outline.png")
img_fill = pg.resource.image("assets/images/gesture/fill.png")
img_outline.anchor_x = img_outline.width // 2
img_outline.anchor_y = img_outline.height // 2
img_fill.anchor_x = img_fill.width // 2
img_fill.anchor_y = img_fill.height // 2

icons = {
	GestureType.ABORT: pg.resource.image("assets/images/gesture/person/abort.png"),
	GestureType.CONFIRM: pg.resource.image("assets/images/gesture/person/confirm.png"),
	GestureType.POINT: pg.resource.image("assets/images/gesture/person/point.png"),
}


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
		self.type = type
		self.active = False

		self.batch = pg.graphics.Batch()

		self.expander = pg.shapes.Circle(x, y, 0, 32, color=color, batch=self.batch)
		self.expander.visible = False
		self.outline = pg.sprite.Sprite(img_outline, x, y, batch=self.batch)
		self.outline.color = color
		self.fill = pg.sprite.Sprite(img_fill, x, y, batch=self.batch)
		self.fill.color = color
		self.fill.visible = False

		icon = icons[type]
		self.icon = pg.sprite.Sprite(
			icon, x - icon.width // 2, y - icon.height // 2, batch=self.batch
		)
		self.icon.color = color

		def on_change_operator_gesture_type(value: GestureType):
			self.active = value == self.type
			if self.active:
				self.icon.color = (0, 0, 0)
				self.fill.visible = True
				self.expander.visible = True
				on_change_operator_gesture_progress(state.operator_gesture_progress)
			else:
				self.icon.color = self.outline.color
				self.fill.visible = False
				self.expander.visible = False

		state.subscribe("operator_gesture_type", on_change_operator_gesture_type, immediate=True)

		def on_change_operator_gesture_progress(value: float):
			if not self.expander.visible:
				return
			self.expander.radius = map_range(ease_in_cubic(value), 0.0, 1.0, self.radius - 1, 120)

		state.subscribe("operator_gesture_progress", on_change_operator_gesture_progress)

	@property
	def x(self):
		return self.outline.x

	@property
	def y(self):
		return self.outline.y

	@property
	def radius(self):
		return self.outline.width / 2

	def draw(self):
		self.batch.draw()
