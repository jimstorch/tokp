#------------------------------------------------------------------------------
#   File:       loot_mdb_parser.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT   
#------------------------------------------------------------------------------

import glob
import datetime
import sys
import os
import re
from optparse import OptionParser

from tokp_lib.parse_chat import Loot
from tokp_lib.timestamp_event import timestamp_event
from tokp_lib.write_summary import write_summary
import tokp_lib.system_rules as Rules

usage = "usage: %prog [options]"
parser = OptionParser(usage=usage)
(options, args) = parser.parse_args()

## Define the start of the raid week (1=Monday, 6=Sunday)
options.raidweek_start = 2

## Open the old file
old_loot_file = 'old_loot/old_loot_by_date.txt'
old_loot_file_ID = open(old_loot_file, 'rU')

raid_date = datetime.datetime(2000,1,1,20,0)
date_str = r'(?P<year>(20[0-9][0-9]))-(?P<month>(0?[1-9]|1[012]))-(?P<day>(0?[1-9]|[12][0-9]|3[01]))'
time_str = r'(?P<hour>(0?[0-9]|[12][0-9])):(?P<minute>([0-5][0-9])):(?P<second>([0-5][0-9]))'
date_obj = re.compile(date_str)
time_obj = re.compile(time_str)

# make a new raid
loots = []
loot = Loot('',raid_date)

## Read each line of the combat log
for line_number, line in enumerate(old_loot_file_ID):
    ## Split the line on the commas, order as follows
    ## date and time, zone, boss, item, member, value
    ## one hitch, the value field is opposite from the rest of this python code
    timestamp, zone, boss, item, name, value = line.strip().split(',')
    #print timestamp, zone, boss, item, member, value
    
    ## Convert the timestamp string to an actual timestamp
    date_match_obj = date_obj.search(timestamp)
    time_match_obj = time_obj.search(timestamp)
    if date_match_obj and time_match_obj:
        year = int(date_match_obj.group('year'))
        month = int(date_match_obj.group('month'))
        day = int(date_match_obj.group('day'))
        #hour = int(time_match_obj.group('hour'))
        #minute = int(time_match_obj.group('minute'))
        #second = int(time_match_obj.group('second'))
        hour = 20
        minute = 0
        second = 0
        timestamp = datetime.datetime(year,month,day,hour,minute,second)
    elif date_match_obj:
        print 'error with time'
        timestamp = None
    elif time_match_obj:
        print 'error with date'
        timestamp = None
    else:
        print 'error with time and date'
        timestamp = None

    ## Fix the reversed loot values
    value = 5 - int(value)
    if (value == 0):
        value = 5
    value = Rules.RevValueLabels[value]

    if (timestamp == raid_date):
        # same raid, append the item
        loot.add_item( (name,item,value) )
    else:
        if (loot.item_list != []):
            loots.append(loot)
            #print loot.item_list
        # make a new raid
        loot = Loot(zone,timestamp)
        loot.add_item( (name,item,value) )
        raid_date = timestamp

    loots.append(loot)

#print loots
raids = []
## Create the summary file
write_summary(options, raids, loots)
