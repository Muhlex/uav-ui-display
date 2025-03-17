from math import degrees

import pyglet as pg

from config import Config
from state import state


class Debug:
	def __init__(self):
		self.win = pg.window.Window(width=1024, height=512, caption=type(self).__name__)
		self.win.push_handlers(self.on_draw)
		self.win.push_handlers(self.on_key_press)

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
UAV state: {state.uav_state}
UAV has operator? {state.has_operator}
UAV origin: {state.uav_origin}
Target origin: {state.target_origin}
Operator origin: {state.operator_origin}
Yaw towards operator: {degrees(state.operator_dir_yaw):.2f}
Battery level: {state.battery_frac:.2f}
"""

	def on_draw(self):
		self.win.clear()
		self.batch.draw()

	def on_key_press(self, symbol: int, modifiers: int):
		match symbol:
			case pg.window.key.O:
				state.has_operator = not state.has_operator
			case pg.window.key.B:
				new_battery_frac = state.battery_frac - 0.1
				if new_battery_frac <= 0.0:
					new_battery_frac = 1.0
				state.battery_frac = new_battery_frac
