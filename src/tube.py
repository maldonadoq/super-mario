import pygame as pg

class Tube(pg.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()

		self.image = pg.image.load('images/utils/tube.png').convert_alpha()

		length = (12 - y) * 32
		self.image = self.image.subsurface(0, 0, 64, length)
		self.rect = pg.Rect(x*32, y*32, 64, length)

	def render(self, game):
		game.screen.blit(self.image, game.get_map().get_camera().apply(self))