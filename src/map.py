import pygame as pg

from pytmx.util_pygame import load_pygame

from .platform import Platform
from .camera import Camera
from .event import Event
from .game_ui import GameUI
from .player import Player
from .flag import Flag
from .tube import Tube
from .text import Text
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

		#self.mobs.append()
		
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

		self.in_event = False
		self.flag = None
		self.sky = None
		self.map = None

		self.tick = 0
		self.time = 400

		self.map_size = (0, 0)
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
				self.map[i][j] = Platform(x*32, y*32, image=None, type_id=0)

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

	def remove_text(self, text_object):
		self.text_objects.remove(text_object)

	def update_player(self, game):
		self.get_player().update(game)

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
				self.score_for_killing_mob // 2

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

		for text_object in self.text_objects:
			text_object.update(game)

		if(not self.in_event):
			self.get_camera().update(game.get_map().get_player().rect)

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

		for obj in self.objs:
			obj.render(game)

		for tube in self.tubes:
			tube.render(game)
		
		self.flag.render(game)
		self.get_player().render(game)
		#self.get_ui().render(game)