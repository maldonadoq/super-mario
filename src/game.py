import pygame as pg

from values import *

class Game:
	def __init__(self):
		pg.init()

		pg.display.set_caption('Super Mario Bros')
		pg.display.set_mode((width, height))

		self.running = True

		self.world = Map('one')
		self.menu = MenuManager(self)

	
	def loop(self):
		while(self.running):
			self.update()
			self.render()

	def input(self):
