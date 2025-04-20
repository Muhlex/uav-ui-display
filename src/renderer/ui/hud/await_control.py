import pyglet as pg
import pyglet.gl as gl

from config import Config
from .base import HUDBase

from assets.images.icon.wave import wave
from components.battery import BatterySmall


class HUDAwaitControl(HUDBase):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.batch = pg.graphics.Batch()

		self.icon_wave = pg.sprite.Sprite(
			wave,
			width // 2 - wave.get_max_width() // 2,
			height - wave.get_max_height(),
			batch=self.batch,
		)
		self.icon_wave.color = Config.Colors.positive

		self.battery = BatterySmall(width // 2 - BatterySmall.width // 2, 2, batch=self.batch)

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.buf.unbind()
