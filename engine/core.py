    
import json
import gzip
import math
from logger import *


from world import *
from player import *
from objects import *
from materials import *

class EngineConfig(object):
    """ This class handles the configuration of the game
    
    """
    
    # app information
    APP_NAME = u'PyCraft'
    APP_VERSION = u'0.1'
    
    CONFIG_PATH = 'ressources/engine.conf'
    
    def __new__(type, *args):
        log = logging.getLogger('Config')
        # Singelton Part: if there is now instance create one and save it to _the_instance.
        # If already existing, just return a reference to the instance.
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        log.debug("Conf object: %s" % (type._the_instance,))
        return type._the_instance
    
    def __init__(self):
        
        self.log = logging.getLogger('Config')
        self._path = '.'

        self.configSettings = {}
        self.configSettings['screenHeight'] = 600
        self.configSettings['screenWidth'] = 800
        self.configSettings['resizeable'] = True
        self.configSettings['walkingSpeed'] = 5
        self.configSettings['flyingSpeed'] = 10
        self.configSettings['gravity'] = 5
        self.configSettings['playerHight'] = 2
        self.configSettings['crouchHight'] = 1
        self.configSettings['maxJumHight'] = 1.0
        self.configSettings['velocity'] = 50
        self.configSettings['ticksPerSecond'] = 60
        self.configSettings['sectorSize'] = 16
        self.configSettings['texturePath'] = 'ressources/texture.png'
                
        # To derive the formula for calculating jump speed, first solve
        #    v_t = v_0 + a * t
        # for the time at which you achieve maximum height, where a is the acceleration
        # due to gravity and v_t = 0. This gives:
        #    t = - v_0 / a
        # Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
        #    s = s_0 + v_0 * t + (a * t^2) / 2
        self.configSettings['jumpSpeed'] = math.sqrt(2 * self.configSettings['gravity'] * 
                self.configSettings['maxJumHight'])
        
        

    def getConfValue(self, key):
        if key in self.configSettings.keys():
             return self.configSettings[key]
        else:
             raise Exception("Setting not found!")
         
    def setConfValue(self, key, val):
        self.configSettings[key] = val
         
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
                self.configSettings = {}
                self.configSettings = json.loads(content)
                self.log.debug(json.dumps(self.configSettings))
            except Exception, e:
                self.log.error('Error parsing config: %s' % (str(e),))
        except Exception, e:
            self.log.error('Error loading config: %s' % (str(e),))
            #TODO: create empty config
        
        
    def saveConfig(self):
        try:
            conf = open(EngineConfig.CONFIG_PATH, 'w')
            conf.write(json.dumps(self.configSettings))
            conf.close()
            self.log.debug('config written in %s' % (EngineConfig.CONFIG_PATH,))
        except Exception, e:
            self.log.error('Error saving config: %s' % (str(e),))


class Savegame(object):
    """ This class handles a savgame
    
    """
    NAME = "save.gz"
   
    @staticmethod
    def save(world, player):
        log = logging.getLogger('save game')
        log.debug('saving game ...')
        try:
            saveFile = gzip.open("%s/%s" % (EngineConfig().getPath(),Savegame.NAME), 'w')
            log.debug('writing data')
            saveFile.write("%s\n" % (player.toJson(),))
            for coord in world.getBlockPositions():
                saveFile.write("%s\n" % (world.getBlock(coord).toJson(),))
            saveFile.close()
        except Exception, e:
            log.error('saving failed: %s' % (str(e),))
    
    @staticmethod
    def load(name="save.gz"):
        log = logging.getLogger('load game')
        log.debug('loading game ...')
        world = World()
        player = Player()
        try:
            saveFile = gzip.open("%s/%s" % (EngineConfig().getPath(),Savegame.NAME), 'r')
            player.fromJson(saveFile.readline())
            for line in saveFile.readlines():
                tmp = Block()
                tmp.fromJson(line)
                world.setBlock(tmp)
        except Exception, e:
            log.error('loading failed: %s' % (e,))
            return None
            
        return (world, player)