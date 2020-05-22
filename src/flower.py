import pygame as pg

from .entity import Entity

class Flower(Entity):
	def __init__(self, x_pos, y_pos):
		super().__init__()

		self.rect = pg.Rect(x_pos, y_pos, 32, 32)
		self.spawned = False
		self.spawn_y_offset = 0

		self.current_image = 0
		self.image_tick = 0
		self.images = (
			pg.image.load('images/flower/flower0.png').convert_alpha(),
			pg.image.load('images/flower/flower1.png').convert_alpha(),
			pg.image.load('images/flower/flower2.png').convert_alpha(),
			pg.image.load('images/flower/flower3.png').convert_alpha()
		)

	def check_collision_with_player(self, game):
		if self.rect.colliderect(game.world.player.rect):
			game.world.player.set_power_lvl(3, game)
			game.world.mobs.remove(self)

	def update_image(self):
		self.image_tick += 1

		if self.image_tick == 60:
			self.image_tick = 0
			self.current_image = 0

		elif self.image_tick % 15 == 0:
			self.current_image += 1

	def spawn_animation(self):
		self.spawn_y_offset -= 1
		self.rect.y -= 1

		if self.spawn_y_offset == -32:
			self.spawned = True

	def update(self, game):
		if(self.spawned):
			self.update_image()
		else:
			self.spawn_animation()

	def render(self, game):
		game.screen.blit(self.images[self.current_image], game.world.camera.apply(self))
