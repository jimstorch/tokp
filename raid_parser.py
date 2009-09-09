#!/usr/bin/env python
#------------------------------------------------------------------------------
#   File:       raid_parser.py
#   Purpose:    
#   Author:     Jim Storch
#   Revised:
#   License:    GPLv3 see LICENSE.TXT   
#------------------------------------------------------------------------------

import time
import sys
import os
from optparse import OptionParser

#from tokp_lib.raidweeks_xml import RaidWeeksXML
#from tokp_lib.raidweeks_xml import raidweek_output
from tokp_lib.datetime_range import datetime_range
from tokp_lib.roster import get_roster
from tokp_lib.parse_combat import parse_combat
from tokp_lib.parse_chat import parse_chat
from tokp_lib.write_summary import write_summary

VERSION = '.004 (pre-alpha)'

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
    default='roster/roster.txt', 
    help="filename of the guild roster")    
parser.add_option('-v','--version', action="store_true", dest="version", 
    default=False, help="show program version number and exit")

(options, args) = parser.parse_args()

## Define the start of the raid week (1=Monday, 6=Sunday)
options.raidweek_start = 2

if options.version:
    print "Version number is", VERSION
    sys.exit()

#if not options.name:
#    print "[Error] Missing -n NAME argument. Try '-h' for help."
#    exit(1)    

## Get our datetime window
#parse_from,parse_to = datetime_range(options.date)
#if parse_from == None:
#    print "[Error] Missing or malformed -d DATE argument. Try '-h' for help."
#    exit(1)

t1 = time.time()

## Load the roster 
roster = get_roster(options.roster)

## Parse the combat log looking for raids
#raids = parse_combat(parse_from, parse_to, options.combatlog, roster, 
#    options.name)
raids = parse_combat(options.combatlog, roster)

## Parse the chat log looking for loots    
#loots = parse_chat(parse_from, parse_to, options.chatlog, roster, options.name)

## Create the summary file
loots = []
#write_summary(options, parse_from, raids, loots)
write_summary(options, raids, loots)

## Update the raidweeks.xml
#RaidWeeks = RaidWeeksXML()
#RaidWeeks.UpdateRaidWeeks(options, parse_from)

t2 = time.time()
print "[complete] Process time was %f seconds." % (t2 - t1) 

    
