import logging
import time

import pyglet
from pyglet.graphics import TextureGroup
from pyglet import image
from collections import deque
from pyglet.gl import *

import Savegame
import Transform
import Block
import World
import EngineConfig as EC
import Materials

TEXTURE_PATH = 'ressources/texture.png'

class Model(object):

    def __init__(self):
        
        self.log = logging.getLogger("Model")
        
        self.conf = EC.EngineConfig()

        # A Batch is a collection of vertex lists for batched rendering.
        self.batch = pyglet.graphics.Batch()

        # Mapping from sector to a list of positions inside that sector.
        self.sectors = {}

        # Simple function queue implementation. The queue is populated with
        # _show_block() and _hide_block() calls
        self.queue = deque()

        self._materialFactory = Materials.MaterialFactory.Instance()
        
        # all shown blocks.
        self.visibleWorld = {}
        
        # This defines all the blocks that are currently in the world.
        (self.world, self.player) = Savegame.Savegame.load()
        if self.world is None:
            self.log.debug("Couldn't load a savegame. Creating new world ...")
            self.world = World.World()
            self.visibleWorld = {}
            self._initialize()
        else:
            # make blocks visible after loading
            for position in self.world.getBlockPositions():
                # sectorize blocks
                self.sectors.setdefault(Transform.Tools.sectorize(position, self.conf.getConfValue('sectorSize')), []).append(position)
                if self.world.getBlock(position).isVisible():
                    self.show_block(position)


    def _initialize(self):
        """ Initialize the world by placing all the blocks.

        """
        self.log.debug("Initializing level...")
        n = 80  # 1/2 width and height of world
        s = 1  # step size
        y = 0  # initial y height
        
        # create an n x n sized plane with two layers
        for x in xrange(-n, n + 1, s):
            for z in xrange(-n, n + 1, s):
                # create a layer stone an grass everywhere.
                self.add_block((x, y - 2, z), materials['Grass'])
                self.add_block((x, y - 3, z), materials['Stone'])
                if x in (-n, n) or z in (-n, n):
                    # create outer walls.
                    for dy in xrange(-1, 3):
                        self.add_block((x, y + dy, z), materials['Stone'])

        # generate the hills randomly
        #o = n - 10
        #for _ in xrange(120):
            #a = random.randint(-o, o)  # x position of the hill
            #b = random.randint(-o, o)  # z position of the hill
            #c = -1  # base of the hill
            #h = random.randint(1, 6)  # height of the hill
            #s = random.randint(4, 8)  # 2 * s is the side length of the hill
            #d = 1  # how quickly to taper off the hills
            #mat = random.choice(materials.keys())
            #for y in xrange(c, c + h):
                #for x in xrange(a - s, a + s + 1):
                    #for z in xrange(b - s, b + s + 1):
                        #if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                            #continue
                        #if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                            #continue
                        #if not self.world.existsBlockAt((x, y, z)):
                            #self.add_block((x, y, z), materials[mat])
                #s -= d  # decrement side lenth so hills taper off

    def hit_test(self, position, vector, max_distance=8):
        """ Line of sight search from current position. If a block is
        intersected it is returned, along with the block previously in the line
        of sight. If no block is found, return None, None.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check visibility from.
        vector : tuple of len 3
            The line of sight vector.
        max_distance : int
            How many blocks away to search for a hit.

        """
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in xrange(max_distance * m):
            key = Transform.Tools.normalize((x, y, z))
            if key != previous and self.world.existsBlockAt(key):
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None

    def exposed(self, position):
        """ Returns False is given `position` is surrounded on all 6 sides by
        blocks, True otherwise.

        """
        x, y, z = position
        for dx, dy, dz in Block.FACES:
            if not self.world.existsBlockAt((x + dx, y + dy, z + dz)):
                return True
        return False

    def add_block(self, position, material, immediate=True):
        """ Add a block with the given `texture` and `position` to the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to add.
        texture : list of len 3
            The coordinates of the texture squares. Use `tex_coords()` to
            generate.
        immediate : bool
            Whether or not to draw the block immediately.

        """
        if self.world.existsBlockAt(position):
            self.remove_block(position, immediate)
        self.world.addBlock(position, material)
        self.sectors.setdefault(Transform.Tools.sectorize(position, self.conf.getConfValue('sectorSize')), []).append(position)
        if immediate:
            if self.exposed(position):
                self.show_block(position)
            self.check_neighbors(position)


    def remove_block(self, position, immediate=True):
        """ Remove the block at the given `position`.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to remove.
        immediate : bool
            Whether or not to immediately remove block from canvas.

        """
        if self.world.getBlock(position).isAlive():
            self.world.getBlock(position).decreaseLife()
        else:
            if immediate:
                if self.world.existsBlockAt(position):
                    self.hide_block(position)
                    
                self.check_neighbors(position)
            self.world.removeBlock(position)
            self.sectors[Transform.Tools.sectorize(position, self.conf.getConfValue('sectorSize'))].remove(position)


    def check_neighbors(self, position):
        """ Check all blocks surrounding `position` and ensure their visual
        state is current. This means hiding blocks that are not exposed and
        ensuring that all exposed blocks are shown. Usually used after a block
        is added or removed.

        """
        x, y, z = position
        for dx, dy, dz in Block.FACES:
            key = (x + dx, y + dy, z + dz)
            if not self.world.existsBlockAt(key):
                continue
            if self.exposed(key):
                if not self.world.existsBlockAt(key):
                    self.show_block(key)
            else:
                if self.world.existsBlockAt(key):
                    self.hide_block(key)


    def show_block(self, position, immediate=True):
        """ Show the block at the given `position`. This method assumes the
        block has already been added with add_block()

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to show.
        immediate : bool
            Whether or not to show the block immediately.

        """
        if immediate:
            self._show_block(position)
        else:
            self._enqueue(self._show_block, position)


    def _show_block(self, position):
        """ Private implementation of the `show_block()` method.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to show.
        texture : list of len 3
            The coordinates of the texture squares. Use `tex_coords()` to
            generate.

        """
        x, y, z = position
        try:
            block = self.world.getBlock(position)
            vertex_data = Transform.Tools.cube_vertices(x, y, z, 0.5)
            texture_data = list(block.getTexture())
            self.log.debug(block.getMaterial())
            # create vertex list
            # FIXME Maybe `add_indexed()` should be used instead
            block.setVisible(True)
            block.setVertex(self.batch.add(24, GL_QUADS, self._materialFactory.getMaterial(block.getMaterial()).textureGroup,
                ('v3f/static', vertex_data),
                ('t2f/static', texture_data)))
        except Exception, e:
            self.log.error("Showing block at %s failed: %s" % (position, e))


    def hide_block(self, position, immediate=True):
        """ Hide the block at the given `position`. Hiding does not remove the
        block from the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to hide.
        immediate : bool
            Whether or not to immediately remove the block from the canvas.

        """
        #self.world.visible.pop(position)
        if immediate:
            self._hide_block(position)
        else:
            self._enqueue(self._hide_block, position)


    def _hide_block(self, position):
        """ Private implementation of the 'hide_block()` method.

        """
        try:
            block = self.world.getBlock(position)
            block.setVisible(False)
            vertex = block.getVertex()
            del vertex
        except Exception, e:
            self.log.error("Hiding block at %s failed: %s" % (position,e))

    def show_sector(self, sector):
        """ Ensure all blocks in the given sector that should be shown are
        drawn to the canvas.

        """
        for position in self.sectors.get(sector, []):
            if not self.world.existsBlockAt(position) and self.exposed(position):
                self.show_block(position, False)
                                
                                
    def hide_sector(self, sector):
        """ Ensure all blocks in the given sector that should be hidden are
        removed from the canvas.

        """
        for position in self.sectors.get(sector, []):
            if self.world.existsBlockAt(position):
                self.hide_block(position, True)

    def change_sectors(self, before, after):
        """ Move from sector `before` to sector `after`. A sector is a
        contiguous x, y sub-region of world. Sectors are used to speed up
        world rendering.

        """
        self.log.debug("Sector switch from %s to %s" % (before, after))
        before_set = set()
        after_set = set()
        # probaby # of sectors to show
        pad = 4
        for dx in xrange(-pad, pad + 1):
            for dy in xrange(-pad, pad + 1):
                for dz in xrange(-pad, pad + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
                        continue
                    if before:
                        x, y, z = before
                        before_set.add((x + dx, y + dy, z + dz))
                    if after:
                        x, y, z = after
                        after_set.add((x + dx, y + dy, z + dz))
        show = after_set - before_set
        hide = before_set - after_set
        for sector in show:
            self.show_sector(sector)
        for sector in hide:
            self.hide_sector(sector)

    def _enqueue(self, func, *args):
        """ Add `func` to the internal queue.

        """
        self.queue.append((func, args))

    def _dequeue(self):
        """ Pop the top function from the internal queue and call it.

        """
        func, args = self.queue.popleft()
        func(*args)

    def process_queue(self):
        """ Process the entire queue while taking periodic breaks. This allows
        the game loop to run smoothly. The queue contains calls to
        _show_block() and _hide_block() so this method should be called if
        add_block() or remove_block() was called with immediate=False

        """
        start = time.clock()
        while self.queue and time.clock() - start < 1.0 / TICKS_PER_SEC:
            self._dequeue()


    def process_entire_queue(self):
        """ Process the entire queue with no breaks.

        """ 
        while self.queue:
            self._dequeue()
