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


zones = ['Mines of Moria','Mordor','Minas Morgul','Dennys']

guild = ['Everard', 'Sam', 'Sauron', 'Boromir', 'Galadriel',
    'Legolas', 'Peregrin', 'Celeborn', 'Proudfoot', 'Gilgalad',
    'Bilbo', 'Saruman','Lurtz', 'Gandalf', 'Lendil', 
    'Rosie', 'Merry', 'Aragorn', 'Bounder', 'Haldir',
    'Maggot', 'Gimli', 'Gollum', 'Isildur','Arwen',
    'Barliman', 'Elrond', 'Frodo', 'Larry', 'Curly']


one_day = datetime.timedelta(days=1)
three_hours = datetime.timedelta(minutes=180)

raid_night = datetime.datetime(2007,9,1,19,0,0)

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


