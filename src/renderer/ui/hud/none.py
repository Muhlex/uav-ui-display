from .base import HUDBase


class HUDNone(HUDBase):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)

	def render(self):
		pass
