import pyglet as pg
import pyglet.gl as gl

from config import Config
from ...dynamic_texture import DynamicTexture

from components.battery import BatterySmall

from assets.images.person.wave import wave as icon_wave

icon_point = pg.resource.image("assets/images/person/point.png")
icon_cancel = pg.resource.image("assets/images/person/cancel.png")


class HUDApproach(DynamicTexture):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.batch = pg.graphics.Batch()

		self.title = pg.text.Label(
			"~~APPROACH~~",
			font_name=Config.Fonts.display.name,
			font_size=Config.Fonts.display_size,
			color=Config.Colors.idle,
			x=width // 2,
			y=height - 2,
			anchor_x="center",
			anchor_y="top",
			batch=self.batch,
		)

		self.battery = BatterySmall(width // 2 - BatterySmall.width // 2, 0, batch=self.batch)

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.buf.unbind()
