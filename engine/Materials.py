import logging
import json
import os

from pyglet.graphics import TextureGroup
from pyglet import image

import Transform
import EngineConfig as EC
from Singleton import *

class Material(object):
    """ Contains matirial information
    
    """
    
    def __init__(self):
        self.name = ''
        self.texture = None
        self.sustain = 0
        self.textureGroup = None
        self.clipping = True


@Singleton
class MaterialFactory(object):

    def __init__(self):
        self.log = logging.getLogger('MaterialFactory')
        # get config object
        conf = EC.EngineConfig()
        self._materialPath = os.path.join(conf.getConfValue('baseDir'),'ressources/materials/')
        self._materials = {}
        self.loadMaterials()
        
    def getMaterial(self, name):
        self.log.debug(self._materials[name])
        return self._materials[name]
    
    def keys(self):
        return self._materials.keys()

    def loadMaterials(self):
        """ This method crawles the ressources for diffrent materials
            and loads them for future use
        """
        self.log.debug('loading materials from %s' % (self._materialPath, ))
        for file in os.listdir(self._materialPath):
            absPath = os.path.join(self._materialPath, file)
            
            """ if found new material, load metadata and textures """
            if os.path.isdir(absPath):
                self.log.debug('material found: %s' % (file, ))
                
                # load json material definition
                try:
                    defFile = open(os.path.join(absPath, "material.json"), 'r')
                    definition = "".join(defFile.readlines())
                    jsonObj = json.loads(definition)
                except Exception, e:
                    self.log.error("Error loading material metadata: %s" % (str(e), ))
                    
                # create new Material object
                self._materials[jsonObj['name']] = Material()
                    
                # load texture
                try:
                    self._materials[jsonObj['name']].name = jsonObj['name']
                    self._materials[jsonObj['name']].sustain = jsonObj['sustain']
                    self._materials[jsonObj['name']].clipping = jsonObj['clipping']
                    self._materials[jsonObj['name']].texture = Transform.Tools.tex_coords(
                        tuple(jsonObj['texture']['mapping']['top']),
                        tuple(jsonObj['texture']['mapping']['bottom']),
                        tuple(jsonObj['texture']['mapping']['sides']))
                    # A TextureGroup manages an OpenGL texture.
                    self._materials[jsonObj['name']].textureGroup = TextureGroup(
                        image.load(os.path.join(absPath,jsonObj['texture']['ressource'])).get_texture())
                    
                except Exception, e:
                    self.log.error("Error loading material textures: %s" % (str(e), ))
                    self.log.error(e)