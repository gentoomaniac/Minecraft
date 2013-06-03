class Block:
    """ will hold a block object

    """

    def __init__(self, position, material):
        self.x, self.y, self.z = position
        self.material = material
        self.life = material.sustain
        self.isVisible = True
        # pyglet `VertextList` for shown blocks
        self.vertex = None
        
        
class Material:
    """ Contains matirial information
    
    """
    
    def __init__(self, name, texture, sustain=0):
        self.name = name
        self.texture = texture
        self.sustain = sustain