import pyglet as pg
import pyglet.gl as gl

from config import Config
from ...dynamic_texture import DynamicTexture

from components.battery import BatterySmall

from assets.images.person.wave import wave as icon_wave

icon_point = pg.resource.image("assets/images/person/point.png")
icon_cancel = pg.resource.image("assets/images/person/cancel.png")


class HUDAwaitControl(DynamicTexture):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.batch = pg.graphics.Batch()

		self.title = pg.text.Label(
			"Ready for command:",
			font_name=Config.Fonts.display.name,
			font_size=Config.Fonts.display_size,
			color=Config.Colors.idle,
			x=width // 2,
			y=height - 2,
			anchor_x="center",
			anchor_y="top",
			batch=self.batch,
		)

		self.point_label = pg.text.Label(
			"Point to deliver",
			font_name=Config.Fonts.display.name,
			font_size=Config.Fonts.display_size,
			color=Config.Colors.white,
			x=width // 4,
			y=self.title.y - self.title.font_size - Config.Fonts.display_size / 2 - 16,
			anchor_x="left",
			anchor_y="center",
			batch=self.batch,
		)
		self.point_icon = pg.sprite.Sprite(
			icon_point,
			x=self.point_label.x - 4 - icon_point.width,
			y=self.point_label.y - icon_point.height // 2,
			batch=self.batch,
		)

		self.cancel_label = pg.text.Label(
			"Abort control",
			font_name=Config.Fonts.display.name,
			font_size=Config.Fonts.display_size,
			color=Config.Colors.abort,
			x=self.point_label.x,
			y=self.point_label.y - self.point_label.font_size - 8,
			anchor_x="left",
			anchor_y="center",
			batch=self.batch,
		)
		self.cancel_icon = pg.sprite.Sprite(
			icon_cancel,
			x=self.cancel_label.x - 4 - icon_point.width,
			y=self.cancel_label.y - icon_point.height // 2,
			batch=self.batch,
		)
		self.cancel_icon.color = Config.Colors.abort

		self.battery = BatterySmall(width // 2 - BatterySmall.width // 2, 0, batch=self.batch)

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.buf.unbind()
