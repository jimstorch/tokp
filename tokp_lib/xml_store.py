#------------------------------------------------------------------------------
#   File:       xml_store.py
#   Purpose:    Store and Retrieve data from XML files
#   Author:     Jim Storch
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import datetime
import re
from xml.etree import cElementTree as et


rawstr = r"^(?P<year>\d{2,})-(?P<month>\d\d)-(?P<day>\d\d)\s(?P<hour>\d\d)" + \
    ":(?P<minute>\d\d):(?P<second>\d\d)\.(?P<micro>\d*)$"
compile_obj = re.compile(rawstr)


#--[ Converting Datetime Objects ]---------------------------------------------

## Seems like a lot of juggling but strftime() and strptime() don't support
## microseconds.

def dt_to_str(dt):
    ## Convert a datetime to a string formated YYYY-MM-DD HH:MM:SS:MMMMMM
    return '%d-%.2d-%.2d %.2d:%.2d:%.2d.%.6d' % (
         dt.year, dt.month, dt.day,
         dt.hour, dt.minute, dt.second, dt.microsecond )

def str_to_dt(string):
    ## Convert a string back into datetime object
    match_obj = compile_obj.search(string)
    if match_obj:
        year = int(match_obj.group('year'))
        month = int(match_obj.group('month'))
        day = int(match_obj.group('day'))
        hour = int(match_obj.group('hour'))
        minute = int(match_obj.group('minute'))
        second = int(match_obj.group('second'))
        micro = int(match_obj.group('micro'))
        return datetime.datetime(year, month, day, hour, minute, second, micro)
    
    else:
        raise ValueError('Could not parse datetime string')    


#--[ Raid to XML ]-------------------------------------------------------------

def raid_to_xml(raid):
    
    #xml = et.Element('raid', zone = raid.zone, 
    #    start_time = dt_to_str(raid.start_time),
    #    end_time = dt_to_str(raid.end_time))
    
    xml = et.Element('raid')
    zone = et.SubElement(xml,'zone')
    zone.text = raid.zone
            
    for member in raid.raid_members:
        guy = et.Element('member',name=member)
        xml.append(guy)  

    return et.tostring(xml)

    


