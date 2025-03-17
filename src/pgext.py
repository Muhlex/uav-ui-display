import pyglet as pg
import pyglet.gl as gl


class ColorFramebuffer(pg.image.buffer.Framebuffer):
	def __init__(
		self,
		width: int,
		height: int,
		target: int = gl.GL_TEXTURE_2D,
		internalformat: int | None = gl.GL_RGBA8,
		min_filter: int | None = None,
		mag_filter: int | None = None,
		fmt: int = gl.GL_RGBA,
		blank_data: bool = True,
	):
		super().__init__()
		self.texture = pg.image.Texture.create(
			width,
			height,
			target=target,
			internalformat=internalformat,
			min_filter=min_filter,
			mag_filter=mag_filter,
			fmt=fmt,
			blank_data=blank_data,
		)
		self.attach_texture(self.texture, attachment=gl.GL_COLOR_ATTACHMENT0)
