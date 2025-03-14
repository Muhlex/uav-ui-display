import pyglet as pg
from pyglet import gl

from data import UAV_State

from .search import HudSearch


class Hud:
	def __init__(self, w: int, h: int):
		self.state = UAV_State.SEARCH
		self.stateToHuds = {UAV_State.SEARCH: HudSearch()}
		self.tex = pg.image.Texture.create(w, h, min_filter=gl.GL_NEAREST, mag_filter=gl.GL_NEAREST)
		self.buf = pg.image.Framebuffer()  # type: ignore
		self.buf.attach_texture(self.tex, attachment=gl.GL_COLOR_ATTACHMENT0)

	@property
	def stateHud(self):
		return self.stateToHuds[self.state]

	def draw(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.stateHud.draw(self.tex)
		self.buf.unbind()
