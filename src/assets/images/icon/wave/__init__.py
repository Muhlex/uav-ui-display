import pyglet as pg

images = [
	pg.resource.image("assets/images/icon/wave/0.png"),
	pg.resource.image("assets/images/icon/wave/1.png"),
	pg.resource.image("assets/images/icon/wave/2.png"),
]

frames = [
	pg.image.animation.AnimationFrame(images[0], duration=0.4),
	pg.image.animation.AnimationFrame(images[1], duration=0.4),
	pg.image.animation.AnimationFrame(images[0], duration=0.4),
	pg.image.animation.AnimationFrame(images[2], duration=0.4),
]

wave = pg.image.animation.Animation(frames)
