import pygame as pg

from .values import wwidth, wheight

class Camera:
	def __init__(self, width, height):
		self.rect = pg.Rect(0, 0, width, height)
		self.complex_camera(self.rect)

	def complex_camera(self, target):
		x = target.x
		y = target.y

		width = self.rect.width
		height = self.rect.height

		x = (-x + wwidth/2 - target.width/2)
		y = (-y + wheight/2 - target.height)

		x = min(0, x)
		y = max(-(self.rect.width - wwidth), x)
		y = wheight - self.rect.h

		return pg.Rect(x, y, width, height)

	def apply(self, target):
		return (target.rect.x + self.rect.x, target.rect.y)

	def update(self, target):
		self.rect = self.complex_camera(target)

	def reset(self):
		self.rect = pg.Rect(0, 0, self.rect.w, self.rect.h)