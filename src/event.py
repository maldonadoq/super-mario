
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

		game.sounds.stop('overworld')
		game.sounds.stop('overworld_fast')
		game.sounds.play('death', 0, 0.5)

		# Sets "dead" sprite
		game.world.player.set_image(len(game.world.player.sprites))

	def start_win(self, game):
		self.type = 1
		self.delay = 2000
		self.time = 0

		game.sounds.stop('overworld')
		game.sounds.stop('overworld_fast')
		game.sounds.play('level_end', 0, 0.5)

		game.world.player.set_image(5)
		game.world.player.x_vel = 1
		game.world.player.rect.x += 10
		
		if game.world.time >= 300:
			game.world.player.add_score(5000)
			game.world.spawn_score_text(game.world.player.rect.x + 16, game.world.player.rect.y, score=5000)
		elif 200 <= game.world.time < 300:
			game.world.player.add_score(2000)
			game.world.spawn_score_text(game.world.player.rect.x + 16, game.world.player.rect.y, score=2000)
		else:
			game.world.player.add_score(1000)
			game.world.spawn_score_text(game.world.player.rect.x + 16, game.world.player.rect.y, score=1000)

	def update(self, game):

		# Death
		if self.type == 0:
			self.y_vel += gravity * fall_multiplier if self.y_vel < 6 else 0
			game.world.player.rect.y += self.y_vel

			if pg.time.get_ticks() > self.time + self.delay:
				if not self.game_over:
					game.world.player.reset_move()
					game.world.player.reset_jump()
					game.world.reset(False)
					game.sounds.play('overworld', 9999999, 0.5)
				else:
					game.menu_manager.current_game_state = 'loading'
					game.menu_manager.loading_menu.set_text_and_type('Game Over', False)
					game.menu_manager.loading_menu.update_time()
					game.sounds.play('game_over', 0, 0.5)

		# Flag win
		elif self.type == 1:

			if not self.player_in_castle:

				if not game.world.flag.flag_omitted:
					game.world.player.set_image(5)
					game.world.flag.move_flag_down()
					game.world.player.flag_animation_move(game, False)

				else:
					self.tick += 1
					if self.tick == 1:
						game.world.player.direction = False
						game.world.player.set_image(6)
						game.world.player.rect.x += 20
					elif self.tick >= 30:
						game.world.player.flag_animation_move(game, True)
						game.world.player.update_image(game)

			else:
				if game.world.time > 0:
					self.score_tick += 1
					if self.score_tick % 10 == 0:
						game.sounds.play('scorering', 0, 0.5)

					game.world.time -= 1
					game.world.player.add_score(50)

				else:
					if self.time == 0:
						self.time = pg.time.get_ticks()

					elif pg.time.get_ticks() >= self.time + self.delay:
						game.menu_manager.current_game_state = 'loading'
						game.menu_manager.loading_menu.set_text_and_type('End Game', False)
						game.menu_manager.loading_menu.update_time()
						game.sounds.play('game_over', 0, 0.5)
