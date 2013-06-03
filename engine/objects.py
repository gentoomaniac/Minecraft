class Block:
    """ will hold a block object

    """

    def __init__(self, position, material):
        self._position = position
        self._material = material
        self._life = material.sustain
        self.isVisible = True
        # pyglet `VertextList` for shown blocks
        self._vertex = None
        
    def decreaseLife(self, step=1):
        self._life -= step
        
    def isAlive(self):
        if self._life > 0:
            return True
        else:
            return False

    def getTexture(self):
        return self._material.texture
    
    def getVertex(self):
        return self._vertex
    
    def setVertex(self, vertex):
        self._vertex = vertex
        
    def getPosition(self):
        return self._position