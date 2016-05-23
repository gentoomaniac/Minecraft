import json

import Materials

class Block(object):
    """ will hold a block object

    """

    def __init__(self, position=None, material=None, isTop=True):
        # pyglet `VertextList` for shown blocks
        self._vertex = None
        self._position = position
        self._material = material
        self._life = None
        self._isTop = isTop
        if material:
            self._life = material.sustain


    def destroy(self):
        if self._vertex:
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
        if self._isTop:
            return self._material.texture['top']
        else:
            return self._material.texture['middle']

    def getVertex(self):
        return self._vertex

    def setVertex(self, vertex):
        self._vertex = vertex

    def getMaterial(self):
        return self._material

    def getPosition(self):
        return self._position


    def isTop(self):
        return self._isTop
    
    def setTop(self, isTop):
        self._isTop = isTop


    def getMaterial(self):
        return self._material.name

    def toJson(self):
        out = {
            'position': self._position,
            'material': self._material.name,
            'life': self._life,
            'isTop': self._isTop,
            }
        return json.dumps(out)

    def load(self, data):
        materialFactory = Materials.MaterialFactory.Instance()

        self._position = tuple(data['position'])
        self._material = materialFactory.getMaterial(data['material'])
        self._isTop = data['isTop']
        self._life = data['life']


FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]
