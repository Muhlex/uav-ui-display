from data import Data

from .matrix import Matrix
# from .radar import Radar


class Renderer:
	matrix = Matrix(480, 96, 4)
	# radar = Radar(256, 256)

	def __init__(self, data: Data):
		self.data = data
