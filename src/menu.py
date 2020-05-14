import pygame as pg
from .values import wwidth, wheight

class MainMenu:
	def __init__(self):
		self.image = pg.image.load('images/utils/super_mario_bros.png').convert_alpha()
	
	def render(self, game):
		game.screen.blit(self.image, (50,50))

class LoadingMenu:
	def __init__(self, game):
		self.time = pg.time.get_ticks()
		self.loading = True
		self.background = pg.Surface((wwidth, wheight))
	
	def update(self, game):
		if(pg.time.get_ticks() >= self.time + (5250 if(not self.loading) else 2500)):
			if(self.loading):
				game.mm.current_game_state = 'game'
				game.get_sound().play('overworld', 999999, 0.5)
				game.get_map().in_event = False
			else:
				game.mm.current_game_state = 'main_menu'
				game.get_map().reset(True)
	
	def set_type(self, _type):
		self.loading = _type

	def render(self, game):
		game.screen.blit(self.background, (0,0))

	def update_time(self):
		self.time = pg.time.get_ticks()

class MenuManager:
	def __init__(self, game):
		self.current_game_state = 'main_menu'

		self.main_menu = MainMenu()
		self.loading_menu = LoadingMenu(game)

	def update(self, game):
		if(self.current_game_state == 'loading'):
			self.loading_menu.update(game)
		#elif(self.current_game_state == 'game'):
		#	game.get_map().update(game)

	def render(self, game):
		if(self.current_game_state == 'main_menu'):
			#game.get_map().render_map(game)
			self.main_menu.render(game)
		elif(self.current_game_state == 'loading'):
			self.loading_menu.render(game)
		#elif(self.current_game_state == 'game'):
		#	game.get_map().render(game)
		#	game.get_map().get_ui().render(game)
		
		pg.display.update()

	def start_loading(self):
		self.current_game_state = 'loading'
		self.loading_menu.update_time()