#!/usr/bin/env python                                                              
# -*- coding: utf-8 -*-

import logging
import sys
import os
import syslog
from optparse import OptionParser

import engine.EngineConfig as EC
import engine.engine as Engine

def main():
    """ prepare logging object
    """
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s\t%(name)s\t: %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='debug.log')
    log = logging.getLogger(__name__)
    
    log.debug(' #################### Starting ####################')
    
    # get config object
    conf = EC.EngineConfig.Instance()
    conf.setPath(os.path.abspath(os.path.join(os.path.dirname(__file__))))
    conf.loadConfig()
    conf.setConfValue('baseDir', os.path.dirname(__file__))
    
    """ Create config object and parse command line options
    """
    parser = OptionParser()
    parser.add_option("-l", "--level", dest="level",
                    help="load level", metavar="FILE")
    
    log.debug('Creating core object')
    gfx = Engine.Core()
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    log.debug('Setting up core object')
    gfx.set_exclusive_mouse(True)
    gfx.setup()


if __name__ == '__main__':
    main()
