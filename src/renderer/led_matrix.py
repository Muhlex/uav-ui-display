import pyglet.gl as gl

from .dynamic_texture import DynamicTexture
from .led_matrix_canvas import LEDMatrixCanvas

class LEDMatrix(DynamicTexture):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.overdraw_horz = width // 2
		self.canvas = LEDMatrixCanvas(width, height, self.overdraw_horz)

	def render(self):
		self.canvas.render()

		self.buf.bind()
		self.canvas.texture.blit(-self.overdraw_horz, 0)

		gl.glEnable(gl.GL_BLEND)
		gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
		regionLeft = self.canvas.texture.get_region(0, 0, self.overdraw_horz, self.height)
		regionLeft.blit(self.width - self.overdraw_horz, 0)
		regionRight = self.canvas.texture.get_region(
			self.width + self.overdraw_horz, 0, self.overdraw_horz, self.height
		)
		regionRight.blit(0, 0)
		gl.glDisable(gl.GL_BLEND)

		self.buf.unbind()
