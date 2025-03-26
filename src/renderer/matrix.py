import pyglet.gl as gl

from .dynamic_texture import DynamicTexture
from .overdraw_matrix import OverdrawMatrix

class Matrix(DynamicTexture):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.overdraw_horz = width // 2
		self.overdraw = OverdrawMatrix(width, height, self.overdraw_horz)

	def render(self):
		self.overdraw.render()

		self.buf.bind()
		self.overdraw.texture.blit(-self.overdraw_horz, 0)

		gl.glEnable(gl.GL_BLEND)
		gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
		regionLeft = self.overdraw.texture.get_region(0, 0, self.overdraw_horz, self.height)
		regionLeft.blit(self.width - self.overdraw_horz, 0)
		regionRight = self.overdraw.texture.get_region(
			self.width + self.overdraw_horz, 0, self.overdraw_horz, self.height
		)
		regionRight.blit(0, 0)
		gl.glDisable(gl.GL_BLEND)

		self.buf.unbind()
