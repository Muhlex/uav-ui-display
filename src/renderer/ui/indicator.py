import pyglet as pg
import pyglet.gl as gl
from pgext import ColorFramebuffer

from .base import UIBase

from state import state, UAVState


class Indicator(UIBase):
	def __init__(self, w: int, h: int):
		super().__init__()
		self.buf = ColorFramebuffer(w, h)

	@property
	def texture(self):
		return self.buf.texture

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.buf.unbind()
