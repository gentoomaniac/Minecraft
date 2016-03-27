#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Usage:
        main.py [options]

    Options:
        --version           show version number
        -h, --help          show this help message and exit
        -d, --debug         enable debug logging
        --level=savegame    load the specified savegame
"""

import logging
import os
from docopt import docopt

import engine.EngineConfig as EC
import engine.engine as Engine
import logger as l

def main():
    """ prepare logging object
    """
    # logging.basicConfig(level=logging.DEBUG,
    #                 format='%(asctime)s %(levelname)s\t%(name)s\t: %(message)s',
    #                 datefmt='%a, %d %b %Y %H:%M:%S',
    #                 filename='debug.log')
    log = l.getLogger('main')

    log.debug(' #################### Starting ####################')

    """ Create config object and parse command line options
    """
    conf = EC.EngineConfig.Instance()
    conf.setPath(os.path.abspath(os.path.join(os.path.dirname(__file__))))
    conf.loadConfig()
    conf.setConfValue('baseDir', os.path.dirname(__file__))

    log.debug((docopt(__doc__, version='0.1')))

    log.debug('Creating core object')
    gfx = Engine.Core()
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    log.debug('Setting up core object')
    gfx.set_exclusive_mouse(True)
    gfx.setup()


if __name__ == '__main__':
    main()
