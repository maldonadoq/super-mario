import pygame as pg

from pytmx.util_pygame import load_pygame

from .camera import Camera
from .event import Event
from .game_ui import GameUI
from .player import Player
from .flag import Flag
from .text import Text

from .platform import Platform
from .tube import Tube
from .debris import CoinDebris, PlatformDebris
from .goombas import Goombas
from .mushroom import Mushroom
from .flower import Flower
from .koopa import Koopa
from .fireball import Fireball

from .values import wwidth, wheight

class BackgroundObject:
	def __init__(self, x, y, image):
		self.rect = pg.Rect(x, y, 32, 32)
		self.image = image
		self.type = 'background_object'

	def render(self, game):
		game.screen.blit(self.image, game.get_map().get_camera().apply(self))

class Map:
	def __init__(self, world_name):
		self.objs = []
		self.objs_bg = []
		self.tubes = []
		self.debris = []
		self.mobs = []
		self.projectiles = []
		self.text_objects = []

		self.map = 0
		self.sky = 0
		self.flag = None
		self.map_size = (0,0)		

		self.textures = {}
		self.world_name = world_name
		self.load_world()		

		self.is_mob_spawned = [False, False]
		self.score_for_killing_mob = 100
		self.score_time = 0

		self.in_event = False
		self.time = 400
		self.tick = 0

		self.camera = Camera(self.map_size[0]*32, 14)
		self.event = Event()
		self.game_ui = GameUI()
		self.player = Player(128, 351)
	
	def load_world(self):
		tmx = load_pygame('worlds/one/W11.tmx')
		self.map_size = (tmx.width, tmx.height)

		self.sky = pg.Surface((wwidth, wheight))
		self.sky.fill((pg.Color('#5c94fc')))

		self.map = [[0]*tmx.height for i in range(tmx.width)]

		layer_num = 0

		for layer in tmx.visible_layers:
			for y in range(tmx.height):
				for x in range(tmx.width):
					image = tmx.get_tile_image(x, y, layer_num)

					if(image is not None):
						tile_id = tmx.get_tile_gid(x, y, layer_num)

						if(layer.name == 'Foreground'):
							# Question Block
							if(tile_id == 22):
								image = (
									image,	
									tmx.get_tile_image(0, 15, layer_num),
									tmx.get_tile_image(1, 15, layer_num),
									tmx.get_tile_image(2, 15, layer_num)
								)
							
							self.map[x][y] = Platform(x*tmx.tilewidth, y*tmx.tileheight, image, tile_id)
							self.objs.append(self.map[x][y])

						elif(layer.name == 'Background'):
							self.map[x][y] = BackgroundObject(x*tmx.tileheight, y*tmx.tilewidth, image)
							self.objs_bg.append(self.map[x][y])

			layer_num += 1

		self.spawn_tube(28, 10)
		self.spawn_tube(37, 9)
		self.spawn_tube(46, 8)
		self.spawn_tube(55, 8)
		self.spawn_tube(163, 10)
		self.spawn_tube(179, 10)

		self.mobs.append(Goombas(736, 352, False))
		self.mobs.append(Goombas(1295, 352, True))
		self.mobs.append(Goombas(1632, 352, False))
		self.mobs.append(Goombas(1672, 352, False))
		self.mobs.append(Goombas(5570, 352, False))
		self.mobs.append(Goombas(5620, 352, False))
		
		self.map[21][8].bonus = 'mushroom'
		self.map[78][8].bonus = 'mushroom'
		self.map[109][4].bonus = 'mushroom'

		self.flag = Flag(6336, 48)

	def reset(self, reset_all):
		self.objs = []
		self.objs_bg = []
		self.tubes = []
		self.debris = []
		self.mobs = []
		self.is_mob_spawned = [False, False]

		self.in_event = False
		self.flag = None
		self.sky = None
		self.map = None

		self.tick = 0
		self.time = 400

		self.map_size = (0, 0)
		self.textures = {}
		self.load_world()

		self.get_event().reset()
		self.get_player().reset(reset_all)
		self.get_camera().reset()

	def get_name(self):
		return self.world_name

	def get_player(self):
		return self.player

	def get_camera(self):
		return self.camera

	def get_event(self):
		return self.event

	def get_ui(self):
		return self.game_ui

	def get_blocks_for_collision(self, x, y):
		return (
			self.map[x][y - 1],
			self.map[x][y + 1],
			self.map[x][y],
			self.map[x - 1][y],
			self.map[x + 1][y],
			self.map[x + 2][y],
			self.map[x + 1][y - 1],
			self.map[x + 1][y + 1],
			self.map[x][y + 2],
			self.map[x + 1][y + 2],
			self.map[x - 1][y + 1],
			self.map[x + 2][y + 1],
			self.map[x][y + 3],
			self.map[x + 1][y + 3]
		)

	def get_blocks_below(self, x, y):
		return (
			self.map[x][y+1],
			self.map[x+1][y+1]
		)
	
	def get_mobs(self):
		return self.mobs

	def spawn_tube(self, x, y):
		self.tubes.append(Tube(x, y))

		for j in range(y, 12):
			for i in range(x, x+2):
				self.map[i][j] = Platform(i*32, j*32, image=None, type_id=0)

	def spawn_mushroom(self, x, y):
		self.get_mobs().append(Mushroom(x,y, True))

	def spawn_goombas(self, x, y, move_direction):
		self.get_mobs().append(Goombas(x, y, move_direction))

	def spawn_koopa(self, x, y, move_direction):
		self.get_mobs().append(Koopa(x, y, move_direction))

	def spawn_flower(self, x, y):
		self.mobs.append(Flower(x, y))

	def spawn_debris(self, x, y, _type):
		if(_type == 0):
			self.debris.append(PlatformDebris(x, y))
		elif(_type == 1):
			self.debris.append(CoinDebris(x, y))

	def spawn_fireball(self, x, y, move_direction):
		self.projectiles.append(Fireball(x, y, move_direction))
 
	def spawn_score_text(self, x, y, score=None):
		if(score is None):
			self.text_objects.append(Text(str(self.score_for_killing_mob), 16, (x,y)))

			self.score_time = pg.time.get_ticks()
			if(self.score_for_killing_mob < 1600):
				self.score_for_killing_mob *= 2

		else:
			self.text_objects.append(Text(str(score), 16, (x,y)))

	def remove_object(self, object):
		self.objs.remove(object)
		self.map[object.rect.x // 32][object.rect.y // 32] = 0

	def remove_whizbang(self, whizbang):
		self.projectiles.remove(whizbang)

	def remove_text(self, text_object):
		self.text_objects.remove(text_object)

	def update_player(self, game):
		self.get_player().update(game)

	def update_entities(self, game):
		for mob in self.mobs:
			mob.update(game)
			if(not self.in_event):
				self.entity_collisions(game)

	def update_time(self, game):
		if(not self.in_event):
			self.tick += 1
			if(self.tick % 40 == 0):
				self.time -= 1
				self.tick = 0

			if(self.time == 100 and self.tick == 1):
				game.get_sound().start_fast_music(game)
			elif(self.time == 0):
				self.player_death(game)

	def update_score_time(self):
		if(self.score_for_killing_mob != 100):
			if(pg.time.get_ticks() > self.score_time + 750):
				self.score_for_killing_mob //= 2

	def entity_collisions(self, game):
		if not game.get_map().get_player().unkillable:
			for mob in self.mobs:
				mob.check_collision_with_player(game)

	def try_spawn_mobs(self, game):
		if self.get_player().rect.x > 2080 and not self.is_mob_spawned[0]:
			self.spawn_goombas(2495, 224, False)
			self.spawn_goombas(2560, 96, False)
			self.is_mob_spawned[0] = True

		elif self.get_player().rect.x > 2460 and not self.is_mob_spawned[1]:
			self.spawn_goombas(3200, 352, False)
			self.spawn_goombas(3250, 352, False)
			self.spawn_koopa(3400, 352, False)
			self.spawn_goombas(3700, 352, False)
			self.spawn_goombas(3750, 352, False)
			self.spawn_goombas(4060, 352, False)
			self.spawn_goombas(4110, 352, False)
			self.spawn_goombas(4190, 352, False)
			self.spawn_goombas(4240, 352, False)
			self.is_mob_spawned[1] = True

	def player_death(self, game):
		self.in_event = True
		self.get_player().reset_jump()
		self.get_player().reset_move()
		self.get_player().num_lives -= 1

		if(self.get_player().num_lives == 0):
			self.get_event().start_kill(game, game_over=True)
		else:
			self.get_event().start_kill(game, game_over=False)

	def player_win(self, game):
		self.in_event = True
		self.get_player().reset_jump()
		self.get_player().reset_move()
		self.get_event().start_win(game)

	def update(self, game):

		self.update_entities(game)

		if(not game.get_map().in_event):
			if(self.get_player().in_level_up_animation):
				self.get_player().change_power_lvl_animation()
			elif(self.get_player().in_level_down_animation):
				self.get_player().change_power_lvl_animation()
				self.update_player(game)
			else:
				self.update_player(game)

		else:
			self.get_event().update(game)

		# Debris is 1) Particles which appears when player destroy a brick block
		# 2) Coins which appears when player activate a "question" platform
		for debris in self.debris:
			debris.update(game)

		# Player's fireballs
		for whizbang in self.projectiles:
			whizbang.update(game)

		# Text which represent how mapy points player get
		for text_object in self.text_objects:
			text_object.update(game)

		if(not self.in_event):
			self.get_camera().update(game.get_map().get_player().rect)

		self.try_spawn_mobs(game)
		self.update_time(game)
		self.update_score_time()

	def render_map(self, game):
		game.screen.blit(self.sky, (0,0))

		for obj_group in (self.objs_bg, self.objs):
			for obj in obj_group:
				obj.render(game)

		for tube in self.tubes:
			tube.render(game)

	def render(self, game):
		game.screen.blit(self.sky, (0,0))

		for obj in self.objs_bg:
			obj.render(game)

		for mob in self.mobs:
			mob.render(game)

		for obj in self.objs:
			obj.render(game)

		for tube in self.tubes:
			tube.render(game)
		
		for whizbang in self.projectiles:
			whizbang.render(game)

		for debris in self.debris:
			debris.render(game)

		self.flag.render(game)

		for text_object in self.text_objects:
			text_object.render_in_game(game)

		self.get_player().render(game)
		self.get_ui().render(game)