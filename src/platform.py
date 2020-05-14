import pygame as pg

class Platform:
	def __init__(self, x, y, image, type_id):
		self.image = image
		self.rect = pg.Rect(x, y, 32, 32)

		# 22 question
		# 23 brick

		self.type_id = type_id
		self.type = 'platform'

		self.shaking = False
		self.shaking_up = True
		self.shake_offset = 0

		if(self.type_id == 22):
			self.current_image = None
			self,image_tick = None
			self.is_activated = False
			self.bonus = 'coin'
	
	def update(self):
		pass