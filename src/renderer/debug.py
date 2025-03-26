from math import degrees

import pyglet as pg

from config import Config
from state import state, UAVState


class Debug:
	def __init__(
		self,
		x: int,
		y: int,
		width: int = 512,
		height: int = 512,
		batch: pg.graphics.Batch | None = None,
	):
		self.batch = batch or pg.graphics.Batch()

		doc = pg.text.decode_text("")
		doc_style = {
			"font_name": Config.Fonts.debug.name,
			"font_size": 12,
			"color": (150, 255, 150, 255),
		}
		doc.set_style(0, 0, doc_style)
		self.rect = pg.shapes.Rectangle(
			x, y, width, height, color=(0, 35, 0, 255), batch=self.batch
		)
		self.layout = pg.text.layout.IncrementalTextLayout(
			doc,
			x + 8,
			y + 8,
			width=width - 8 * 2,
			height=height - 8 * 2,
			multiline=True,
			wrap_lines=True,
			batch=self.batch,
		)

		self.update(0.0)
		pg.clock.schedule_interval(self.update, 1 / 60)

	def draw(self):
		self.batch.draw()

	def update(self, dt: float):
		self.layout.document.text = f"""\
UAV state: {state.uav_state}
Has operator? {state.has_operator}
Has target? {state.has_target}

UAV origin: {state.uav_origin}
Target origin: {state.target_origin}
Operator origin: {state.operator_origin}
Yaw towards operator: {degrees(state.operator_dir_yaw):.2f}
Pitch towards operator: {degrees(state.operator_dir_pitch):.2f}

Battery level: {state.battery_frac:.2f}
"""

	def on_key_press(self, symbol: int, modifiers: int):
		match symbol:
			case pg.window.key.S:
				state.uav_state = UAVState((state.uav_state.value + 1) % len(UAVState))
			case pg.window.key.O:
				state.has_operator = not state.has_operator
			case pg.window.key.T:
				state.has_target = not state.has_target
			case pg.window.key.B:
				new_battery_frac = state.battery_frac - 0.1
				if new_battery_frac <= 0.0:
					new_battery_frac = 1.0
				state.battery_frac = new_battery_frac
