from math import pi

import pyglet.gl as gl

from .dynamic_texture import DynamicTexture
from .ui.base import UIBase
from .ui.hud import HUD
from .ui.indicator import Indicator


class OverdrawMatrix(DynamicTexture):
	def __init__(self, matrix_width: int, matrix_height: int, overdraw_horz: int):
		super().__init__(matrix_width + overdraw_horz * 2, matrix_height)
		self.matrix_width = matrix_width
		self.overdraw_horz = overdraw_horz

		self.uis: list[UIBase] = [HUD(matrix_width, matrix_height - 8), Indicator(matrix_width, 8)]

	def yaw_to_x(self, yaw: float):
		return self.overdraw_horz + self.matrix_width // 2 - yaw / (2 * pi) * self.matrix_width

	def y_frac_to_y(self, y_frac: float):
		return int(y_frac * self.height)

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.buf.unbind()

		for ui in self.uis:
			ui.render()
			tex = ui.texture
			x = int(self.yaw_to_x(ui.yaw)) - tex.width // 2
			y = self.y_frac_to_y(ui.y_frac)
			y_frac = y / self.height
			y -= int(tex.height * y_frac)

			self.buf.bind()
			gl.glEnable(gl.GL_BLEND)
			gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
			tex.blit(x, y)
			gl.glDisable(gl.GL_BLEND)
			self.buf.unbind()
