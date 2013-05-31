#!/usr/bin/env python                                                              
# -*- coding: utf-8 -*-

from core import *
from engine import *

import sys                                                                         
import syslog                                                                      
                                                                                   
class Debug:                                                                       
                                                                                   
    def __init__(self, dlvl):                                                      
        self.level = dlvl                                                          
                                                                                   
    def setLvl(self, dlvl):                                                        
        self.level = dlvl                                                          
                                                                                   
    def stdout(self, dstr, dlvl=1):                                                
        if dlvl <= self.level:                                                     
            print dstr                                                             
                                                                                   
    def syslog(self, dstr, dlvl=1):                                                
        if dlvl <= self.level:                                                     
            syslog.syslog('%s: %s' % (sys.argv[0], dstr.replace('\n', ' ')))

def main():
    conf = core.Config()
    
    gfx = engine.Core(width=conf.getConfValue('screenWidth'), height=conf.getConfValue('screenWidth'), caption="%s v%s" % (conf.APP_NAME, conf.APP_VERSION), resizable=conf.getConfValue('resizeable'))
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    gfx.set_exclusive_mouse(True)
    gfx.setup()


if __name__ == '__main__':
    main()
