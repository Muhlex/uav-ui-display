from threading import Thread
from json import dumps, loads
import atexit

from websockets.sync.client import connect, ClientConnection
from pyglet.math import Vec3

from state import state


class UEReceiver:
	def __init__(self, websockets_uri: str, remote_control_presets: list[str]):
		self.ws: ClientConnection | None = None
		self.uri = websockets_uri
		self.rcps = remote_control_presets

		atexit.register(lambda: self.ws.close() if self.ws is not None else None)

	def init(self):
		def thread():
			try:
				ws = connect(self.uri)
			except Exception as e:
				print(f"Failed to connect to Unreal Engine websocket server:\n{e}")
				return

			def get_rcp_register_message(rcp_name: str):
				return dumps(
					{
						"MessageName": "preset.register",
						"Parameters": {"PresetName": f"{rcp_name}"},
					}
				)

			rcp_register_messages = map(get_rcp_register_message, self.rcps)
			for msg in rcp_register_messages:
				ws.send(msg)

			while True:
				msg = loads(ws.recv(decode=False))
				if "Type" not in msg or msg["Type"] != "PresetFieldsChanged":
					continue
				for field in msg["ChangedFields"]:
					name = field["PropertyLabel"]
					value = field["PropertyValue"]
					self.update_state(name, value)

		Thread(target=thread, daemon=True).start()

	def update_state(self, name: str, ue_value):
		if "X" in ue_value and "Y" in ue_value and "Z" in ue_value:
			value = Vec3(ue_value["X"], ue_value["Z"], ue_value["Y"])  # in UE, Z is up
		else:
			value = ue_value
		setattr(state, name, value)
