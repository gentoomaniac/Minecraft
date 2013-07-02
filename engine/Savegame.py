import json
import gzip
import math
import logging
import os

import World
import Player
import Block
import Materials
import EngineConfig as EC

class Savegame(object):
    """ This class handles a savgame
    
    """
    NAME = "save.gz"
   
    @staticmethod
    def save(world, player):
        log = logging.getLogger('save game')
        log.debug('saving game ...')
        try:
            saveFile = gzip.open(os.path.join(EC.EngineConfig.Instance().getPath(), Savegame.NAME), 'w')
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
        world = World.World()
        player = Player.Player()
        try:
            saveFile = gzip.open(os.path.join(EC.EngineConfig.Instance().getPath(), Savegame.NAME), 'r')
            player.fromJson(saveFile.readline())
            for line in saveFile.readlines():
                tmp = Block.Block()
                tmp.fromJson(line)
                world.setBlock(tmp)
        except Exception, e:
            log.error('loading failed: %s' % (e,))
            return None
            
        return (world, player)