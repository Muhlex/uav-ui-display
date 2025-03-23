from math import pi

import pyglet as pg
import pyglet.gl as gl
from pgext import ColorFramebuffer

from ue.send import UESender

from .ui.base import UIBase
from .ui.hud import HUD


class Output:
	def __init__(self, w: int, h: int, scale: int):
		self.sent_frame = False
		self.w = w
		self.h = h
		self.scale = scale

		self.win = pg.window.Window(width=w * scale, height=h * scale, caption=type(self).__name__)
		self.win.push_handlers(self.on_draw)

		self.overdraw_horz = w // 2
		self.overdraw_w = w + self.overdraw_horz * 2

		self.overdraw_buf = ColorFramebuffer(self.overdraw_w, h)
		self.buf = ColorFramebuffer(w, h)
		self.sender = UESender("LED Matrix")

		self.fps = pg.window.FPSDisplay(window=self.win)

		self.uis: list[UIBase] = [HUD(self.w, self.h)]

	def yaw_to_x(self, yaw: float):
		return self.overdraw_horz + self.w // 2 - yaw / (2 * pi) * self.w

	def pitch_to_y(self, pitch: float):
		return self.h // 2  # TODO

	def draw_uis(self):
		self.overdraw_buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.overdraw_buf.unbind()

		for ui in self.uis:
			ui.render()
			tex = ui.texture
			x = int(self.yaw_to_x(ui.yaw)) - tex.width // 2
			y = self.h // 2 if ui.pitch is None else int(self.pitch_to_y(ui.pitch))
			y_frac = y / self.h
			y -= int(tex.height * y_frac)

			self.overdraw_buf.bind()
			tex.blit(x, y)
			self.overdraw_buf.unbind()

	def draw_wrap(self):
		self.buf.bind()
		self.overdraw_buf.texture.blit(-self.overdraw_horz, 0)

		gl.glEnable(gl.GL_BLEND)
		gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
		regionLeft = self.overdraw_buf.texture.get_region(0, 0, self.overdraw_horz, self.h)
		regionLeft.blit(self.w - self.overdraw_horz, 0)
		regionRight = self.overdraw_buf.texture.get_region(
			self.overdraw_w - self.overdraw_horz, 0, self.overdraw_horz, self.h
		)
		regionRight.blit(0, 0)
		gl.glDisable(gl.GL_BLEND)

		self.buf.unbind()

	def on_draw(self):
		self.draw_uis()
		self.draw_wrap()

		self.buf.texture.blit(0, 0, width=self.win.width, height=self.win.height)
		self.fps.draw()

		self.sender.update_texture(self.buf.texture)
