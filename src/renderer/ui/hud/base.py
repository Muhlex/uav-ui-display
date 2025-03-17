from abc import ABC, abstractmethod

import pyglet as pg


class HudBase(ABC):
	@property
	@abstractmethod
	def texture(self) -> pg.image.Texture:
		pass

	@abstractmethod
	def render(self):
		pass
