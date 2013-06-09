import json
from materials import *

class Block(object):
    """ will hold a block object

    """

    def __init__(self, position=None, material=None):
        self._isVisible = False
        # pyglet `VertextList` for shown blocks
        self._vertex = None
        self._position = None
        self._material = None
        self._life = None

        if position is not None and material is not None:
            self._position = position
            self._material = material
            self._life = material.sustain

        
    def destroy(self):
        if self._vertex is not None:
            self._vertex.delete()
        
    def decreaseLife(self, step=1):
        self._life -= step
        
    def isAlive(self):
        if self._life > 0:
            return True
        else:
            return False
        
    def getLife(self):
        return self._life

    def getTexture(self):
        return self._material.texture
    
    def getVertex(self):
        return self._vertex
    
    def setVertex(self, vertex):
        self._vertex = vertex
        
    def deleteVertex(self):
        del self._vertex
        
    def getPosition(self):
        return self._position
    
    def isVisible(self):
        return self._isVisible
    
    def setVisible(self, visible):
        self._isVisible = visible
        
    def getMaterial(self):
        return self._material.name
    
    def toJson(self):
        out = {
            'position': self._position,
            'material': self._material.name,
            'life': self._life,
            'visible': self._isVisible
            }
        return json.dumps(out)
    
    def fromJson(self, data):
        obj = json.loads(data)
        self._position = tuple(obj['position'])
        self._material = materials[obj['material']]
        self._life = obj['life']
        self._isVisible = obj['visible']