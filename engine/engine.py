import math

import pyglet
from pyglet.window import key, mouse
from pyglet.gl import *

import Transform
import Block
import Materials
import Savegame
import EngineConfig as EC
import Player
import Model
import UI
import logger as l


class Core(pyglet.window.Window):
    """ This is the graphics engine

    """

    def __init__(self, *args, **kwargs):
        self.log = l.getLogger("Core")
        # get config object
        self.conf = EC.EngineConfig.Instance()

        super(Core, self).__init__(width=self.conf.getConfValue('screenWidth'),
               height=self.conf.getConfValue('screenHeight'),
               caption="%s v%s" % (self.conf.APP_NAME, self.conf.APP_VERSION),
               resizable=self.conf.getConfValue('resizeable'))

        # Whether or not the window exclusively captures the mouse.
        self.exclusive = False

        # Strafing is moving lateral to the direction you are facing,
        # e.g. moving to the left or right while continuing to face forward.
        #
        # First element is -1 when moving forward, 1 when moving back, and 0
        # otherwise. The second element is -1 when moving left, 1 when moving
        # right, and 0 otherwise. Third element is 1 when flying up -1 when
        # flying down and 0 otherwise
        self.strafe = [0, 0, 0]

        # Which sector the player is currently in.
        self.sector = None

        # The crosshairs at the center of the screen.
        self.reticle = None

        # Velocity in the y (upward) direction.
        self.dy = 0

        # Convenience list of num keys.
        self.num_keys = [
            key._1, key._2, key._3, key._4, key._5,
            key._6, key._7, key._8, key._9, key._0]

        # Instance of the model that handles the world.
        self.model = Model.Model()

        # create the player
        if self.model.player is not None:
            self._player = self.model.player
        else:
            self._player = Player()

        self._materialFactory = Materials.MaterialFactory.Instance()

        # A list of blocks the player can place. Hit num keys to cycle.
        self._player.inventory = self._materialFactory.keys()

        # The current block the user can place. Hit num keys to cycle.
        self._selectedBlock = self._materialFactory.getMaterial(self._player.inventory[0])

        # The label that is displayed in the top left of the canvas.
        self.label = pyglet.text.Label('', font_name='Arial', font_size=18,
            x=10, y=self.height - 10, anchor_x='left', anchor_y='top',
            color=(0, 0, 0, 255))


        # position of block in focus to print in lable
        self.focusedBlock = tuple()
        
        self._hud = UI.HUD()

        # This call schedules the `update()` method to be called
        # TICKS_PER_SEC. This is the main game event loop.
        pyglet.clock.schedule_interval(self.update, 1.0 / self.conf.getConfValue('ticksPerSecond'))

    def set_exclusive_mouse(self, exclusive):
        """ If `exclusive` is True, the game will capture the mouse, if False
        the game will ignore the mouse.

        """
        super(Core, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def get_sight_vector(self):
        """ Returns the current line of sight vector indicating the direction
        the player is looking.

        """
        x, y = self._player.rotation
        # y ranges from -90 to 90, or -pi/2 to pi/2, so m ranges from 0 to 1 and
        # is 1 when looking ahead parallel to the ground and 0 when looking
        # straight up or down.
        m = math.cos(math.radians(y))
        # dy ranges from -1 to 1 and is -1 when looking straight down and 1 when
        # looking straight up.
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)

    def get_motion_vector(self):
        """ Returns the current motion vector indicating the velocity of the
        player.

        dy = Hight
        dx = Left (?)
        dz = Right (?)

        Returns
        -------
        vector : tuple of len 3
            Tuple containing the velocity in x, y, and z respectively.

        """

        # check if there is any movement
        if any(self.strafe):
            """ First element is rotation of the player in the x-z plane
                (ground plane) measured from the z-axis down. The second is
                the rotation angle from the ground plane up. Rotation is in
                degrees.

                The vertical plane rotation ranges from -90 (looking straight
                down) to 90 (looking straight up). The horizontal rotation
                range is unbounded.
            """
            x, y = self._player.rotation

            # get ground degrees.
            strafe = math.degrees(math.atan2(self.strafe[0], self.strafe[1]))

            # get Y angle from player
            y_angle = math.radians(y)
            # get radians for ground plane radians and add movement
            x_angle = math.radians(x + strafe)

            # if player is flying we need to move in 3 dimensions
            if self._player.flying:
                """ This if handles the straight up/down movement.
                 This is relative to the ground so we need to handle a movement
                 in the other dimensions seperately.
                 In this case let's assume a 45 degree movement otherwise 90
                 straight
                """
                if self.strafe[2] != 0:
                    """ if we have a 2 dimensional movement at the same time
                        we split the upwards movement into half.
                        Otherwise the projection to X/Z would be 0 so we the
                        movement in the first two dimensions would be 0.
                    """
                    if self.strafe[0] or self.strafe[1]:
                        y_angle = math.radians(45)
                    else:
                        y_angle = math.radians(90)

                m = math.cos(y_angle)
                dy = math.sin(y_angle)

                # if not explizitly moving up, use the normal behavior
                if self.strafe[0] > 0 and not self.strafe[2] or \
                        self.strafe[2] < 0:
                    # Moving backwards.
                    dy *= -1

                """ in case were only moving sidewards we need to reset dy and
                    m to not apply the normal view angle to the movement
                """
                if self.strafe[1] and not self.strafe[0] and not \
                        self.strafe[2]:
                    dy = 0.0
                    m = 1

                # When you are flying up or down, you have less left and right
                # motion.
                dx = math.cos(x_angle) * m
                dz = math.sin(x_angle) * m
            else:
                # no hight movement
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return (dx, dy, dz)

    def update(self, dt):
        """ This method is scheduled to be called repeatedly by the pyglet
        clock.

        Parameters
        ----------
        dt : float
            The change in time since the last call.

        """
        self.model.process_queue()
        sector = Transform.sectorize(self._player.position, self.conf.getConfValue('sectorSize'))
        if sector != self.sector:
            self.model.change_sectors(self.sector, sector)
            if self.sector is None:
                self.model.process_entire_queue()
            self.sector = sector
        m = 8
        dt = min(dt, 0.2)
        for _ in xrange(m):
            self._update(dt / m)

    def _update(self, dt):
        """ Private implementation of the `update()` method. This is where most
        of the motion logic lives, along with gravity and collision detection.

        Parameters
        ----------
        dt : float
            The change in time since the last call.

        """
        # walking
        speed = self.conf.getConfValue('flyingSpeed') if self._player.flying else self.conf.getConfValue('walkingSpeed')
        d = dt * speed # distance covered this tick.
        dx, dy, dz = self.get_motion_vector()
        # New position in space, before accounting for gravity.
        dx, dy, dz = dx * d, dy * d, dz * d
        # gravity
        if not self._player.flying:
            # Update your vertical speed: if you are falling, speed up until you
            # hit terminal velocity; if you are jumping, slow down until you
            # start falling.
            self.dy -= dt * self.conf.getConfValue('gravity')
            self.dy = max(self.dy, -self.conf.getConfValue('velocity'))
            dy += self.dy * dt
        # collisions
        x, y, z = self._player.position
        if self._player.isCrouch:
            x, y, z = self.collide((x + dx, y + dy, z + dz),
                self.conf.getConfValue('crouchHight'))
        else:
            x, y, z = self.collide((x + dx, y + dy, z + dz),
                self.conf.getConfValue('playerHight'))
        self._player.position = (x, y, z)

    def collide(self, position, height):
        """ Checks to see if the player at the given `position` and `height`
        is colliding with any blocks in the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check for collisions at.
        height : int or float
            The height of the player.

        Returns
        -------
        position : tuple of len 3
            The new position of the player taking into account collisions.

        """
        # How much overlap with a dimension of a surrounding block you need to
        # have to count as a collision. If 0, touching terrain at all counts as
        # a collision. If .49, you sink into the ground, as if walking through
        # tall grass. If >= .5, you'll fall through the ground.
        pad = 0.25
        p = list(position)
        np = Transform.normalize(position)
        for face in Block.FACES:  # check all surrounding blocks
            for i in xrange(3):  # check each dimension independently
                if not face[i]:
                    continue
                # How much overlap you have with this dimension.
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in xrange(height):  # check each height
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if not self.model.world.existsBlockAt(tuple(op)):
                        continue
                    # check for non resiting block (no colision)
                    if not self._materialFactory.getMaterial(
                            self.model.world.getBlock(tuple(op)).getMaterial()).clipping:
                        continue

                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        # You are colliding with the ground or ceiling, so stop
                        # falling / rising.
                        self.dy = 0
                    break
        return tuple(p)

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when a mouse button is pressed. See pyglet docs for button
        amd modifier mappings.

        Parameters
        ----------
        x, y : int
            The coordinates of the mouse click. Always center of the screen if
            the mouse is captured.
        button : int
            Number representing mouse button that was clicked. 1 = left button,
            4 = right button.
        modifiers : int
            Number representing any modifying keys that were pressed when the
            mouse button was clicked.

        """
        if self.exclusive:
            vector = self.get_sight_vector()
            block, previous = self.model.hit_test(self._player.position, vector)
            if (button == mouse.RIGHT) or \
                    ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
                # ON OSX, control + left click = right click.
                if previous:
                    self.model.add_block(previous, self._selectedBlock, immediate=True)
            elif button == pyglet.window.mouse.LEFT and block:
                self.model.remove_block(block, immediate=True)
        else:
            self.set_exclusive_mouse(True)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called when the player moves the mouse.

        Parameters
        ----------
        x, y : int
            The coordinates of the mouse click. Always center of the screen if
            the mouse is captured.
        dx, dy : float
            The movement of the mouse.

        """
        if self.exclusive:
            m = 0.15
            x, y = self._player.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self._player.rotation = (x, y)

    def on_key_press(self, symbol, modifiers):
        """ Called when the player presses a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.

        """

        if symbol == key.W:
            self.strafe[0] -= 1
        elif symbol == key.S:
            if modifiers & key.MOD_CTRL:
                Savegame.Savegame.save(self.model.world, self._player)
            else:
                self.strafe[0] += 1
        elif symbol == key.A:
            self.strafe[1] -= 1
        elif symbol == key.D:
            self.strafe[1] += 1
        elif symbol == key.C:
            if self._player.flying:
                self.strafe[2] -= 1
            elif modifiers & key.MOD_CTRL:
                self.conf.saveConfig()
            else:
                self._player.isCrouch = True
                pos = list(self._player.position)
                pos[1] -= self.conf.getConfValue('playerHight') - self.conf.getConfValue('crouchHight')
                self._player.position = tuple(pos)
        elif symbol == key.Q:
            self.conf.saveConfig()
                #pyglet.app.exit()
        elif symbol == key.SPACE:
            if self.dy == 0 and not self._player.flying:
                self.dy = self.conf.getConfValue('jumpSpeed')
            elif self._player.flying:
                self.strafe[2] += 1
        elif symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
        elif symbol == key.TAB:
            self._player.flying = not self._player.flying
        elif symbol in self.num_keys:
            index = (symbol - self.num_keys[0]) % len(self._player.inventory)
            # TODO: move selected block to player object
            self._selectedBlock = self._materialFactory.getMaterial(self._player.inventory[index])

    def on_key_release(self, symbol, modifiers):
        """ Called when the player releases a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.

        """
        if symbol == key.W:
            self.strafe[0] += 1
        elif symbol == key.S:
            if not modifiers & key.MOD_CTRL:
                self.strafe[0] -= 1
        elif symbol == key.A:
            self.strafe[1] += 1
        elif symbol == key.D:
            self.strafe[1] -= 1
        elif symbol == key.C:
            if self._player.flying:
                self.strafe[2] += 1
            elif not modifiers & key.MOD_CTRL:
                self._player.isCrouch = False
                pos = list(self._player.position)
                pos[1] += self.conf.getConfValue('playerHight') - self.conf.getConfValue('crouchHight')
                self._player.position = tuple(pos)
        elif symbol == key.SPACE:
            if self._player.flying:
                self.strafe[2] -= 1


    def on_resize(self, width, height):
        """ Called when the window is resized to a new `width` and `height`.

        """
        # label
        self.label.y = height - 10
        # reticle
        if self.reticle:
            self.reticle.delete()
        x, y = self.width / 2, self.height / 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )

    def set_2d(self):
        """ Configure OpenGL to draw in 2d.

        """
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_3d(self):
        """ Configure OpenGL to draw in 3d.

        """
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self._player.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self._player.position
        glTranslatef(-x, -y, -z)

    def on_draw(self):
        """ Called by pyglet to draw the canvas.

        """
        self.clear()
        self.set_3d()
        glColor3d(1, 1, 1)
        self.model.batch.draw()
        self.draw_focused_block()
        self.set_2d()
        self._hud.draw()
        self.draw_label()
        self.draw_reticle()

    def draw_focused_block(self):
        """ Draw black edges around the block that is currently under the
        crosshairs.

        """
        vector = self.get_sight_vector()
        block = self.model.hit_test(self._player.position, vector)[0]
        if block:
            x, y, z = block
            self.focusedBlock = block
            vertex_data = Transform.cube_vertices(x, y, z, 0.51)
            glColor3d(0, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def draw_label(self):
        """ Draw the label in the top left of the screen.

        """
        try:
            x, y, z = self._player.position
            if self.model.world.getBlock(self.focusedBlock) is not None:
                self.label.text = '%02d (%.2f, %.2f, %.2f) %d / %d -- focus: %s - %s - %i' % (
                    pyglet.clock.get_fps(), x, y, z,
                    len(self.model.visibleWorld), self.model.world.getBlockCount(),
                    self.focusedBlock, self.model.world.getBlock(self.focusedBlock).getMaterial(),
                    self.model.world.getBlock(self.focusedBlock).getLife())
            else:
                self.label.text = '%02d (%.2f, %.2f, %.2f) %d / %d' % (
                    pyglet.clock.get_fps(), x, y, z,
                    len(self.model.visibleWorld), self.model.world.getBlockCount())
        except Exception, e:
            self.label.text = str(e)
        self.label.draw()

    def draw_reticle(self):
        """ Draw the crosshairs in the center of the screen.

        """
        glColor3d(255, 0, 0)
        self.reticle.draw(GL_LINES)

    def setup_fog(self):
        """ Configure the OpenGL fog properties.

        """
        # Enable fog. Fog "blends a fog color with each rasterized pixel fragment's
        # post-texturing color."
        glEnable(GL_FOG)
        # Set the fog color.
        glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
        # Say we have no preference between rendering speed and quality.
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        # Specify the equation used to compute the blending factor.
        glFogi(GL_FOG_MODE, GL_LINEAR)
        # How close and far away fog starts and ends. The closer the start and end,
        # the denser the fog in the fog range.
        glFogf(GL_FOG_START, 20.0)
        glFogf(GL_FOG_END, 60.0)


    def setup(self):
        """ Basic OpenGL configuration.

        """
        # Set the color of "clear", i.e. the sky, in rgba.
        glClearColor(0.5, 0.69, 1.0, 1)
        ## We need to enable this again as we now have partly transparent blocks
        # Enable culling (not rendering) of back-facing facets -- facets that aren't
        # visible to you.
        glEnable(GL_CULL_FACE)

        self.setup_fog()
        pyglet.app.run()
