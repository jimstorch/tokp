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
# Seems like a lot of juggling but strftime() and strptime() do not support
# microseconds.

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


#--[ Indent ]------------------------------------------------------------------
# From http://effbot.org/zone/element-lib.htm (plus Paul Du Bois comment)

def indent(elem, level=0):
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        for child in elem:
            indent(child, level+1)
        if not child.tail or not child.tail.strip():
            child.tail = i
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


#--[ Write Raid XML ]----------------------------------------------------------

def write_raid_xml(raid):
    
    fname = raid.start_time.strftime("%Y%m%d.%H%M.") + raid.zone + '.xml'
    dstr = raid.start_time.strftime("%m/%d/%Y")
    xml = et.Element('raid',date = dstr)
    zone = et.SubElement(xml,'zone')
    zone.text = raid.zone
    start_time = et.SubElement(xml,'start_time')
    start_time.text = dt_to_str(raid.start_time)
    end_time = et.SubElement(xml,'end_time')
    end_time.text = dt_to_str(raid.end_time)
    members = et.SubElement(xml,'members')
    raid.raid_members.sort()
    for member in raid.raid_members:
        name = et.SubElement(members,'name')
        name.text = member


    tree = et.ElementTree(xml)
    indent(xml)
    indent(xml)
    f = open('raids/' + fname,'w')
    #f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    tree.write(f, 'utf-8')
    #print et.tostring(xml)


#--[ Read Raid XML ]-----------------------------------------------------------  


