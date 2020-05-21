import pygame as pg

from .entity import Entity
from .values import gravity

class Mushroom(Entity):
	def __init__(self, x_pos, y_pos, move_direction):
		super().__init__()

		self.rect = pg.Rect(x_pos, y_pos, 32, 32)

		if move_direction:
			self.x_vel = 1
		else:
			self.x_vel = -1

		self.spawned = False
		self.spawn_y_offset = 0
		self.image = pg.image.load('images/utils/mushroom.png').convert_alpha()

	def check_collision_with_player(self, game):
		if self.rect.colliderect(game.get_map().get_player().rect):
			game.get_map().get_player().set_power_lvl(2, game)
			game.get_map().get_mobs().remove(self)

	def die(self, game, instantly, crushed):
		game.get_map().get_mobs().remove(self)

	def spawn_animation(self):
		self.spawn_y_offset -= 1
		self.rect.y -= 1

		if self.spawn_y_offset == - 32:
			self.spawned = True

	def update(self, game):
		if self.spawned:
			if not self.on_ground:
				self.y_vel += gravity

			blocks = game.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
			self.update_x_pos(blocks)
			self.update_y_pos(blocks)

			self.check_map_borders(game)
		else:
			self.spawn_animation()

	def render(self, game):
		game.screen.blit(self.image, game.get_map().get_camera().apply(self))
