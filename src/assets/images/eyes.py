import pyglet as pg

from state import state, UAVState


class Eyes:
	def __init__(self, x: float, y: float, width: int, batch: pg.graphics.Batch | None = None):
		self.batch = batch or pg.graphics.Batch()
		self.circles: list[pg.shapes.Circle] = []

		self.x = x
		self.y = y

		def on_uav_state_change(uav_state: UAVState):
			match uav_state:
				case UAVState.SEARCH:
					radius = 4
					count = 12
					gap = (width - count * radius * 2) // count
					self.update_circles(count=count, radius=radius, gap=gap)
				case _:
					self.update_circles(count=2, radius=4, gap=10)

		state.subscribe("uav_state", on_uav_state_change)
		on_uav_state_change(state.uav_state)

	def update_circles(self, count: int, radius: int, gap: float):
		for circle in self.circles:
			circle.delete()

		w = radius * 2 * count + gap * (count - 1)
		x = self.x - w / 2

		self.circles = [
			pg.shapes.Circle(
				x + radius + i * (radius * 2 + gap),
				self.y,
				radius,
				color=(0, 50, 255, 255),
				batch=self.batch,
			)
			for i in range(count)
		]

	def draw(self):
		self.batch.draw()
