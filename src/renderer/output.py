from math import pi

import pyglet as pg
from pyglet import gl

from data import Data
from .hud import Hud


class Output:
	def __init__(self, data: Data, w: int, h: int, scale: int):
		self.data = data
		self.w = w
		self.h = h
		self.scale = scale

		self.overdraw_horz = w // 2
		self.overdraw_w = w + self.overdraw_horz * 2

		self.overdraw_tex = pg.image.Texture.create(
			self.overdraw_w, h, min_filter=gl.GL_NEAREST, mag_filter=gl.GL_NEAREST
		)
		self.overdraw_buf = pg.image.Framebuffer()  # type: ignore
		self.overdraw_buf.attach_texture(self.overdraw_tex, attachment=gl.GL_COLOR_ATTACHMENT0)

		self.tex = pg.image.Texture.create(w, h, min_filter=gl.GL_NEAREST, mag_filter=gl.GL_NEAREST)
		self.buf = pg.image.Framebuffer()  # type: ignore
		self.buf.attach_texture(self.tex, attachment=gl.GL_COLOR_ATTACHMENT0)

		self.win = pg.window.Window(width=w * scale, height=h * scale, caption=type(self).__name__)
		self.win.push_handlers(self.on_draw)

		self.fps = pg.window.FPSDisplay(window=self.win)

		self.hud = Hud(self.w // 3, self.h)

	def yawToX(self, yaw: float):
		return self.overdraw_horz + self.w // 2 + yaw / (2 * pi) * self.w

	def draw(self):
		self.hud.draw()

		self.overdraw_buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		x = -self.hud.tex.width // 2
		if self.data.has_operator:
			x += int(self.yawToX(self.data.operator_yaw))
		else:
			x += int(self.yawToX(self.data.scroll_yaw))
		self.hud.tex.blit(x, 0)
		if not self.data.has_operator:
			self.hud.tex.blit(x + self.hud.tex.width, 0)
			self.hud.tex.blit(x - self.hud.tex.width, 0)
		self.overdraw_buf.unbind()

	def wrap(self):
		self.buf.bind()
		self.overdraw_tex.blit(-self.overdraw_horz, 0)

		gl.glEnable(gl.GL_BLEND)
		gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
		# TODO: This should be possible without getting the image data again,
		# but pyglet doesn't implement it currently (potentially do it manually).
		regionLeft = self.overdraw_tex.get_region(0, 0, self.overdraw_horz, self.h).get_image_data()
		regionLeft.blit(self.w - self.overdraw_horz, 0)
		regionRight = self.overdraw_tex.get_region(
			self.overdraw_w - self.overdraw_horz, 0, self.overdraw_horz, self.h
		).get_image_data()
		regionRight.blit(0, 0)
		gl.glDisable(gl.GL_BLEND)

		self.buf.unbind()

	def on_draw(self):
		self.draw()
		self.wrap()

		self.win.clear()
		self.tex.blit(0, 0, width=self.win.width, height=self.win.height)
		self.fps.draw()
