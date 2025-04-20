from ...dynamic_texture import DynamicTexture


class HUDBase(DynamicTexture):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.yawspeed = 0.0
