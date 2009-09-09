#------------------------------------------------------------------------------
#   File:       tokp.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import time
import sys
from optparse import OptionParser
from tokp_lib.compute_score import Guild

VERSION = '.001 (pre-alpha)'

## Options
usage = "usage: %prog [options]"
tokp_options = OptionParser(usage=usage)
tokp_options.add_option('-v','--version', action="store_true", dest="version", 
    default=False, help="show program version number and exit")
(options, args) = tokp_options.parse_args()

# display version number and end
if options.version:
    print "Version number is", VERSION
    sys.exit()

# time at program start
t1 = time.time()

# define the guild
ToK = Guild()
# load all raids
#ToK.LoadRaids()
ToK.LoadAll()
t2 = time.time()
print "[raids loaded] Process time was %1.3f seconds." % (t2 - t1) 
# compute attendance at every raidweek
ToK.ComputeAttendance()
t2 = time.time()
print "[scores computed] Process time was %1.3f seconds." % (t2 - t1) 
# update reports for output
ToK.UpdateReports()
t2 = time.time()
print "[reports updated] Process time was %1.3f seconds." % (t2 - t1) 

# display program run time
t2 = time.time()
print "[complete] Process time was %1.3f seconds." % (t2 - t1) 

