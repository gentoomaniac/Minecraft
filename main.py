#!/usr/bin/env python                                                              
# -*- coding: utf-8 -*-

import sys                                                                         
import syslog                                                                      
from optparse import OptionParser

from core import *
from engine import *
                                                                                   
def main():
    """ Create config object and parse command line options
    """
    conf = core.Config()
    parser = OptionParser()
    parser.add_option("-l", "--level", dest="level",
                    help="load level", metavar="FILE")
    
    gfx = engine.Core(width=conf.getConfValue('screenWidth'), height=conf.getConfValue('screenWidth'), caption="%s v%s" % (conf.APP_NAME, conf.APP_VERSION), resizable=conf.getConfValue('resizeable'))
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    gfx.set_exclusive_mouse(True)
    gfx.setup()


if __name__ == '__main__':
    main()
