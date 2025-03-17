from .output import Output
from .debug import Debug


class Renderer:
	def __init__(self):
		self.debug = Debug()
		self.output = Output(480, 96, 4)
