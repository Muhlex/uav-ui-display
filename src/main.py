from threading import Thread
from ue_ws_client import start_ws_client

import pyglet as pg

import config as config
from renderer import Renderer


renderer = Renderer()

renderer.debug.win.set_location(32, 64)
renderer.output.win.set_location(32, 64 + renderer.debug.win.height + 64)

unreal_ws_client_args = {"uri": "ws://127.0.0.1:30020", "rcp_name": "RCP_LED"}
Thread(target=start_ws_client, daemon=True, kwargs=unreal_ws_client_args).start()

pg.app.run()
