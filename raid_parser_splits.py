import glob
import time
import sys
import os
from optparse import OptionParser

#from tokp_lib.raidweeks_xml import RaidWeeksXML
#from tokp_lib.raidweeks_xml import raidweek_output
#from tokp_lib.datetime_range import datetime_range
from tokp_lib.roster import get_roster
from tokp_lib.parse_combat import parse_combat
from tokp_lib.parse_chat import parse_chat
from tokp_lib.write_summary import write_summary

usage = "usage: %prog [options]"
parser = OptionParser(usage=usage)
(options, args) = parser.parse_args()

## Define the start of the raid week (1=Monday, 6=Sunday)
options.raidweek_start = 2

t1 = time.time()

## Load the roster 
roster = get_roster('roster/roster.txt')

## Parse the combat log looking for raids
logfiles = glob.glob('logs/split_logs/*.txt')
for combatlog in logfiles:
    raids = parse_combat(combatlog, roster)

    ## Parse the chat log looking for loots    
    loots = []
    #loots = parse_chat(options.chatlog, roster, options.name)

    ## Create the summary file
    write_summary(options, raids, loots)

t2 = time.time()
print "[complete] Process time was %f seconds." % (t2 - t1) 
