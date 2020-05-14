import pygame as pg

class Sounds:
    def __init__(self):
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        self.sounds['overworld'] = pg.mixer.Sound('sounds/overworld.wav')
        self.sounds['overworld_fast'] = pg.mixer.Sound('sounds/overworld-fast.wav')
        self.sounds['level_end'] = pg.mixer.Sound('sounds/')
        self.sounds['coin'] = pg.mixer.Sound('sounds/')
        self.sounds['small_mario_jump'] = pg.mixer.Sound('sounds/')
        self.sounds['big_mario_jump'] = pg.mixer.Sound('sounds/')
        self.sounds['brick_break'] = pg.mixer.Sound('sounds/')
        self.sounds[''] = pg.mixer.Sound('sounds/')
        self.sounds[''] = pg.mixer.Sound('sounds/')
        self.sounds[''] = pg.mixer.Sound('sounds/')
        self.sounds[''] = pg.mixer.Sound('sounds/')
        self.sounds[''] = pg.mixer.Sound('sounds/')
        self.sounds[''] = pg.mixer.Sound('sounds/')
        self.sounds[''] = pg.mixer.Sound('sounds/')
        self.sounds[''] = pg.mixer.Sound('sounds/')
        self.sounds[''] = pg.mixer.Sound('sounds/')
