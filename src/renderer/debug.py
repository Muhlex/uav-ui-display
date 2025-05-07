from math import degrees

import pyglet as pg

from util import map_range
from config import Config
from state import state, UAVState, GestureType

img_slider_track = pg.resource.image("assets/images/gui/slider_track.png")
img_slider_knob = pg.resource.image("assets/images/gui/slider_knob.png")


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
		self.bg = pg.shapes.Rectangle(x, y, width, height, color=(0, 35, 0, 255), batch=self.batch)
		self.layout = pg.text.layout.IncrementalTextLayout(
			doc,
			x + 8,
			y + 8,
			width=width // 2 - 8 * 2,
			height=height - 8 * 2,
			multiline=True,
			wrap_lines=True,
			batch=self.batch,
		)

		self.labels: list[pg.text.Label] = []
		self.widgets: list[pg.gui.WidgetBase] = []

		def create_slider(text: str, value: float, on_change, min=0.0, max=1.0):
			x = width // 2
			y = self.widgets[-1].y - 12 if self.widgets else int(self.layout.y + self.layout.height)
			label = pg.text.Label(
				text,
				font_name=Config.Fonts.debug.name,
				font_size=9,
				x=x,
				y=y,
				anchor_y="top",
				batch=self.batch,
			)
			slider = pg.gui.Slider(
				x,
				int(y - img_slider_track.height - label.font_size - 8),
				img_slider_track,
				img_slider_knob,
				batch=self.batch,
			)

			def set_value(value: float):
				slider.value = map_range(value, min, max, 0.0, 100.0)

			def on_change_handler(_, value: float):
				on_change(map_range(value, 0.0, 100.0, min, max))

			set_value(value)
			slider.set_handler("on_change", on_change_handler)
			self.labels.append(label)
			self.widgets.append(slider)

			return set_value

		# BATTERY
		def on_change_battery_frac(value: float):
			state.battery_frac = value

		set_battery_frac = create_slider(
			"Battery level",
			state.battery_frac,
			on_change_battery_frac,
		)
		state.subscribe("battery_frac", lambda v: set_battery_frac(v))

		# GESTURE PROGRESS
		def on_change_operator_gesture_progress(value: float):
			state.operator_gesture_progress = value

		set_operator_gesture_progress = create_slider(
			"Operator gesture progress",
			state.operator_gesture_progress,
			on_change_operator_gesture_progress,
		)
		state.subscribe("operator_gesture_progress", lambda v: set_operator_gesture_progress(v))

		# OPERATOR ORIGIN
		def on_change_operator_origin_x(value: float):
			vec = pg.math.Vec3(value, state.operator_origin.y, state.operator_origin.z)
			state.operator_origin = vec

		set_operator_origin_x = create_slider(
			"Operator origin X",
			state.operator_origin.x,
			on_change_operator_origin_x,
			min=-1024.0,
			max=1024.0,
		)
		state.subscribe("operator_origin", lambda v: set_operator_origin_x(v.x))

		def on_change_operator_origin_z(value: float):
			vec = pg.math.Vec3(state.operator_origin.x, state.operator_origin.y, value)
			state.operator_origin = vec

		set_operator_origin_z = create_slider(
			"Operator origin Z",
			state.operator_origin.z,
			on_change_operator_origin_z,
			min=-1024.0,
			max=1024.0,
		)
		state.subscribe("operator_origin", lambda v: set_operator_origin_z(v.z))

		# UAV ORIGIN
		def on_change_uav_origin_x(value: float):
			vec = pg.math.Vec3(value, state.uav_origin.y, state.uav_origin.z)
			state.uav_origin = vec

		set_uav_origin_x = create_slider(
			"UAV origin X",
			state.uav_origin.x,
			on_change_uav_origin_x,
			min=-1024.0,
			max=1024.0,
		)
		state.subscribe("uav_origin", lambda v: set_uav_origin_x(v.x))

		def on_change_uav_origin_z(value: float):
			vec = pg.math.Vec3(state.uav_origin.x, state.uav_origin.y, value)
			state.uav_origin = vec

		set_uav_origin_z = create_slider(
			"UAV origin Z",
			state.uav_origin.z,
			on_change_uav_origin_z,
			min=-1024.0,
			max=1024.0,
		)
		state.subscribe("uav_origin", lambda v: set_uav_origin_z(v.z))

		# TARGET ORIGIN
		def on_change_target_origin_x(value: float):
			vec = pg.math.Vec3(value, state.target_origin.y, state.target_origin.z)
			state.target_origin = vec

		set_target_origin_x = create_slider(
			"Target origin X",
			state.target_origin.x,
			on_change_target_origin_x,
			min=-1024.0,
			max=1024.0,
		)
		state.subscribe("target_origin", lambda v: set_target_origin_x(v.x))

		def on_change_target_origin_z(value: float):
			vec = pg.math.Vec3(state.target_origin.x, state.target_origin.y, value)
			state.target_origin = vec

		set_target_origin_z = create_slider(
			"Target origin Z",
			state.target_origin.z,
			on_change_target_origin_z,
			min=-1024.0,
			max=1024.0,
		)
		state.subscribe("target_origin", lambda v: set_target_origin_z(v.z))

		self.update(0.0)
		pg.clock.schedule_interval(self.update, 1 / 30)

	def draw(self):
		self.batch.draw()

	def update(self, dt: float):
		self.layout.document.text = f"""\
UAV state: {state.uav_state}
Has operator? {state.has_operator}
Has target? {state.has_target}

Operator origin: {state.operator_origin}
UAV origin: {state.uav_origin}
Target origin: {state.target_origin}
Yaw towards operator: {degrees(state.operator_dir_yaw):.2f}
Pitch towards operator: {degrees(state.operator_dir_pitch):.2f}

Operator gesture: {state.operator_gesture_type}
Operator gesture progress: {state.operator_gesture_progress:.2f}

Bystander count: {len(state.bystander_origins)}
Yaws towards bystanders: {[round(degrees(yaw), 2) for yaw in state.bystander_dir_yaws]}
Selected bystander: {state.bystander_selected_index}

Battery level: {state.battery_frac:.2f}
"""

	def on_key_press(self, symbol: int, modifiers: int):
		match symbol:
			case pg.window.key.S:
				state.uav_state = UAVState((state.uav_state.value + 1) % len(UAVState))
			case pg.window.key.G:
				state.operator_gesture_type = GestureType(
					(state.operator_gesture_type.value + 1) % len(GestureType)
				)
			case pg.window.key.O:
				state.has_operator = not state.has_operator
			case pg.window.key.T:
				state.has_target = not state.has_target
			case pg.window.key.I:
				bystander_count = len(state.bystander_origins)
				current = state.bystander_selected_index
				state.bystander_selected_index = (current + 2) % (bystander_count + 1) - 1
			case pg.window.key.B:
				new_battery_frac = state.battery_frac - 0.1
				if new_battery_frac <= 0.0:
					new_battery_frac = 1.0
				state.battery_frac = new_battery_frac
