from data import Data

from .output import Output
from .debug import Debug


class Renderer:
	def __init__(self, data: Data):
		self.debug = Debug(data)
		self.output = Output(data, 480, 96, 4)
