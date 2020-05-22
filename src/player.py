import pygame as pg

from .values import *

class Player:
	def __init__(self, x_pos, y_pos):
		self.num_lives = 3
		self.score = 0
		self.coins = 0

		self.visible = True
		self.sprite_tick = 0
		self.power_lvl = 0

		self.unkillable = False
		self.unkillable_time = 0

		self.in_level_up_animation = False
		self.in_level_up_animation_time = 0
		self.in_level_down_animation = False
		self.in_level_down_animation_time = 0

		self.already_jumped = False
		self.next_jump_time = 0
		self.next_fireball_time = 0
		self.x_vel = 0
		self.y_vel = 0
		self.direction = True
		self.on_ground = False
		self.fast_moving = False
		
		self.pos_x = x_pos

		self.image = pg.image.load('images/mario/mario.png').convert_alpha()
		self.sprites = []
		self.load_sprites()

		self.rect = pg.Rect(x_pos, y_pos, 32, 32)

	def load_sprites(self):
		self.sprites = [
			# 0 Small, stay
			pg.image.load('images/mario/mario.png'),
			# 1 Small, move 0
			pg.image.load('images/mario/mario_move0.png'),
			# 2 Small, move 1
			pg.image.load('images/mario/mario_move1.png'),
			# 3 Small, move 2
			pg.image.load('images/mario/mario_move2.png'),
			# 4 Small, jump
			pg.image.load('images/mario/mario_jump.png'),
			# 5 Small, end 0
			pg.image.load('images/mario/mario_end.png'),
			# 6 Small, end 1
			pg.image.load('images/mario/mario_end1.png'),
			# 7 Small, stop
			pg.image.load('images/mario/mario_st.png'),

			# =============================================

			# 8 Big, stay
			pg.image.load('images/mario/mario1.png'),
			# 9 Big, move 0
			pg.image.load('images/mario/mario1_move0.png'),
			# 10 Big, move 1
			pg.image.load('images/mario/mario1_move1.png'),
			# 11 Big, move 2
			pg.image.load('images/mario/mario1_move2.png'),
			# 12 Big, jump
			pg.image.load('images/mario/mario1_jump.png'),
			# 13 Big, end 0
			pg.image.load('images/mario/mario1_end.png'),
			# 14 Big, end 1
			pg.image.load('images/mario/mario1_end1.png'),
			# 15 Big, stop
			pg.image.load('images/mario/mario1_st.png'),

			# =============================================

			# 16 Big_fireball, stay
			pg.image.load('images/mario/mario2.png'),
			# 17 Big_fireball, move 0
			pg.image.load('images/mario/mario2_move0.png'),
			# 18 Big_fireball, move 1
			pg.image.load('images/mario/mario2_move1.png'),
			# 19 Big_fireball, move 2
			pg.image.load('images/mario/mario2_move2.png'),
			# 20 Big_fireball, jump
			pg.image.load('images/mario/mario2_jump.png'),
			# 21 Big_fireball, end 0
			pg.image.load('images/mario/mario2_end.png'),
			# 22 Big_fireball, end 1
			pg.image.load('images/mario/mario2_end1.png'),
			# 23 Big_fireball, stop
			pg.image.load('images/mario/mario2_st.png'),
		]

		# Left side
		for i in range(len(self.sprites)):
			self.sprites.append(pg.transform.flip(self.sprites[i], 180, 0))
			
		# Power level changing, right
		self.sprites.append(pg.image.load('images/mario/mario_lvlup.png').convert_alpha())
		# Power level changing, left
		self.sprites.append(pg.transform.flip(self.sprites[-1], 180, 0))
		# Death
		self.sprites.append(pg.image.load('images/mario/mario_death.png').convert_alpha())

	def update(self, game):
		self.player_physics(game)
		self.update_image(game)
		self.update_unkillable_time()

	def player_physics(self, game):
		if(game.key_right):
			self.x_vel += speed_increase_rate
			self.direction = True
		if(game.key_left):
			self.x_vel -= speed_increase_rate
			self.direction = False
		if(not game.key_up):
			self.already_jumped = False
		elif(game.key_up):
			if(self.on_ground and not self.already_jumped):
				self.y_vel = -jump_power
				self.already_jumped = True
				self.next_jump_time = pg.time.get_ticks() + 750
				if(self.power_lvl >= 1):
					game.sounds.play('big_mario_jump', 0, 0.5)
				else:
					game.sounds.play('small_mario_jump', 0, 0.5)

		# Fireball shoot and fast moving
		self.fast_moving = False
		if(game.key_shift):
			self.fast_moving = True
			if(self.power_lvl == 2):
				if(pg.time.get_ticks() > self.next_fireball_time):
					if(not (self.in_level_up_animation or self.in_level_down_animation)):
						if(len(game.world.projectiles) < 2):
							self.shoot_fireball(game, self.rect.x, self.rect.y, self.direction)

		if(not (game.key_right or game.key_left)):
			if(self.x_vel > 0):
				self.x_vel -= speed_decrease_rate
			elif(self.x_vel < 0):
				self.x_vel += speed_decrease_rate
		else:
			if(self.x_vel > 0):
				if(self.fast_moving):
					if(self.x_vel > max_fastmove_speed):
						self.x_vel = max_fastmove_speed
				else:
					if(self.x_vel > max_move_speed):
						self.x_vel = max_move_speed
			if(self.x_vel < 0):
				if(self.fast_moving):
					if((-self.x_vel) > max_fastmove_speed):
						self.x_vel = -max_fastmove_speed
				else:
					if((-self.x_vel) > max_move_speed):
						self.x_vel = -max_move_speed

		# removing the computational error
		if(0 < self.x_vel < speed_decrease_rate):
			self.x_vel = 0
		if(0 > self.x_vel > -speed_decrease_rate):
			self.x_vel = 0

		if(not self.on_ground):
			# Moving up, button is pressed
			if(self.y_vel < 0 and game.key_up):
				self.y_vel += gravity
				
			# Moving up, button is not pressed - low jump
			elif(self.y_vel < 0 and not game.key_up):
				self.y_vel += gravity * low_jump_multiplier
			
			# Moving down
			else:
				self.y_vel += gravity * fall_multiplier
			
			if(self.y_vel > max_fall_speed):
				self.y_vel = max_fall_speed

		blocks = game.world.get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
		
		self.pos_x += self.x_vel
		self.rect.x = self.pos_x
		
		self.update_x_pos(blocks)

		self.rect.y += self.y_vel
		self.update_y_pos(blocks, game)

		# on_ground parameter won't be stable without this piece of code
		coord_y = self.rect.y // 32
		if(self.power_lvl > 0):
			coord_y += 1
		for block in game.world.get_blocks_below(self.rect.x // 32, coord_y):
			if(block != 0 and block.type != 'background_object'):
				if(pg.Rect(self.rect.x, self.rect.y + 1, self.rect.w, self.rect.h).colliderect(block.rect)):
					self.on_ground = True

		# Map border check
		if(self.rect.y > 448):
			game.world.player_death(game)

		# End Flag collision check
		if(self.rect.colliderect(game.world.flag.pillar_rect)):
			game.world.player_win(game)

	def set_image(self, image_id):

		# "Dead" sprite
		if(image_id == len(self.sprites)):
			self.image = self.sprites[-1]

		elif(self.direction):
			self.image = self.sprites[image_id + self.power_lvl * 8]
		else:
			self.image = self.sprites[image_id + self.power_lvl * 8 + 24]

	def update_image(self, game):

		self.sprite_tick += 1
		if(game.key_shift):
			self.sprite_tick += 1

		if(self.power_lvl in (0, 1, 2)):

			if(self.x_vel == 0):
				self.set_image(0)
				self.sprite_tick = 0

			# Player is running
			elif(
					((self.x_vel > 0 and game.key_right and not game.key_left) or
					 (self.x_vel < 0 and game.key_left and not game.key_right)) or
					(self.x_vel > 0 and not (game.key_left or game.key_right)) or
					(self.x_vel < 0 and not (game.key_left or game.key_right))
			):
							 
				if(self.sprite_tick > 30):
					self.sprite_tick = 0
				   
				if(self.sprite_tick <= 10):
					self.set_image(1)
				elif(11 <= self.sprite_tick <= 20):
					self.set_image(2)
				elif(21 <= self.sprite_tick <= 30):
					self.set_image(3)
				elif(self.sprite_tick == 31):
					self.sprite_tick = 0
					self.set_image(1)

			# Player decided to move in the another direction, but hasn't stopped yet
			elif((self.x_vel > 0 and game.key_left and not game.key_right) or (self.x_vel < 0 and game.key_right and not game.key_left)):
				self.set_image(7)
				self.sprite_tick = 0

			if(not self.on_ground):
				self.sprite_tick = 0
				self.set_image(4)

	def update_unkillable_time(self):
		if(self.unkillable):
			self.unkillable_time -= 1
			if(self.unkillable_time == 0):
				self.unkillable = False

	def update_x_pos(self, blocks):
		for block in blocks:
			if(block != 0 and block.type != 'background_object'):
				block.debugLight = True
				if(pg.Rect.colliderect(self.rect, block.rect)):
					if(self.x_vel > 0):
						self.rect.right = block.rect.left
						self.pos_x = self.rect.left
						self.x_vel = 0
					elif(self.x_vel < 0):
						self.rect.left = block.rect.right
						self.pos_x = self.rect.left
						self.x_vel = 0

	def update_y_pos(self, blocks, game):
		self.on_ground = False
		for block in blocks:
			if(block != 0 and block.type != 'background_object'):
				if(pg.Rect.colliderect(self.rect, block.rect)):

					if(self.y_vel > 0):
						self.on_ground = True
						self.rect.bottom = block.rect.top
						self.y_vel = 0

					elif(self.y_vel < 0):
						self.rect.top = block.rect.bottom
						self.y_vel = -self.y_vel / 3
						self.activate_block_action(game, block)

	def activate_block_action(self, game, block):
		# Question Block
		if(block.type_id == 22):
			game.sounds.play('block_hit', 0, 0.5)
			if(not block.is_activated):
				block.spawn_bonus(game)

		# Brick Platform
		elif(block.type_id == 23):
			if(self.power_lvl == 0):
				block.shaking = True
				game.sounds.play('block_hit', 0, 0.5)
			else:
				block.destroy(game)
				game.sounds.play('brick_break', 0, 0.5)
				self.add_score(50)

	def reset(self, reset_all):
		self.direction = True
		self.rect.x = 96
		self.pos_x = 96
		self.rect.y = 351
		if(self.power_lvl != 0):
			self.power_lvl = 0
			self.rect.y += 32
			self.rect.h = 32

		if(reset_all):
			self.score = 0
			self.coins = 0
			self.num_lives = 3

			self.visible = True
			self.sprite_tick = 0
			self.power_lvl = 0
			self.in_level_up_animation = False
			self.in_level_up_animation_time = 0

			self.unkillable = False
			self.unkillable_time = 0

			self.in_level_down_animation = False
			self.in_level_down_animation_time = 0

			self.already_jumped = False
			self.x_vel = 0
			self.y_vel = 0
			self.on_ground = False

	def reset_jump(self):
		self.y_vel = 0
		self.already_jumped = False

	def reset_move(self):
		self.x_vel = 0
		self.y_vel = 0

	def jump_on_mob(self):
		self.already_jumped = True
		self.y_vel = -4
		self.rect.y -= 6

	def set_power_lvl(self, power_lvl, game):
		if(self.power_lvl == 0 == power_lvl and not self.unkillable):
			game.world.player_death(game)
			self.in_level_up_animation = False
			self.in_level_down_animation = False

		elif(self.power_lvl == 0 and self.power_lvl < power_lvl):
			self.power_lvl = 1
			game.sounds.play('mushroom_eat', 0, 0.5)
			game.world.spawn_score_text(self.rect.x + 16, self.rect.y, score=1000)
			self.add_score(1000)
			self.in_level_up_animation = True
			self.in_level_up_animation_time = 61

		elif(self.power_lvl == 1 and self.power_lvl < power_lvl):
			game.sounds.play('mushroom_eat', 0, 0.5)
			game.world.spawn_score_text(self.rect.x + 16, self.rect.y, score=1000)
			self.add_score(1000)
			self.power_lvl = 2

		elif(self.power_lvl > power_lvl):
			game.sounds.play('pipe', 0, 0.5)
			self.in_level_down_animation = True
			self.in_level_down_animation_time = 200
			self.unkillable = True
			self.unkillable_time = 200

		else:
			game.sounds.play('mushroom_eat', 0, 0.5)
			game.world.spawn_score_text(self.rect.x + 16, self.rect.y, score=1000)
			self.add_score(1000)

	def change_power_lvl_animation(self):

		if(self.in_level_down_animation):
			self.in_level_down_animation_time -= 1

			if(self.in_level_down_animation_time == 0):
				self.in_level_down_animation = False
				self.visible = True
			elif(self.in_level_down_animation_time % 20 == 0):
				if(self.visible):
					self.visible = False
				else:
					self.visible = True
				if(self.in_level_down_animation_time == 100):
					self.power_lvl = 0
					self.rect.y += 32
					self.rect.h = 32

		elif(self.in_level_up_animation):
			self.in_level_up_animation_time -= 1

			if(self.in_level_up_animation_time == 0):
				self.in_level_up_animation = False
				self.rect.y -= 32
				self.rect.h = 64

			elif(self.in_level_up_animation_time in (60, 30)):
				if(self.direction):
					self.image = self.sprites[-3]
				else:
					self.image = self.sprites[-2]

				self.rect.y -= 16
				self.rect.h = 48

			elif(self.in_level_up_animation_time in (45, 15)):
				if(self.direction):
					self.image = self.sprites[0]
				else:
					self.image = self.sprites[24]

				self.rect.y += 16
				self.rect.h = 32

	def flag_animation_move(self, game, walk_to_castle):
		if(walk_to_castle):
			self.direction = True

			if(not self.on_ground):
				if(self.y_vel <= max_fall_speed):
					self.y_vel += gravity

			x = self.rect.x // 32
			y = self.rect.y // 32
			blocks = game.world.get_blocks_for_collision(x, y)

			self.rect.x += self.x_vel
			if(self.rect.colliderect(game.world.map[205][11])):
				self.visible = False
				game.world.event.player_in_castle = True
			self.update_x_pos(blocks)

			self.rect.top += self.y_vel
			self.update_y_pos(blocks, game)

			# on_ground works incorrect without this piece of code
			x = self.rect.x // 32
			y = self.rect.y // 32
			if(self.power_lvl > 0):
				y += 1
			for block in game.world.get_blocks_below(x, y):
				if(block != 0 and block.type != 'background_object'):
					if(pg.Rect(self.rect.x, self.rect.y + 1, self.rect.w, self.rect.h).colliderect(block.rect)):
						self.on_ground = True

		else:
			if(game.world.flag.flag_rect.y + 20 > self.rect.y + self.rect.h):
				self.rect.y += 3

	def shoot_fireball(self, game, x, y, move_direction):
		game.world.spawn_fireball(x, y, move_direction)
		game.sounds.play('fireball', 0, 0.5)
		self.next_fireball_time = pg.time.get_ticks() + 400

	def add_coins(self, count):
		self.coins += count

	def add_score(self, count):
		self.score += count

	def render(self, game):
		if(self.visible):
			game.screen.blit(self.image, game.world.camera.apply(self))
