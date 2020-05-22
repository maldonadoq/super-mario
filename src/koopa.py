import pygame as pg

from .entity import Entity
from .values import gravity

class Koopa(Entity):
	def __init__(self, x_pos, y_pos, move_direction):
		super().__init__()
		self.rect = pg.Rect(x_pos, y_pos, 32, 46)

		self.move_direction = move_direction

		if(move_direction):
			self.x_vel = 1
		else:
			self.x_vel = -1

		self.current_image = 0
		self.image_tick = 0
		self.images = [
			pg.image.load('images/enemy/koopa_0.png').convert_alpha(),
			pg.image.load('images/enemy/koopa_1.png').convert_alpha(),
			pg.image.load('images/enemy/koopa_dead.png').convert_alpha()
		]
		self.images.append(pg.transform.flip(self.images[0], 180, 0))
		self.images.append(pg.transform.flip(self.images[1], 180, 0))
		self.images.append(pg.transform.flip(self.images[2], 0, 180))

	"""
	States: 
	0 - Just walking around
	1 - Hidden 
	2 - Hidden and fast moving
	-1 - Dead
	"""

	def check_collision_with_player(self, game):
		if(self.collision):
			if(self.rect.colliderect(game.world.player.rect)):
				if(self.state != -1):
					if(game.world.player.y_vel > 0):
						self.change_state(game)
						game.sounds.play('kill_mob', 0, 0.5)
						game.world.player.reset_jump()
						game.world.player.jump_on_mob()
					else:
						if(not game.world.player.unkillable):
							game.world.player.set_powerlvl(0, game)

	def check_collision_with_mobs(self, game):
		for mob in game.world.mobs:
			if(mob is not self):
				if(self.rect.colliderect(mob.rect)):
					if(mob.collision):
						mob.die(game, instantly=False, crushed=False)

	def die(self, game, instantly, crushed):
		if(not instantly):
			game.world.player.add_score(game.world.score_for_killing_mob)
			game.world.spawn_score_text(self.rect.x + 16, self.rect.y)
			self.state = -1
			self.y_vel = -4
			self.current_image = 5
		else:
			game.world.mobs.remove(self)

	def change_state(self, game):
		self.state += 1
		self.current_image = 2

		# 0 to 1 state
		if(self.rect.h == 46):
			self.x_vel = 0
			self.rect.h = 32
			self.rect.y += 14
			game.world.player.add_score(100)
			game.world.spawn_score_text(self.rect.x + 16, self.rect.y, score=100)

		# 1 to 2
		elif(self.state == 2):
			game.world.player.add_score(100)
			game.world.spawn_score_text(self.rect.x + 16, self.rect.y, score=100)

			if(game.world.player.rect.x - self.rect.x <= 0):
				self.x_vel = 6
			else:
				self.x_vel = -6

		# 2 to 3
		elif(self.state == 3):
			self.die(game, instantly=False, crushed=False)

	def update_image(self):
		self.image_tick += 1

		if(self.x_vel > 0):
			self.move_direction = True
		else:
			self.move_direction = False

		if(self.image_tick == 35):
			if(self.move_direction):
				self.current_image = 4
			else:
				self.current_image = 1
		elif(self.image_tick == 70):
			if(self.move_direction):
				self.current_image = 3
			else:
				self.current_image = 0
			self.image_tick = 0

	def update(self, game):
		if(self.state == 0):
			self.update_image()

			if(not self.on_ground):
				self.y_vel += gravity

			blocks = game.world.get_blocks_for_collision(self.rect.x // 32, (self.rect.y - 14) // 32)
			self.update_x_pos(blocks)
			self.update_y_pos(blocks)

			self.check_map_borders(game)

		elif(self.state == 1):
			blocks = game.world.get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
			self.update_x_pos(blocks)
			self.update_y_pos(blocks)

			self.check_map_borders(game)

		elif(self.state == 2):
			if(not self.on_ground):
				self.y_vel += gravity

			blocks = game.world.get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
			self.update_x_pos(blocks)
			self.update_y_pos(blocks)

			self.check_map_borders(game)
			self.check_collision_with_mobs(game)

		elif(self.state == -1):
			self.rect.y += self.y_vel
			self.y_vel += gravity

			self.check_map_borders(game)

	def render(self, game):
		game.screen.blit(self.images[self.current_image], game.world.camera.apply(self))
