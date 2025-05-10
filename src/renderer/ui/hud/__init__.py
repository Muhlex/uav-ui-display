from math import pi

import pyglet as pg
import pyglet.gl as gl

from ...led_matrix_canvas import LEDMatrixCanvas

from state import state, UAVState

from ..base import UIBase

from .base import HUDBase
from .none import HUDNone
from .low_power import HUDLowPower
from .search import HUDSearch
from .await_control import HUDAwaitControl
from .await_command import HUDAwaitCommand
from .select_target import HUDSelectTarget
from .move_to_target import HUDMoveToTarget
from .hover_target import HUDHoverTarget


class HUD(UIBase):
	def __init__(self, canvas: LEDMatrixCanvas):
		super().__init__(canvas.width, canvas.height)
		self.y_frac = 1.0

		safe_padding = 4
		safe_width = canvas.matrix_width // 3 - (safe_padding * 2)

		huds: dict[UAVState, HUDBase] = {
			UAVState.NONE: HUDNone(canvas.matrix_width, canvas.height),
			UAVState.LOW_POWER: HUDLowPower(safe_width, canvas.height),
			UAVState.SEARCH: HUDSearch(canvas.matrix_width // 4, canvas.height),
			UAVState.AWAIT_CONTROL: HUDAwaitControl(safe_width, canvas.height),
			UAVState.AWAIT_COMMAND: HUDAwaitCommand(canvas.matrix_width, canvas.height),
			UAVState.SELECT_TARGET: HUDSelectTarget(canvas.matrix_width, canvas.height, safe_width),
			UAVState.MOVE_TO_TARGET: HUDMoveToTarget(canvas.matrix_width, canvas.height),
			UAVState.HOVER_TARGET: HUDHoverTarget(canvas.matrix_width, canvas.height),
		}
		self.active_hud = huds[UAVState.NONE]

		self.batch = pg.graphics.Batch()

		self.sprites: list[pg.sprite.Sprite] = []

		def on_change_uav_state(uav_state: UAVState):
			self.active_hud = huds.get(uav_state, huds[UAVState.NONE])

			for sprite in self.sprites:
				sprite.delete()
			self.sprites.clear()

			hud_width = self.active_hud.texture.width
			tile_count = canvas.matrix_width // hud_width
			gap = (canvas.matrix_width - tile_count * hud_width) // tile_count

			for i in range(tile_count):
				i_zeroed = i - (tile_count - 1) / 2 # e. g. [-0.5, 0.5] or [-1.0, 0.0, 1.0]
				x = canvas.width // 2 - hud_width // 2 - gap // 2 + i_zeroed * hud_width + (gap * i)
				self.sprites.append(
					pg.sprite.Sprite(self.active_hud.texture, x, 0, batch=self.batch)
				)

		state.subscribe("uav_state", on_change_uav_state, immediate=True)

		pg.clock.schedule_interval(self.tick, 1 / 120)

	def tick(self, dt: float):
		yawspeed = self.active_hud.yawspeed
		if yawspeed != 0.0:
			unclamped_yaw = self.yaw + yawspeed * dt
			self.yaw = (unclamped_yaw + pi) % (2 * pi) - pi
		elif state.has_operator:
			self.yaw = state.operator_dir_yaw

	def render(self):
		self.active_hud.render()

		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.buf.unbind()
