from math import degrees

import pyglet as pg

from config import Config
from data import Data


class Debug:
	def __init__(self, data: Data):
		self.data = data

		self.win = pg.window.Window(width=1024, height=512, caption=type(self).__name__)
		self.win.push_handlers(self.on_draw)

		self.batch = pg.graphics.Batch()

		doc = pg.text.decode_text("")
		doc_style = {
			"font_name": Config.Fonts.debug.name,
			"font_size": 14,
			"color": (127, 255, 127, 255),
		}
		doc.set_style(0, 0, doc_style)
		self.layout = pg.text.layout.IncrementalTextLayout(
			doc,
			8,
			8,
			width=self.win.width - 16,
			height=self.win.height - 16,
			multiline=True,
			wrap_lines=True,
			batch=self.batch,
		)

		self.update(0.0)
		pg.clock.schedule_interval(self.update, 0.2)

	def update(self, dt: float):
		self.layout.document.text = f"""\
UAV state: {self.data.uav_state}
UAV origin: {self.data.uav_origin}
Target origin: {self.data.target_origin}
Operator origin: {self.data.operator_origin}
Yaw towards operator: {degrees(self.data.operator_yaw):.2f}

Scrolling yaw: {degrees(self.data.scroll_yaw):.2f}
"""

	def on_draw(self):
		self.win.clear()
		self.batch.draw()
