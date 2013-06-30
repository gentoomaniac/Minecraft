import logging
import json
import os

import Transform
import EngineConfig as EC

class Material(object):
    """ Contains matirial information
    
    """
    
    def __init__(self, name, texture, sustain=0):
        self.name = name
        self.texture = texture
        self.sustain = sustain

class MaterialFactory(object):

    def __new__(type, *args):
        log = logging.getLogger('MaterialFactory')
        # Singelton Part: if there is no instance create one and save it to _the_instance.
        # If already existing, just return a reference to the instance.
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        log.debug("MaterialFactory object: %s" % (type._the_instance,))
        return type._the_instance

    def __init__(self):
        self.log = logging.getLogger('MaterialFactory')
        # get config object
        conf = EC.EngineConfig()
        self._materialPath = os.path.join(conf.getConfValue('baseDir'),'ressources/materials/')
        self._materials = {}
        self.loadMaterials()

    def loadMaterials(self):
        self.log.debug('loading materials from %s' % (self._materialPath, ))
        for file in os.listdir(self._materialPath):
            absPath = os.path.join(self._materialPath, file)
            if os.path.isdir(absPath):
                try:
                    defFile = open(os.path.join(absPath, "material.json"), 'r')
                    definition = "".join(defFile.readlines())
                    jsonObj = json.loads(definition)
                    self._materials[jsonObj['name']] = jsonObj
                except Exception, e:
                    self.log.error(str(e))
                    
                self._materials[file] = 'file'
                self.log.debug('material found: %s' % (file, ))


materials = {
    'Grass': Material("Grass", Transform.Tools.tex_coords((1, 0), (0, 1), (0, 0)), 1), 
    'Sand': Material("Sand", Transform.Tools.tex_coords((1, 1), (1, 1), (1, 1)), 0),
    'Brick': Material("Brick", Transform.Tools.tex_coords((2, 0), (2, 0), (2, 0)), 2),
    'Stone': Material("Stone",Transform.Tools.tex_coords((2, 1), (2, 1), (2, 1)), 4)
}