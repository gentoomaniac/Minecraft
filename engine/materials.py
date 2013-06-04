from transform import *
class Material(object):
    """ Contains matirial information
    
    """
    
    def __init__(self, name, texture, sustain=0):
        self.name = name
        self.texture = texture
        self.sustain = sustain

materials = {
    'GRASS': Material("Grass", Tools.tex_coords((1, 0), (0, 1), (0, 0)), 1), 
    'SAND': Material("Sand", Tools.tex_coords((1, 1), (1, 1), (1, 1)), 0),
    'BRICK': Material("Brick", Tools.tex_coords((2, 0), (2, 0), (2, 0)), 2),
    'STONE': Material("Stone",Tools.tex_coords((2, 1), (2, 1), (2, 1)), 5)
}