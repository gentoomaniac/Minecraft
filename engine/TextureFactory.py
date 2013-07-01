import logging

from pyglet.graphics import TextureGroup
from pyglet import image
from pyglet.gl import *

from Singleton import *

@Singleton
class TextureFactory():

    """ This class handles texture loading etc
    """
    
    def __init__(self):
        self.log = logging.getLogger('TextureFactory')
        self._textures = {}
        self.log.debug("TextureFactory initialised")
        self.glSetup()
        
    def glSetup(self):
        # Set the texture minification/magnification function to GL_NEAREST (nearest
        # in Manhattan distance) to the specified texture coordinates. GL_NEAREST
        # "is generally faster than GL_LINEAR, but it can produce textured images
        # with sharper edges because the transition between texture elements is not
        # as smooth."
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        
        # Transparency for textures
        glEnable(GL_BLEND) 
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 
        

    def loadTexture(self, path):
        """ This function loads textures if necessary and returns them as a object
        """
        if not path in self._textures:
            self.log.debug("Loading texture: %s" % (path, ))
            try:
                self._textures[path] = TextureGroup(image.load(path).get_texture())
            except Exception, e:
                self.log.error(e)
        return self._textures[path]