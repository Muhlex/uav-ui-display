from abc import ABC, abstractmethod
import pyglet as pg

class HudBase(ABC):
	@abstractmethod
	def activate(self, tex: pg.image.Texture):
		pass

	@abstractmethod
	def draw(self, tex: pg.image.Texture):
		pass
