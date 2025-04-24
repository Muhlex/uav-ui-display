from math import pi

import pyglet as pg
import pyglet.gl as gl

from state import state, UAVState

from ..base import UIBase

from .base import HUDBase
from .none import HUDNone
from .low_power import HUDLowPower
from .search import HUDSearch
from .approach import HUDApproach
from .await_control import HUDAwaitControl
from .await_command import HUDAwaitCommand
from .cancel_command import HUDCancelCommand
from .select_target import HUDSelectTarget


class HUD(UIBase):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.y_frac = 1.0

		gap = 2
		tile_count = 3
		hud_width = width // tile_count - gap
		huds: dict[UAVState, HUDBase] = {
			UAVState.NONE: HUDNone(hud_width, height),
			UAVState.LOW_POWER: HUDLowPower(hud_width, height),
			UAVState.SEARCH: HUDSearch(hud_width, height),
			UAVState.APPROACH: HUDApproach(hud_width, height),
			UAVState.AWAIT_CONTROL: HUDAwaitControl(hud_width, height),
			UAVState.AWAIT_COMMAND: HUDAwaitCommand(hud_width, height),
			UAVState.CANCEL_COMMAND: HUDCancelCommand(hud_width, height),
			UAVState.SELECT_TARGET: HUDSelectTarget(hud_width, height),
		}
		self.active_hud = huds[UAVState.NONE]

		self.batch = pg.graphics.Batch()
		self.sprites = [
			pg.sprite.Sprite(
				self.active_hud.texture,
				gap * 0.5 + i * (hud_width + gap),
				0,
				batch=self.batch,
			)
			for i in range(tile_count)
		]

		def on_change_uav_state(uav_state: UAVState):
			self.active_hud = huds.get(uav_state, huds[UAVState.NONE])
			for sprite in self.sprites:
				sprite.image = self.active_hud.texture

		state.subscribe("uav_state", on_change_uav_state, immediate=True)

		def on_change_has_operator(has_operator: bool):
			for sprite in self.sprites:
				sprite.visible = not has_operator
			if has_operator:
				self.sprites[len(self.sprites) // 2].visible = True

		state.subscribe("has_operator", on_change_has_operator, immediate=True)

		pg.clock.schedule_interval(self.tick, 1 / 120)

	def tick(self, dt: float):
		yawspeed = self.active_hud.yawspeed
		if yawspeed != 0.0:
			unclamped_yaw = self.yaw + yawspeed * dt
			self.yaw = (unclamped_yaw + pi) % (2 * pi) - pi
		elif state.has_operator:
			self.yaw = state.operator_dir_yaw

	def render(self):
		if self.active_hud is None:
			self.buf.bind()
			gl.glClear(gl.GL_COLOR_BUFFER_BIT)
			self.buf.unbind()
			return

		self.active_hud.render()

		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		self.batch.draw()
		self.buf.unbind()
