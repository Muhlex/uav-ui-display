import pyglet as pg
from pyglet import gl


class Matrix:
	def __init__(self, w: int, h: int, scale: int):
		self.w = w
		self.h = h
		self.scale = scale

		self.tex = pg.image.Texture.create(w, h, min_filter=gl.GL_NEAREST, mag_filter=gl.GL_NEAREST)
		self.buf = pg.image.Framebuffer()  # type: ignore (for some reason this is marked as private)
		self.buf.attach_texture(self.tex, attachment=gl.GL_COLOR_ATTACHMENT0)

		self.win = pg.window.Window(width=w * scale, height=h * scale, caption=type(self).__name__)
		self.win.push_handlers(self.on_draw)

		self.fps = pg.window.FPSDisplay(window=self.win)

	def render(self):
		label = pg.text.Label(
			"Hello World",
			font_name="Upheaval TT (BRK)",
			font_size=15,
			x=self.w,
			y=self.h // 2,
			anchor_x="center",
			anchor_y="center",
		)
		label.draw()

	def on_draw(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.render()
		self.buf.unbind()

		self.win.clear()
		self.tex.blit(0, 0, width=self.win.width, height=self.win.height)
		self.fps.draw()
