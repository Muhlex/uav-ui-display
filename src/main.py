import pyglet as pg

import config as config

from ue.receive import UEReceiver
from ue.send import UESender
from renderer import Renderer

if __name__ == '__main__':
	receiver = UEReceiver("127.0.0.1", 7001)
	sender = UESender("LED Matrix")
	renderer = Renderer(matrix_width=480, matrix_height=96, sender=sender)

	try:
		pg.app.run()
	except KeyboardInterrupt:
		pass
