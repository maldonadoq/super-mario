import pygame as pg

from .values import gravity, fall_multiplier

class CoinDebris:    
	def __init__(self, x_pos, y_pos):
		self.rect = pg.Rect(x_pos, y_pos, 16, 28)

		self.y_vel = -2
		self.y_offset = 0
		self.moving_up = True

		self.current_image = 0
		self.image_tick = 0
		self.images = [
			pg.image.load('images/coin/coin_an0.png').convert_alpha(),
			pg.image.load('images/coin/coin_an1.png').convert_alpha(),
			pg.image.load('images/coin/coin_an2.png').convert_alpha(),
			pg.image.load('images/coin/coin_an3.png').convert_alpha()
		]

	def update(self, game):
		self.image_tick += 1

		if self.image_tick % 15 == 0:
			self.current_image += 1

		if self.current_image == 4:
			self.current_image = 0
			self.image_tick = 0

		if self.moving_up:
			self.y_offset += self.y_vel
			self.rect.y += self.y_vel
			
			if self.y_offset < -50:
				self.moving_up = False
				self.y_vel = -self.y_vel
		else:
			self.y_offset += self.y_vel
			self.rect.y += self.y_vel
			
			if self.y_offset == 0:
				game.world.debris.remove(self)

	def render(self, game):
		game.screen.blit(self.images[self.current_image], game.world.camera.apply(self))


class PlatformDebris:
	def __init__(self, x_pos, y_pos):
		self.image = pg.image.load('images/utils/block_debris0.png').convert_alpha()

		# 4 different parts
		self.rectangles = [
			pg.Rect(x_pos - 20, y_pos + 16, 16, 16),
			pg.Rect(x_pos - 20, y_pos - 16, 16, 16),
			pg.Rect(x_pos + 20, y_pos + 16, 16, 16),
			pg.Rect(x_pos + 20, y_pos - 16, 16, 16)
		]

		self.y_vel = -4
		self.rect = None

	def update(self, game):
		self.y_vel += gravity * fall_multiplier

		for i in range(len(self.rectangles)):
			self.rectangles[i].y += self.y_vel
			if(i < 2):
				self.rectangles[i].x -= 1
			else:
				self.rectangles[i].x += 1

		if self.rectangles[1].y > game.world.map_size[1] * 32:
			game.world.debris.remove(self)

	def render(self, game):
		for rect in self.rectangles:
			self.rect = rect
			game.screen.blit(self.image, game.world.camera.apply(self))
