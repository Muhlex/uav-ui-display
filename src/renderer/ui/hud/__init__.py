from math import pi

import pyglet as pg
import pyglet.gl as gl
from pgext import ColorFramebuffer

from state import state, UAVState

from ..base import UIBase
from .base import HudBase
from .search import HUDSearch
from .low_power import HUDLowPower
from .await_command import HudAwaitCommand


class HUD(UIBase):
	def __init__(self, w: int, h: int):
		super().__init__()
		self.y_frac = 1.0
		self.scroll_yawspeed = 0.08
		self.tile_count = 3

		hud_w = w // self.tile_count
		self.state_to_huds: dict[UAVState, HudBase] = {
			UAVState.SEARCH: HUDSearch(hud_w, h),
			UAVState.LOW_POWER: HUDLowPower(hud_w, h),
			UAVState.AWAIT_COMMAND: HudAwaitCommand(hud_w, h),
		}
		self.buf = ColorFramebuffer(w, h)

		pg.clock.schedule_interval(self.tick, 1 / 60)

	@property
	def texture(self) -> pg.image.Texture:
		return self.buf.texture

	@property
	def active_hud(self):
		return self.state_to_huds.get(state.uav_state)

	def tick(self, dt: float):
		if state.has_operator:
			self.yaw = state.operator_dir_yaw
		else:
			unclamped_yaw = self.yaw + dt * self.scroll_yawspeed
			self.yaw = (unclamped_yaw + pi) % (2 * pi) - pi

	def render(self):
		if self.active_hud is None:
			self.buf.bind()
			gl.glClear(gl.GL_COLOR_BUFFER_BIT)
			self.buf.unbind()
			return

		self.active_hud.render()
		tex = self.active_hud.texture

		self.buf.bind()
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)

		# TODO: Use sprites here for a bit of a performance improvement
		tile_count = 1 if state.has_operator else self.tile_count
		w = tex.width * tile_count
		x = self.buf.texture.width // 2 - w // 2
		for i in range(tile_count):
			tex.blit(x + i * tex.width, 0)

		self.buf.unbind()
