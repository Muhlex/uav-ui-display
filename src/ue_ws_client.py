import json
from websockets.sync.client import connect

from pyglet.math import Vec3
from state import state


def start_ws_client(uri: str, rcp_name: str):
	register_msg = json.dumps(
		{
			"MessageName": "preset.register",
			"Parameters": {"PresetName": f"{rcp_name}"},
		}
	)
	with connect(uri) as ws:
		ws.send(register_msg)

		while True:
			receive_msg = json.loads(ws.recv(decode=False))
			if receive_msg["Type"] != "PresetFieldsChanged":
				continue
			for field in receive_msg["ChangedFields"]:
				name = field["PropertyLabel"]
				value = field["PropertyValue"]
				update_state(name, value)


def update_state(name: str, ue_value):
	if "X" in ue_value and "Y" in ue_value and "Z" in ue_value:
		value = Vec3(ue_value["X"], ue_value["Z"], ue_value["Y"])  # in UE, Z is up
	else:
		value = ue_value
	setattr(state, name, value)
