from abc import ABC, abstractmethod

import pyglet as pg


class UIBase(ABC): # TODO: Inherit from DynamicTexture?
	def __init__(self):
		self.yaw = 0.0
		self.y_frac = 0.5

	@property
	@abstractmethod
	def texture(self) -> pg.image.Texture:
		pass

	@abstractmethod
	def render(self):
		pass
