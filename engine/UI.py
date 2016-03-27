import logging
import os

import pyglet
from pyglet.gl import *

import EngineConfig as EC
import TextureFactory as TF

class HUD(object):
    
    def __init__(self):
        self.log = logging.getLogger('HUD')
        #get config object
        self._conf = EC.EngineConfig.Instance()
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        self._hud_path = os.path.join(self._conf.getConfValue('baseDir'),
                'ressources/hud/')
        self._bar = pyglet.image.load(os.path.join(self._hud_path, 'bar.jpg'))
        self._bar_sprite = pyglet.sprite.Sprite(self._bar)
        self._bar_sprite.anchor_x = self._conf.getConfValue('screenWidth') // 2
        self._bar_sprite.anchor_y = self._bar_sprite.height // 2
        
    def draw(self):
        self._bar_sprite.draw()