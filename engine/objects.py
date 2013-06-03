class Block:
    """ will hold a block object

    """

    def __init__(self, position, material):
        self.x, self.y, self.z = position
        self.material = material
        self._life = material.sustain
        self.isVisible = True
        # pyglet `VertextList` for shown blocks
        self.vertex = None
        
    def decreaseLife(self, step=1):
        self._life -= step
        
    def isAlive(self):
        if self._life > 0:
            return True
        else:
            return False
