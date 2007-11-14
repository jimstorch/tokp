#!/usr/bin/env python
#------------------------------------------------------------------------------
#   File:       xml_test.py
#   Purpose:    
#   Author:     Jim Storch
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

"""
This script creates 12 random raids with 20 random guild members each.
The first raid is on Oct 1, 2007 and the next 11 occur randomly spaced
three to six days apart.
"""

import datetime
import random

from tokp_lib.parse_combat import Raid
from tokp_lib.xml_store import write_raid_xml, read_raid_xml, raid_files
from tokp_lib.raidweeks_xml import RaidWeek, raidweek_output
from tokp_lib.compute_score import GuildMember

zones = ['Mines of Moria','Mordor','Minas Morgul','Dennys']

guild = ['Everard', 'Sam', 'Sauron', 'Boromir', 'Galadriel',
    'Legolas', 'Peregrin', 'Celeborn', 'Proudfoot', 'Gilgalad',
    'Bilbo', 'Saruman','Lurtz', 'Gandalf', 'Lendil', 
    'Rosie', 'Merry', 'Aragorn', 'Bounder', 'Haldir',
    'Maggot', 'Gimli', 'Gollum', 'Isildur','Arwen',
    'Barliman', 'Elrond', 'Frodo', 'Larry', 'Curly']


one_day = datetime.timedelta(days=1)
three_hours = datetime.timedelta(minutes=180)

raid_night = datetime.datetime(2007,10,1,19,0,0)

for x in range(12):
    zone = random.choice(zones)
    raid = Raid(zone, raid_night)
    ## make a raid of 20 random members
    while len(raid.raid_members) < 20:
        temp = random.choice(guild)
        raid.add_member(temp)
    raid.end_time = raid_night + three_hours
    write_raid_xml(raid)
    raid_night += one_day * random.randrange(3,7)

AllRaids = {}
file_list = raid_files()
for fname in file_list:
    if not fname == "raidweeks":
        AllRaids[fname] = read_raid_xml(fname+'.xml')
#print AllRaids
    
# scan the raid dictionary:
# create dictionary of guild members
# update guild as new members found
# update participation

# define the guild
Guild = {}
RaidWeekStart = 2
RaidWeeks = {}

# sort the raids into raidweek buckets
for index in AllRaids.keys():
    str_raidweek = raidweek_output(RaidWeekStart, AllRaids[index].start_time)
    if str_raidweek not in RaidWeeks.keys():
        RaidWeeks[str_raidweek] = RaidWeek()
        RaidWeeks[str_raidweek].SetRaidWeek(str_raidweek)
    RaidWeeks[str_raidweek].add_member(AllRaids[index])
    # can add loot to the Guild dictionary here!    

# compute participation in each week
Attendance = []
for week in RaidWeeks.keys():
    WeekAttendance = {}
    for CurRaid in RaidWeeks[week].Raids:
        for Member in CurRaid.raid_members:
            if Member not in Guild.keys():
                Guild[Member] = GuildMember()
            if Member not in WeekAttendance.keys():
                WeekAttendance[Member] = 0
            WeekAttendance[Member] += float(1) / float(RaidWeeks[week].NumRaidsThisWeek)
    # store the weekly participation event for each member
    for Member in Guild.keys():
        if Member in WeekAttendance.keys():
            Guild[Member].add_participation(RaidWeeks[week].AttendanceDate, WeekAttendance[Member])
        else:
            Guild[Member].add_participation(RaidWeeks[week].AttendanceDate, 0)

# scan events for all guild members
for Member in Guild.keys():
    Guild[Member].ScanMemberEvents()
##    print Guild[Member].Scores
