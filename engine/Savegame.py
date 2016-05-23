import json
import gzip
import math
import os

import World
import Player
import Block
import Materials
import EngineConfig as EC
import logger as l

class Savegame(object):
    """ This class handles a savgame

    """
    NAME = "save.old.gz"

    @staticmethod
    def save(world, player):
        log = l.getLogger('savegame')
        log.debug('saving game ...')
        try:
            saveFile = gzip.open(os.path.join(
                EC.EngineConfig.Instance().getPath(), Savegame.NAME), 'w')
            log.debug('writing data')
            saveFile.write("%s\n" % (player.toJson(),))
            for coord in world.getBlockPositions():
                saveFile.write("%s\n" % (world.getBlock(coord).toJson(),))
            saveFile.close()
        except Exception, e:
            log.error('saving failed: %s' % (str(e),))

    @staticmethod
    def load(name="save.old.gz"):
        log = l.getLogger('load game')
        log.debug('loading game ...')
        world = World.World()
        player = Player.Player()
        try:
            saveFile = gzip.open(os.path.join(
                EC.EngineConfig.Instance().getPath(), Savegame.NAME), 'r')
            player.fromJson(saveFile.readline())
            for line in saveFile.readlines():
                tmp = Block.Block()
                try:
                    tmp.load(json.loads(line))
                    world.setBlock(tmp)
                except Exception as e:
                    log.error("Couldn't load block froms string: {}".format(line))
        except Exception, e:
            log.error('loading failed: %s' % (e,))
            return None

        return (world, player)
