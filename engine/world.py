from objects import *
class World(object):
    """ Representation of the World
    
    """
    
    def __init__(self):
        self._blocks = {}
        # PLAYER position
        self.position = (0, 0, 0)
        
    def addBlock(self, position, material):
        if position not in self._blocks:
            self._blocks[position] = Block(position, material)
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
            'position': list(self.position)
            }
        return json.dumps(data)
    
    def fromJson(self, data):
        obj = json.loads(data)
        self.position = tuple(obj['position'])