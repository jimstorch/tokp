#!/usr/bin/env python
#------------------------------------------------------------------------------
#   File:       xml_test.py
#   Purpose:    
#   Author:     Jim Storch
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import datetime
import random

from tokp_lib.parse_combat import Raid 
from tokp_lib.xml_store import write_raid_xml

timestamp = datetime.datetime.now()
ten_minutes = datetime.timedelta(minutes=10)


zones = ['Mines of Moria','Mordor','Minas Morgul','Dennys']

guild = ['Everard', 'Sam', 'Sauron', 'Boromir', 'Galadriel',
    'Legolas', 'Peregrin', 'Celeborn', 'Proudfoot', 'Gilgalad',
    'Bilbo', 'Saruman','Lurtz', 'Gandalf', 'Lendil', 
    'Rosie', 'Merry', 'Aragorn', 'Bounder', 'Haldir',
    'Maggot', 'Gimli', 'Gollum', 'Isildur','Arwen',
    'Barliman', 'Elrond', 'Frodo', 'Larry', 'Curly']

zone = random.choice(zones)
raid = Raid(zone, timestamp)
## make a raid of 20 random members
while len(raid.raid_members) < 20:
    timestamp += ten_minutes
    raid.add_member(random.choice(guild), timestamp)

raid.end_time = timestamp + ten_minutes

write_raid_xml(raid)    

