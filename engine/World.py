import json
import logging

from Block import *

class World(object):
    """ Representation of the World

    """

    def __init__(self):
        self.log = logging.getLogger("World")
        self._blocks = {}

    def addBlock(self, position, material):
        if position not in self._blocks:
            x, y, z = position
            isTopBlock = False if (x, y+1, z) in self._blocks else True
            
            self._blocks[position] = Block(position, material, isTop=isTopBlock)
            self._blocks[position].setVisible(True)
        else:
            raise Exception('Already a block at %s' % (position,))

    def getBlock(self, position):
        if position in self._blocks:
            return self._blocks[position]
        else:
            return None

    def setBlock(self, block):
        self._blocks[block.getPosition()] = block


    def removeBlock(self, position):
        if position in self._blocks:
            self._blocks[position].destroy()
            del self._blocks[position]
        else:
            raise Exception('No block at %s' % (position,))

    def existsBlockAt(self, position):
        if position in self._blocks:
            return True
        else:
            return False

    def getBlockCount(self):
        return len(self._blocks)

    def getBlockPositions(self):
        return self._blocks.keys()

    def toJson(self):
        data = {
            }
        return json.dumps(data)

    def fromJson(self, data):
        obj = json.loads(data)
