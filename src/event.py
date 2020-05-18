
import pygame as pg

from .values import gravity, fall_multiplier

class Event:
	def __init__(self):
		# 0 = Kill/Game Over
		# 1 = Win (using flag)

		self.type = 0

		self.delay = 0
		self.time = 0
		self.x_vel = 0
		self.y_vel = 0
		self.game_over = False

		self.player_in_castle = False
		self.tick = 0
		self.score_tick = 0

	def reset(self):
		self.type = 0

		self.delay = 0
		self.time = 0
		self.x_vel = 0
		self.y_vel = 0
		self.game_over = False

		self.player_in_castle = False
		self.tick = 0
		self.score_tick = 0

	def start_kill(self, game, game_over):
		self.type = 0
		self.delay = 4000
		self.y_vel = -4
		self.time = pg.time.get_ticks()
		self.game_over = game_over

		game.get_sound().stop('overworld')
		game.get_sound().stop('overworld_fast')
		game.get_sound().play('death', 0, 0.5)

		# Sets "dead" sprite
		game.get_map().get_player().set_image(len(game.get_map().get_player().sprites))

	def start_win(self, game):
		self.type = 1
		self.delay = 2000
		self.time = 0

		game.get_sound().stop('overworld')
		game.get_sound().stop('overworld_fast')
		game.get_sound().play('level_end', 0, 0.5)

		game.get_map().get_player().set_image(5)
		game.get_map().get_player().x_vel = 1
		game.get_map().get_player().rect.x += 10
		
		if game.get_map().time >= 300:
			game.get_map().get_player().add_score(5000)
			game.get_map().spawn_score_text(game.get_map().get_player().rect.x + 16, game.get_map().get_player().rect.y, score=5000)
		elif 200 <= game.get_map().time < 300:
			game.get_map().get_player().add_score(2000)
			game.get_map().spawn_score_text(game.get_map().get_player().rect.x + 16, game.get_map().get_player().rect.y, score=2000)
		else:
			game.get_map().get_player().add_score(1000)
			game.get_map().spawn_score_text(game.get_map().get_player().rect.x + 16, game.get_map().get_player().rect.y, score=1000)

	def update(self, game):

		# Death
		if self.type == 0:
			self.y_vel += gravity * fall_multiplier if self.y_vel < 6 else 0
			game.get_map().get_player().rect.y += self.y_vel

			if pg.time.get_ticks() > self.time + self.delay:
				if not self.game_over:
					game.get_map().get_player().reset_move()
					game.get_map().get_player().reset_jump()
					game.get_map().reset(False)
					game.get_sound().play('overworld', 9999999, 0.5)
				else:
					game.get_mm().current_game_state = 'loading'
					game.get_mm().loading_menu.set_text_and_type('Game Over', False)
					game.get_mm().loading_menu.update_time()
					game.get_sound().play('game_over', 0, 0.5)

		# Flag win
		elif self.type == 1:

			if not self.player_in_castle:

				if not game.get_map().flag.flag_omitted:
					game.get_map().get_player().set_image(5)
					game.get_map().flag.move_flag_down()
					game.get_map().get_player().flag_animation_move(game, False)

				else:
					self.tick += 1
					if self.tick == 1:
						game.get_map().get_player().direction = False
						game.get_map().get_player().set_image(6)
						game.get_map().get_player().rect.x += 20
					elif self.tick >= 30:
						game.get_map().get_player().flag_animation_move(game, True)
						game.get_map().get_player().update_image(game)

			else:
				if game.get_map().time > 0:
					self.score_tick += 1
					if self.score_tick % 10 == 0:
						game.get_sound().play('scorering', 0, 0.5)

					game.get_map().time -= 1
					game.get_map().get_player().add_score(50)

				else:
					if self.time == 0:
						self.time = pg.time.get_ticks()

					elif pg.time.get_ticks() >= self.time + self.delay:
						game.get_mm().current_game_state = 'loading'
						game.get_mm().loading_menu.set_text_and_type('End Game', False)
						game.get_mm().loading_menu.update_time()
						game.get_sound().play('game_over', 0, 0.5)
