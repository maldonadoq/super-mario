import pygame as pg

class Sounds:
	def __init__(self):
		self.sounds = {}
		self.load_sounds()

	def load_sounds(self):
		self.sounds['overworld']        = pg.mixer.Sound('sounds/overworld.wav')
		self.sounds['overworld_fast']   = pg.mixer.Sound('sounds/overworld_fast.wav')
		self.sounds['level_end']        = pg.mixer.Sound('sounds/level_end.wav')
		self.sounds['coin']             = pg.mixer.Sound('sounds/coin.wav')
		self.sounds['small_mario_jump'] = pg.mixer.Sound('sounds/small_mario_jump.wav')
		self.sounds['big_mario_jump']   = pg.mixer.Sound('sounds/big_mario_jump.wav')
		self.sounds['brick_break'] 		= pg.mixer.Sound('sounds/brick_break.wav')
		self.sounds['block_hit'] 		= pg.mixer.Sound('sounds/block_hit.wav')
		self.sounds['mushroom_appear'] 	= pg.mixer.Sound('sounds/mushroom_appear.wav')
		self.sounds['mushroom_eat'] 	= pg.mixer.Sound('sounds/mushroom_eat.wav')
		self.sounds['death'] 			= pg.mixer.Sound('sounds/death.wav')
		self.sounds['pipe'] 			= pg.mixer.Sound('sounds/pipe.wav')
		self.sounds['kill_mob']			= pg.mixer.Sound('sounds/kill_mob.wav')
		self.sounds['game_over'] 		= pg.mixer.Sound('sounds/game_over.wav')
		self.sounds['scorering'] 		= pg.mixer.Sound('sounds/scorering.wav')
		self.sounds['fireball'] 		= pg.mixer.Sound('sounds/fireball.wav')
		self.sounds['shot'] 			= pg.mixer.Sound('sounds/shot.wav')

	def play(self, name, loops, volume):
		self.sounds[name].play(loops=loops)
		self.sounds[name].set_volume(volume)

	def stop(self, name):
		self.sounds[name].stop()
		
	def start_fast_music(self, core):
		if core.world.get_name() == 'one':
			self.stop('overworld')
			self.play('overworld_fast', 99999, 0.5)