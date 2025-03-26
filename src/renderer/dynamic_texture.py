from abc import ABC, abstractmethod

from pgext import ColorFramebuffer


class DynamicTexture(ABC):
	def __init__(self, width: int, height: int):
		self.buf = ColorFramebuffer(width, height)

	@property
	def texture(self):
		return self.buf.texture

	@property
	def width(self):
		return self.buf.texture.width

	@property
	def height(self):
		return self.buf.texture.height

	@abstractmethod
	def render(self):
		pass
