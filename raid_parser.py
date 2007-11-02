#!/usr/bin/env python
#------------------------------------------------------------------------------
#   File:       raid_parser.py
#   Purpose:    
#   Author:     Jim Storch
#   Revised:    
#------------------------------------------------------------------------------

import time
import sys
from optparse import OptionParser

from raid_lib.datetime_range import datetime_range
from raid_lib.get_roster import get_roster
from raid_lib.parse_combat import parse_combat
from raid_lib.parse_chat import parse_chat

VERSION = '.002 (pre-alpha)'

## Options
usage = "usage: %prog [options] -d DATE -n NAME"
parser = OptionParser(usage=usage)
parser.add_option('-d','--date', dest='date',
    help="date to parse in the format 'MM/DD'", default='')
parser.add_option('-n','--name', dest='name', default=None,
    help="name of the character that created BOTH logs")
parser.add_option('-b','--battlelog', dest='combatlog', 
    default='logs/WoWCombatLog.txt',
    help="filename of the combat log to parse")
parser.add_option('-c','--chatlog', dest='chatlog', 
    default='logs/WoWChatLog.txt', help="filename of the chat log to parse")
parser.add_option('-r','--roster', dest='roster', 
    default='roster/ToK Roster.csv', 
    help="filename of the guild roster(CSV format)")    
parser.add_option('-v','--version', action="store_true", dest="version", 
    default=False, help="show program version number and exit")

(options, args) = parser.parse_args()

if options.version:
    print "Version number is", VERSION
    sys.exit()

if not options.name:
    print "[Error] Missing -n NAME argument. Try '-h' for help."
    exit(1)    

## Get our datetime window
parse_from,parse_to = datetime_range(options.date)
if parse_from == None:
    print "[Error] Missing or malformed -d DATE argument. Try '-h' for help."
    exit(1)

t1 = time.time()

## Load the roster 
roster = get_roster(options.roster)

## Parse the combat log looking for raids
raids = parse_combat(parse_from, parse_to, options.combatlog, roster, 
    options.name)

## Parse the chat log looking for loots    
loots = parse_chat(parse_from, parse_to, options.chatlog, roster, options.name)

## Create the summary file
datestr = parse_from.strftime('%Y-%m-%d') 
filename = ('raids/%s_%s.txt' % (datestr, options.name))
summary = open(filename,'w')

for raid in raids:
    line = 'Raided %s from %s until %s.\n' % (raid.zone, 
        raid.start_time.strftime('%H:%M'),
        raid.end_time.strftime('%H:%M'))
    summary.write(line)
    summary.write('Guild members in attendance:\n\n')
    raid.raid_members.sort()
    for member in raid.raid_members:
        summary.write('    ' + member + '\n')    
        
summary.write('\n\nLoot received this day:\n\n')
for loot in loots:
    line = "    %s -- '%s' at %s.\n" % (loot[1], loot[2], 
        loot[3].strftime('%H:%M'))
    summary.write(line)            
summary.close()

t2 = time.time()
print "[complete] Process time was %f seconds." % (t2 - t1) 

    
