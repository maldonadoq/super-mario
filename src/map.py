import pygame as pg

from pytmx.util_pygame import load_pygame

from .camera import Camera
from .values import wwidth, wheight

class Map:
	def __init__(self, world_name):
		self.map = None
		self.sky = None
		self.map_size = (0,0)		

		self.world_name = world_name
		self.load_world()

		self.in_even = False
		self.time = 400
		self.tick = 0

		self.camera = Camera(self.map_size[0]*32, 14)
	
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
									tmx.get_tile_image(0, 15, layer_num)
									tmx.get_tile_image(1, 15, layer_num)
									tmx.get_tile_image(2, 15, layer_num)
								)							
							print('Fore', tile_id)

						elif(layer.name == 'Background'):
							print('Back', tile_id)

			layer_num += 1

	def reset(self, reset_all):