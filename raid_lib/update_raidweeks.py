#------------------------------------------------------------------------------
#   File:       update_raidweeks.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:    
#------------------------------------------------------------------------------

import datetime
import os
import xml.parsers.expat

#from raid_lib.raidweek_output import raidweek_output

def update_raidweeks(options, raid_date):

    xml_file = "raids\raidweeks.xml"

    if not os.path.isfile(xml_file):
        print "Error!"

    

    return 1

