import pyglet as pg
import pyglet.gl as gl

from config import Config
from ...dynamic_texture import DynamicTexture

from assets.images.battery import BatterySmall


class HudAwaitCommand(DynamicTexture):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.batch = pg.graphics.Batch()

		self.border = pg.shapes.Box(0, 0, width, height, color=(255, 255, 255), batch=self.batch)
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
		self.battery = BatterySmall(0, 0, batch=self.batch)

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.buf.unbind()
