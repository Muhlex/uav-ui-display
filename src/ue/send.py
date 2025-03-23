import atexit

from pyglet.image import Texture
import pyglet.gl as gl
from SpoutGL import SpoutSender  # type: ignore


class UESender:
	def __init__(self, spout_sender_name: str):
		self.sender = SpoutSender()
		self.name = spout_sender_name
		self.sender.setSenderName(spout_sender_name)
		atexit.register(self.sender.releaseSender)

	def update_texture(self, texture: Texture):
		self.sender.sendTexture(
			texture.id, gl.GL_TEXTURE_2D, texture.width, texture.height, True, 0
		)
		self.sender.setFrameSync(self.name)
