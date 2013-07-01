import json
import logging

import Materials

class Block(object):
    """ will hold a block object

    """

    def __init__(self, position=None, material=None):
        self.log = logging.getLogger("Block")
    
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
        try:
            self._life -= step
        except TypeError, e:
            self.log.debug("%s - type: %s" % (str(e), type(self._life)))
        
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
    
    def getMaterial(self):
        return self._material
    
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
        materialFactory = Materials.MaterialFactory.Instance()
        obj = json.loads(data)
        self._position = tuple(obj['position'])
        self._material = materialFactory.getMaterial(obj['material'])
        self._life = obj['life']
        self._isVisible = True #obj['visible']


FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]