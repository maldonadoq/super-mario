import pygame as pg

from .menu import MenuManager
from .sounds import Sounds
from .values import wwidth, wheight, fps

class Game:
	def __init__(self):
		pg.init()

		pg.display.set_caption('Super Mario Bros')
		pg.display.set_mode((wwidth, wheight))

		self.screen = pg.display.set_mode((wwidth, wheight))
		self.clock = pg.time.Clock()
		
		# self.world = Map('one')
		self.sounds       = Sounds()
		self.menu_manager = MenuManager(self)

		self.running   = True
		self.key_right = False
		self.key_left  = False
		self.key_down  = False
		self.key_up    = False
		self.key_shift = False

	
	def loop(self):
		while(self.running):
			self.input()
			self.update()
			self.render()
			self.clock.tick(fps)

	def input(self):
		if(self.get_mm().current_game_state == 'game'):
			self.input_player()
		else:
			self.input_menu()

	def input_player(self):
		for ev in pg.event.get():
			if(ev.type == pg.QUIT):
				self.running = False

			elif(ev.type == pg.KEYDOWN):
				if(ev.key == pg.K_RIGHT):
					self.key_right = True
				elif(ev.key == pg.K_LEFT):
					self.key_left = True
				elif(ev.key == pg.K_DOWN):
					self.key_down = True
				elif(ev.key == pg.K_UP):
					self.key_up = True
				elif(ev.key == pg.K_LSHIFT):
					self.key_shift = True

			elif(ev.type == pg.KEYUP):
				if(ev.key == pg.K_RIGHT):
					self.key_right = False
				elif(ev.key == pg.K_LEFT):
					self.key_left = False
				elif(ev.key == pg.K_DOWN):
					self.key_down = False
				elif(ev.key == pg.K_UP):
					self.key_up = False
				elif(ev.key == pg.K_LSHIFT):
					self.key_shift = False

	def input_menu(self):
		for ev in pg.event.get():
			if(ev.type == pg.QUIT):
				self.running = False

			elif(ev.type == pg.KEYDOWN):
				if(ev.key == pg.K_RETURN):
					self.get_mm().start_loading()

	def update(self):
		self.get_mm().update(self)

	def render(self):
		self.get_mm().render(self)

	def get_mm(self):
		return self.menu_manager

	def get_sound(self):
		return self.sounds
