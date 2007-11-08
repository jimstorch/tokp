#!/usr/bin/env python
#------------------------------------------------------------------------------
#   File:       xml_test.py
#   Purpose:    
#   Author:     Jim Storch
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import datetime

from tokp_lib.parse_combat import Raid 
from tokp_lib.xml_store import raid_to_xml


timestamp = datetime.datetime.now()
ten_minutes = datetime.timedelta(minutes=10)

raid = Raid('Test Zone', timestamp)
for member in ['Redguy','Greenguy','Blueguy','Orangeguy','Greyguy','Brownguy']:
    timestamp += ten_minutes
    raid.add_member(member, timestamp)
raid.end_time = timestamp + ten_minutes    

raid_xml = raid_to_xml(raid)

print raid_xml
