import pygame as pg
from .values import *

class MainMenu:
	def __init__(self):
		self.image = pg.image.load('images/super_mario_bros.png').convert_alpha()
	
	def render(self, core):
		core.screen.blit(self.image, (50,50))

class LoadingMenu:
	def __init__(self, core):
		self.time = pg.time.get_ticks()
		self.loading = True
		self.background = pg.Surface((width, height))
	
	def update(self, core):
		if(pg.time.get_ticks() >= self.time + (5250 if(not self.loading) else 2500)):
			if(self.loading):
				core.mm.current_game_state = 'game'
				core.get_sound().play('overworld', 999999, 0.5)
				core.get_map().in_event = False
			else:
				core.mm.current_game_state = 'menu'
				core.get_map().reset(True)
	
	def set_type(self, _type):
		self.loading = _type

	def render(self, core):
		core.screen.blit(self.background, (0,0))

	def update_time(self):
		self.time = pg.time.get_ticks()
