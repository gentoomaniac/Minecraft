import logging
import json
import os

import Transform
import EngineConfig as EC
import TextureFactory as TF
from Singleton import *

class Material(object):
    """ Contains matirial information

    """

    def __init__(self):
        self.name = ''
        self.texture = {}
        self.sustain = 0
        self.textureGroup = None
        self.clipping = True


@Singleton
class MaterialFactory(object):

    def __init__(self):
        self.log = logging.getLogger('MaterialFactory')
        # get config object
        conf = EC.EngineConfig.Instance()
        self._materialPath = os.path.join(conf.getConfValue('baseDir'),
                'ressources/materials/')
        self._materials = {}
        self.loadMaterials()

    def getMaterial(self, name):
        return self._materials[name]

    def keys(self):
        return self._materials.keys()

    def loadMaterials(self):
        """ This method crawles the ressources for diffrent materials
            and loads them for future use
        """
        self.log.debug('loading materials from %s' % (self._materialPath, ))

        textureFactory = TF.TextureFactory.Instance()

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
                    self.log.error("Error loading material metadata %s: %s" %
                            (file, str(e)))

                # create new Material object
                self._materials[jsonObj['name']] = Material()

                # load texture
                try:
                    self._materials[jsonObj['name']].name = jsonObj['name']
                    self._materials[jsonObj['name']].sustain = int(jsonObj['sustain'])
                    self._materials[jsonObj['name']].clipping = bool(jsonObj['clipping'])
                    self._materials[jsonObj['name']].texture['top'] = Transform.tex_coords(
                        tuple(jsonObj['texture']['mapping']['top']['top']),
                        tuple(jsonObj['texture']['mapping']['top']['bottom']),
                        tuple(jsonObj['texture']['mapping']['top']['sides']))
                    self._materials[jsonObj['name']].texture['middle'] = Transform.tex_coords(
                        tuple(jsonObj['texture']['mapping']['middle']['top']),
                        tuple(jsonObj['texture']['mapping']['middle']['bottom']),
                        tuple(jsonObj['texture']['mapping']['middle']['sides']))
                    # A TextureGroup manages an OpenGL texture.
                    self._materials[jsonObj['name']].textureGroup = textureFactory.loadTexture(
                        os.path.join(absPath,jsonObj['texture']['ressource']))

                except Exception, e:
                    self.log.debug("Error loading material textures: %s" % (str(e), ))
