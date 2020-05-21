import pygame as pg

from .entity import Entity
from .values import *

class Goombas(Entity):
	def __init__(self, x_pos, y_pos, move_direction):
		super().__init__()
		self.rect = pg.Rect(x_pos, y_pos, 32, 32)

		if move_direction:
			self.x_vel = 1
		else:
			self.x_vel = -1

		self.crushed = False

		self.current_image = 0
		self.image_tick = 0
		self.images = [
			pg.image.load('images/enemy/goombas_0.png').convert_alpha(),
			pg.image.load('images/enemy/goombas_1.png').convert_alpha(),
			pg.image.load('images/enemy/goombas_dead.png').convert_alpha()
		]

		self.images.append(pg.transform.flip(self.images[0], 0, 180))

	def die(self, game, instantly, crushed):
		if not instantly:
			game.get_map().get_player().add_score(game.get_map().score_for_killing_mob)
			game.get_map().spawn_score_text(self.rect.x + 16, self.rect.y)

			if crushed:
				self.crushed = True
				self.image_tick = 0
				self.current_image = 2
				self.state = -1
				game.get_sound().play('kill_mob', 0, 0.5)
				self.collision = False

			else:
				self.y_vel = -4
				self.current_image = 3
				game.get_sound().play('shot', 0, 0.5)
				self.state = -1
				self.collision = False

		else:
			game.get_map().get_mobs().remove(self)

	def check_collision_with_player(self, game):
		if self.collision:
			if self.rect.colliderect(game.get_map().get_player().rect):
				if self.state != -1:
					if game.get_map().get_player().y_vel > 0:
						self.die(game, instantly=False, crushed=True)
						game.get_map().get_player().reset_jump()
						game.get_map().get_player().jump_on_mob()
					else:
						if not game.get_map().get_player().unkillable:
							game.get_map().get_player().set_power_lvl(0, game)

	def update_image(self):
		self.image_tick += 1
		if self.image_tick == 14:
			self.current_image = 1
		elif self.image_tick == 28:
			self.current_image = 0
			self.image_tick = 0

	def update(self, game):
		if self.state == 0:
			self.update_image()

			if not self.on_ground:
				self.y_vel += gravity

			blocks = game.get_map().get_blocks_for_collision(int(self.rect.x // 32), int(self.rect.y // 32))
			self.update_x_pos(blocks)
			self.update_y_pos(blocks)

			self.check_map_borders(game)

		elif self.state == -1:
			if self.crushed:
				self.image_tick += 1
				if self.image_tick == 50:
					game.get_map().get_mobs().remove(self)
			else:
				self.y_vel += gravity
				self.rect.y += self.y_vel
				self.check_map_borders(game)

	def render(self, game):
		game.screen.blit(self.images[self.current_image], game.get_map().get_camera().apply(self))
