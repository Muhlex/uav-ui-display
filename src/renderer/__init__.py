import pyglet as pg

from ue.send import UESender

from .matrix import Matrix
from .debug import Debug


class Renderer(pg.window.Window):
	def __init__(self, matrix_width: int, matrix_height: int, sender: UESender):
		debug_height = 512
		matrix_scale = 3
		width = matrix_width * matrix_scale
		height = 512 + matrix_height * matrix_scale + matrix_height + 8 + 8
		super().__init__(width, height, caption=type(self).__name__)

		self.matrix = Matrix(matrix_width, matrix_height)
		self.batch = pg.graphics.Batch()

		self.background = pg.shapes.Rectangle(
			0, 0, self.width, self.height, color=(30, 30, 30, 255), batch=self.batch
		)

		self.matrix_sprite = pg.sprite.Sprite(
			self.matrix.texture, 0, debug_height + 8, batch=self.batch, blend_dest=pg.gl.GL_ZERO,
		)
		self.matrix_sprite.scale = matrix_scale

		self.overdraw_matrix_sprite = pg.sprite.Sprite(
			self.matrix.overdraw.texture,
			0,
			debug_height + self.matrix_sprite.height + 8 + 8,
			blend_dest=pg.gl.GL_ZERO,
			batch=self.batch,
		)

		self.sender = sender

		self.debug = Debug(0, 0, width, debug_height, batch=self.batch)
		self.fps = pg.window.FPSDisplay(self, samples=60)

	def on_key_press(self, symbol: int, modifiers: int):
		match symbol:
			case pg.window.key.ESCAPE:
				self.close()
				return
			case pg.window.key.F12:
				self.matrix.texture.save("screenshot.png")
		self.debug.on_key_press(symbol, modifiers)

	def on_draw(self):
		self.matrix.render()

		self.clear()
		self.batch.draw()
		self.fps.draw()

		self.sender.update_texture(self.matrix.texture)
