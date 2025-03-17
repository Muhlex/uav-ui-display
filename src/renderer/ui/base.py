from abc import ABC, abstractmethod

import pyglet as pg


class UIBase(ABC):
	def __init__(self):
		self.yaw = 0.0
		self.pitch: float | None = None

	@property
	@abstractmethod
	def texture(self) -> pg.image.Texture:
		pass

	@abstractmethod
	def render(self):
		pass
