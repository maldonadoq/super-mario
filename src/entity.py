import pygame as pg

from .values import fall_multiplier

class Entity:
	def __init__(self):

		self.state = 0
		self.x_vel = 0
		self.y_vel = 0

		self.move_direction = True
		self.on_ground = False
		self.collision = True

		self.image = None
		self.rect = None

	def update_x_pos(self, blocks):
		self.rect.x += self.x_vel

		for block in blocks:
			if(block != 0 and block.type != 'background_object'):

				if(pg.Rect.colliderect(self.rect, block.rect)):

					if(self.x_vel > 0):
						self.rect.right = block.rect.left
						self.x_vel = - self.x_vel
					elif(self.x_vel < 0):
						self.rect.left = block.rect.right
						self.x_vel = - self.x_vel

	def update_y_pos(self, blocks):
		self.rect.y += self.y_vel * fall_multiplier

		self.on_ground = False
		for block in blocks:
			if(block != 0 and block.type != 'background_object'):
				if(pg.Rect.colliderect(self.rect, block.rect)):
					if(self.y_vel > 0):
						self.on_ground = True
						self.rect.bottom = block.rect.top
						self.y_vel = 0

	def check_map_borders(self, game):
		if(self.rect.y >= 448):
			self.die(game, True, False)
		if(self.rect.x <= 1 and self.x_vel < 0):
			self.x_vel = - self.x_vel

	def die(self, game, instantly, crushed):
		pass

	def render(self, game):
		pass
