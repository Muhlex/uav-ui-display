import pyglet as pg


class Radar:
	def __init__(self, w: int, h: int):
		self.win = pg.window.Window(width=w, height=h, caption=type(self).__name__)
		self.win.push_handlers(self.on_draw)

	def on_draw(self):
		self.win.clear()
		label = pg.text.Label(
			"Radar goes here",
			font_name="JetBrains Mono",
			# weight=pg.text.Weight.BOLD,
			font_size=16,
			x=self.win.width // 2,
			y=self.win.height // 2,
			anchor_x="center",
			anchor_y="center",
		)
		label.draw()
