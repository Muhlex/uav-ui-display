import pyglet as pg

images = [
	pg.resource.image("assets/images/person/wave/0.png"),
	pg.resource.image("assets/images/person/wave/1.png"),
	pg.resource.image("assets/images/person/wave/2.png"),
	pg.resource.image("assets/images/person/wave/3.png"),
	pg.resource.image("assets/images/person/wave/4.png"),
]

frames = [
	pg.image.animation.AnimationFrame(images[1], duration=0.2),
	pg.image.animation.AnimationFrame(images[2], duration=0.1),
	pg.image.animation.AnimationFrame(images[3], duration=0.2),
	pg.image.animation.AnimationFrame(images[4], duration=0.3),
	pg.image.animation.AnimationFrame(images[3], duration=0.2),
	pg.image.animation.AnimationFrame(images[2], duration=0.1),
	pg.image.animation.AnimationFrame(images[1], duration=0.2),
	pg.image.animation.AnimationFrame(images[0], duration=0.3),
]

wave = pg.image.animation.Animation(frames)
