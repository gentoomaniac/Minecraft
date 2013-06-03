from objects import *
class World(object):
    """ Representation of the World
    
    """
    
    def __init__(self):
        self._blocks = {}
        
    def addBlock(self, position, material):
        if position not in self._blocks:
            print "adding block at %s" % (position,)
            self._blocks[position] = Block(position, material)
        else:
            print "Total number of blocks %i" % (len(self._blocks),)
            raise Exception('Already a block at %s' % (position,))

    def getBlock(self, position):
        if position in self._blocks:
            return self._blocks[position]
        else:
            return None

    def removeBlock(self, position):
        if position in self._blocks:
            self._blocks[position].delete()
        else:
            raise Exception('No block at %s' % (position,))
        
    def existsBlockAt(self, position):
        if position in self._blocks:
            return True
        else:
            return False