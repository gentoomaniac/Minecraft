#!/usr/bin/env python                                                              
# -*- coding: utf-8 -*-

import logging
import sys
import syslog
from optparse import OptionParser

from engine import *

def main():
    """ prepare logging obkect
    """
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s\t%(name)s\t: %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='debug.log')
    log = logging.getLogger(__name__)
    
    """ Create config object and parse command line options
    """
    conf = engine.Config()
    parser = OptionParser()
    parser.add_option("-l", "--level", dest="level",
                    help="load level", metavar="FILE")
    
    log.debug('Creating core object')
    gfx = engine.Core()
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    log.debug('Setting up core object')
    gfx.set_exclusive_mouse(True)
    gfx.setup()


if __name__ == '__main__':
    main()
