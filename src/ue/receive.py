from threading import Thread
import atexit

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

from pyglet.math import Vec3

from state import state


class UEReceiver:
	def __init__(self, osc_ip: str, osc_port: int):
		def handle_state(address, *args):
			name = address.split("/")[-1]
			self.update_state(name, *args)

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
		if len(values) == 1:
			value = values
		elif len(values) == 3:
			value = Vec3(values[0], values[2], values[1])  # in UE, Z is up
		elif name == "obstacles" and len(values) % (3 * 2) == 0:
			value = []
			for i in range(0, len(values), 3 * 2):
				start = Vec3(values[i], values[i + 2], values[i + 1])
				end = Vec3(values[i + 3], values[i + 5], values[i + 4])
				value.append((start, end))
		else:
			print(f"Ignoring unexpected values for {name}: {values}")
			return

		setattr(state, name, value)
