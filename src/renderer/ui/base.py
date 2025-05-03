from ..dynamic_texture import DynamicTexture


class UIBase(DynamicTexture):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.visible = True
		self.yaw = 0.0
		self.y_frac = 0.5
