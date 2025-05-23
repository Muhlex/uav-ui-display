from threading import Thread
import atexit

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

from enum import Enum

from math import radians
from pyglet.math import Vec3

import pyglet as pg

from state import state


class UEReceiver:
	def __init__(self, osc_ip: str, osc_port: int):
		def handle_state(address, *args):
			name = address.split("/")[-1]
			pg.clock.schedule_once(lambda _: self.update_state(name, *args), 0)

		def handle_default(address, *args):
			print(f'Received unhandled OSC message: "{address}" {args}')

		dispatcher = Dispatcher()
		dispatcher.map("/state/*", handle_state)
		dispatcher.set_default_handler(handle_default)
		server = ThreadingOSCUDPServer((osc_ip, osc_port), dispatcher)

		def thread():
			server.serve_forever()

		Thread(target=thread, daemon=True).start()
		atexit.register(lambda: server.shutdown())

	def update_state(self, name: str, *values):
		def convert_vec3(x: float, y: float, z: float):
			return Vec3(y, z, x)  # UE uses left-handed coordinate system with Z up

		if len(values) == 1:
			value = values[0]
			current = getattr(state, name)
			if isinstance(current, Enum):
				enum_type = type(current)
				value = enum_type(value)
		elif len(values) == 3:
			value = convert_vec3(*values)
		elif name == "bystanders" and len(values) % 7 == 0:
			origins = []
			angles = []
			for i in range(0, len(values), 7):
				origins.append(convert_vec3(*values[i : i + 3]))
				angles.append([radians((360 - angle) % 360) for angle in values[i + 3 : i + 7]])
			setattr(state, "bystander_origins", origins)
			setattr(state, "bystander_arms_angles", angles)
			return
		elif name == "obstacles" and len(values) % (3 * 2) == 0:
			value = []
			for i in range(0, len(values), 3 * 2):
				start = convert_vec3(*values[i : i + 3])
				end = convert_vec3(*values[i + 3 : i + 6])
				value.append((start, end))
		else:
			print(f"Ignoring unexpected values for '{name}': {values}")
			return

		setattr(state, name, value)
