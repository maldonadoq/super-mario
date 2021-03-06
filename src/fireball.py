import pygame as pg

from .values import gravity

class Fireball(object):
	def __init__(self, x_pos, y_pos, move_direction: bool):
		super().__init__()

		self.rect = pg.Rect(x_pos, y_pos, 16, 16)
		self.state = 0
		self.direction = move_direction

		if(move_direction):
			self.x_vel = 5
		else:
			self.x_vel = -5

		self.y_vel = 0

		self.current_image = 0
		self.image_tick = 0

		self.images = [pg.image.load('images/fire/fireball.png').convert_alpha()]

		self.images.append(pg.transform.flip(self.images[0], 0, 90))
		self.images.append(pg.transform.flip(self.images[0], 90, 90))
		self.images.append(pg.transform.flip(self.images[0], 90, 0))

		self.images.append(pg.image.load('images/fire/firework0.png').convert_alpha())
		self.images.append(pg.image.load('images/fire/firework1.png').convert_alpha())
		self.images.append(pg.image.load('images/fire/firework2.png').convert_alpha())

	def update_image(self, game):
		self.image_tick += 1

		if(self.state == 0):
			if(self.image_tick % 15 == 0):
				self.current_image += 1
				if(self.current_image > 3):
					self.current_image = 0
					self.image_tick = 0

		elif(self.state == -1):
			if(self.image_tick % 10 == 0):
				self.current_image += 1
			if(self.current_image == 7):
				game.world.remove_whizbang(self)

	def start_boom(self):
		self.x_vel = 0
		self.y_vel = 0
		self.current_image = 4
		self.image_tick = 0
		self.state = -1

	def update_x_pos(self, blocks):
		self.rect.x += self.x_vel
	  
		for block in blocks:
			if(block != 0 and block.type != 'background_object'):
				if(pg.Rect.colliderect(self.rect, block.rect)):
					# Fireball blows up only when collides on x-axis
					self.start_boom()

	def update_y_pos(self, blocks):
		self.rect.y += self.y_vel
		for block in blocks:
			if(block != 0 and block.type != 'background_object'):
				if(pg.Rect.colliderect(self.rect, block.rect)):
					self.rect.bottom = block.rect.top
					self.y_vel = -3

	def check_map_borders(self, game):
		if(self.rect.x <= 0):
			game.world.remove_whizbang(self)
		elif(self.rect.x >= 6768):
			game.world.remove_whizbang(self)
		elif(self.rect.y > 448):
			game.world.remove_whizbang(self)

	def move(self, game):
		self.y_vel += gravity

		blocks = game.world.get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
		self.update_y_pos(blocks)
		self.update_x_pos(blocks)

		self.check_map_borders(game)

	def check_collision_with_mobs(self, game):
		for mob in game.world.mobs:
			if(self.rect.colliderect(mob.rect)):
				if(mob.collision):
					mob.die(game, instantly=False, crushed=False)
					self.start_boom()

	def update(self, game):
		if(self.state == 0):
			self.update_image(game)
			self.move(game)
			self.check_collision_with_mobs(game)
		elif(self.state == -1):
			self.update_image(game)

	def render(self, game):
		game.screen.blit(self.images[self.current_image], game.world.camera.apply(self))
