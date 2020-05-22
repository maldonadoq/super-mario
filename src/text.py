import pygame as pg

class Text:
	def __init__(self, text, font_size, rect_center, font='Emulogic', text_color = (255, 255, 255)):
		self.font = pg.font.Font('fonts/emulogic.ttf', font_size)
		self.text = self.font.render(text, False, text_color)
		self.rect = self.text.get_rect(center=rect_center)
		self.y_offset = 0

	def update(self, game):
		self.rect.y -=1
		self.y_offset -= 1

		if(self.y_offset == -100):
			game.world.remove_text(self)

	def render(self, game):
		game.screen.blit(self.text, self.rect)

	def render_in_game(self, game):
		game.screen.blit(self.text, game.world.camera.apply(self))