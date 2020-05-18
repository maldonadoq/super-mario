import pygame as pg

class GameUI:
	def __init__(self):
		self.font = pg.font.Font('fonts/emulogic.ttf', 15)
		self.text = 'score coins world time lives'

	def render(self, game):
		x = 10

		for word in self.text.split():
			rect = self.font.render(word, False, (255, 255, 255))
			game.screen.blit(rect, (x,0))
			x += 168

		text = self.font.render(str(game.get_map().get_player().score), False, (255, 255, 255))
		rect = text.get_rect(center=(60, 35))
		game.screen.blit(text, rect)

		text = self.font.render(str(game.get_map().get_player().coins), False, (255, 255, 255))
		rect = text.get_rect(center=(230, 35))
		game.screen.blit(text, rect)

		text = self.font.render(game.get_map().get_name(), False, (255, 255, 255))
		rect = text.get_rect(center=(395, 35))
		game.screen.blit(text, rect)

		text = self.font.render(str(game.get_map().time), False, (255, 255, 255))
		rect = text.get_rect(center=(557, 35))
		game.screen.blit(text, rect)

		text = self.font.render(str(game.get_map().get_player().num_lives), False, (255, 255, 255))
		rect = text.get_rect(center=(730, 35))
		game.screen.blit(text, rect)
		