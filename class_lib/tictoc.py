#------------------------------------------------------------------------------
#   File:       tictoc.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:    
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

from time import clock

class TicToc(object):
    def __init__(self):
        return

    def tic(self):
        self.Start = clock()
        return

    def toc(self):
        self.Elapsed = clock() - self.Start
        output = ('Time Elapsed: %5.3f') % (self.Elapsed)
        print output
        return
