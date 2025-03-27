from ...dynamic_texture import DynamicTexture


class HUDNone(DynamicTexture):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)

	def render(self):
		pass
