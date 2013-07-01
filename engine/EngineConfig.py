import logging
import json
import math

from Singleton import *

@Singleton
class EngineConfig(object):
    """ This class handles the configuration of the game
    
    """
    
    # app information
    APP_NAME = u'PyCraft'
    APP_VERSION = u'0.1'
    
    CONFIG_PATH = 'ressources/engine.conf'
    
    def __init__(self):
        
        self.log = logging.getLogger('Config')
        self._path = '.'

        self._configSettings = {}
        self._configSettings['screenHeight'] = 600
        self._configSettings['screenWidth'] = 800
        self._configSettings['resizeable'] = True
        self._configSettings['walkingSpeed'] = 5
        self._configSettings['flyingSpeed'] = 10
        self._configSettings['gravity'] = 5
        self._configSettings['playerHight'] = 2
        self._configSettings['crouchHight'] = 1
        self._configSettings['maxJumHight'] = 1.0
        self._configSettings['velocity'] = 50
        self._configSettings['ticksPerSecond'] = 60
        self._configSettings['sectorSize'] = 16
        self._configSettings['baseDir'] = '~/Minecraft'
                
        # To derive the formula for calculating jump speed, first solve
        #    v_t = v_0 + a * t
        # for the time at which you achieve maximum height, where a is the acceleration
        # due to gravity and v_t = 0. This gives:
        #    t = - v_0 / a
        # Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
        #    s = s_0 + v_0 * t + (a * t^2) / 2
        self._configSettings['jumpSpeed'] = math.sqrt(2 * self._configSettings['gravity'] * 
                self._configSettings['maxJumHight'])
        
        

    def getConfValue(self, key):
        if key in self._configSettings.keys():
            return self._configSettings[key]
        else:
            raise Exception("Setting not found!")
         
    def setConfValue(self, key, val):
        self._configSettings[key] = val
         
    def setPath(self, path):
        self._path = path
         
    def getPath(self):
        return self._path
        
    def loadConfig(self):
        self.log.debug('loading config')
        try:
            content = open(EngineConfig.CONFIG_PATH, 'r').read()
            try:
                self.log.debug('parsing config')
                self._configSettings.update(json.loads(content))
                self.log.debug(json.dumps(self._configSettings))
            except Exception, e:
                self.log.error('Error parsing config: %s' % (str(e),))
        except Exception, e:
            self.log.error('Error loading config: %s' % (str(e),))
            #TODO: create empty config
        
        
    def saveConfig(self):
        try:
            conf = open(EngineConfig.CONFIG_PATH, 'w')
            conf.write(json.dumps(self._configSettings))
            conf.close()
            self.log.debug('config written in %s' % (EngineConfig.CONFIG_PATH,))
        except Exception, e:
            self.log.error('Error saving config: %s' % (str(e),))
