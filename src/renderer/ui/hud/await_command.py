import pyglet as pg
import pyglet.gl as gl
from pgext import ColorFramebuffer

from config import Config
from .base import HudBase

from assets.images.battery import BatterySmall


class HudAwaitCommand(HudBase):
	def __init__(self, w: int, h: int):
		self.buf = ColorFramebuffer(w, h)
		self.batch = pg.graphics.Batch()

		self.border = pg.shapes.Box(
			0, 0, w, h, color=(255, 255, 255, 100), batch=self.batch
		)
		self.title = pg.text.Label(
			"Ready",
			font_name=Config.Fonts.display.name,
			font_size=Config.Fonts.display_size,
			color=(150, 255, 150, 255),
			x=w // 2,
			y=h - 2,
			anchor_x="center",
			anchor_y="top",
			batch=self.batch,
		)
		self.battery = BatterySmall(0, 0, batch=self.batch)

	@property
	def texture(self):
		return self.buf.texture

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.buf.unbind()
