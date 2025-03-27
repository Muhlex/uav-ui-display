import pyglet as pg
import pyglet.gl as gl

from config import Config
from ...dynamic_texture import DynamicTexture

icon_search = pg.resource.image("assets/images/search_large.png")
icon_search.anchor_x = icon_search.width // 2
icon_search.anchor_y = icon_search.height // 2
icon_search_rotator = pg.resource.image("assets/images/search_large_rotator.png")
icon_search_rotator.anchor_x = icon_search_rotator.width // 2
icon_search_rotator.anchor_y = icon_search_rotator.height // 2


class HUDSearch(DynamicTexture):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.batch = pg.graphics.Batch()

		self.icon = pg.sprite.Sprite(
			icon_search,
			width // 2,
			height - icon_search.height // 2 - 8,
			batch=self.batch,
		)

		self.icon_rotator = pg.sprite.Sprite(
			icon_search_rotator,
			self.icon.x,
			self.icon.y,
			batch=self.batch,
		)
		self.icon_rotator.color = Config.Colors.search

		self.title_label = pg.text.Label(
			"Searching...",
			font_name=Config.Fonts.display.name,
			font_size=Config.Fonts.display_size * 2,
			color=Config.Colors.search,
			x=width // 2,
			y=self.icon.y - icon_search.height // 2 - 8,
			anchor_x="center",
			anchor_y="top",
			batch=self.batch,
		)

		pg.clock.schedule_interval(self.tick, 1 / 120)

	def tick(self, dt: float):
		self.icon_rotator.rotation += dt * 45

	def render(self):
		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.buf.unbind()
