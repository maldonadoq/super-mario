import pygame as pg

from pytmx.util_pygame import load_pygame

from .platform import Platform
from .camera import Camera
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

		self.map = 0
		self.sky = 0
		self.map_size = (0,0)		

		self.world_name = world_name
		self.load_world()

		self.in_event = False
		self.time = 400
		self.tick = 0

		self.camera = Camera(self.map_size[0]*32, 14)
		#self.event = Event()
	
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

	def reset(self, reset_all):
		self.objs = []
		self.objs_bg = []

		self.in_event = False
		self.sky = None
		self.map = None

		self.tick = 0
		self.time = 0

		self.map_size = (0, 0)
		self.load_world()

		self.get_event().reset()
		self.get_camera().reset()

	def get_camera(self):
		return self.camera

	def get_event(self):
		return self.event

	def update(self, game):
		self.get_event().update(game)