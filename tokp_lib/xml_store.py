#------------------------------------------------------------------------------
#   File:       xml_store.py
#   Purpose:    Store and Retrieve data from XML files
#   Author:     Jim Storch
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import datetime
import re
import glob
from xml.etree import cElementTree as et

from tokp_lib.parse_combat import Raid 


#--[ Datetime to String ]------------------------------------------------------
# Seems like a lot of juggling but strftime() and strptime() do not support
# microseconds.

def dt_to_str(dt):

    """Given a datetime object,
    returns a string in the format 'YYYY-MM-DD HH:MM:SS:MMMMMM'."""
    
    return '%d-%.2d-%.2d %.2d:%.2d:%.2d.%.6d' % (
         dt.year, dt.month, dt.day,
         dt.hour, dt.minute, dt.second, dt.microsecond )


#--[ String to Datetime ]------------------------------------------------------

## Regex for str_to_dt()
rawstr = r"^(?P<year>\d{2,})-(?P<month>\d\d)-(?P<day>\d\d)\s(?P<hour>\d\d)" + \
    ":(?P<minute>\d\d):(?P<second>\d\d)\.(?P<micro>\d*)$"
compile_obj = re.compile(rawstr)

def str_to_dt(string_in):

    """Given a string in the format 'YYYY-MM-DD HH:MM:SS:MMMMMM,'
    returns a datetime object."""
    
    match_obj = compile_obj.search(string_in)
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
# From http://effbot.org/zone/element-lib.htm (plus Paul Du Bois's comment)

def indent(elem, level=0):

    """Make an ElementTree all nice and pretty with indents and line breaks."""

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
    
    """ Given a Raid object, serializes it to an XML file.
    Returns the filename used."""
        
    fname = raid.start_time.strftime("%Y%m%d.%H%M.") + raid.zone + '.xml'
    dstr = raid.start_time.strftime("%m/%d/%Y")
    xml = et.Element('raid',date = dstr)
    ## Zone
    zone = et.SubElement(xml,'zone')
    zone.text = raid.zone
    ## Start Time
    start_time = et.SubElement(xml,'start_time')
    start_time.text = dt_to_str(raid.start_time)
    ## End Time
    end_time = et.SubElement(xml,'end_time')
    end_time.text = dt_to_str(raid.end_time)
    ## Members
    members = et.SubElement(xml,'members')
    raid.raid_members.sort()
    for member in raid.raid_members:
        name = et.SubElement(members,'name')
        name.text = member
    ## Make pretty and write to a file
    indent(xml)
    f = open('data/raids/' + fname,'w')
    f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    tree = et.ElementTree(xml)
    tree.write(f, 'utf-8')
    #print et.tostring(xml)
    return fname


#--[ Read Raid XML ]-----------------------------------------------------------  

def read_raid_xml(fname):
    
    """Given an XML file name, un-serializes it to a Raid object.
    Returns the Raid object."""
  
    tree = et.parse(open('data/raids/' + fname,'rU'))
    zone = tree.findtext('zone')
    start_time_str = tree.findtext('start_time')
    start_time = str_to_dt(start_time_str)
    end_time_str = tree.findtext('end_time')
    end_time = str_to_dt(end_time_str)
    raid = Raid(zone,start_time)
    raid.end_time = end_time 
    for elem in tree.getiterator('name'):
        raid.add_member(elem.text)
    return raid    

#--[ Raid Files ]-------------------------------------------------------------- 

## Regex for raid_files()
fname_str = r'.*[/\\](?P<fname>.+)\.xml'
fname_obj = re.compile(fname_str)

def raid_files():

    """Returns a chronologically sorted list of raid XML file names."""

    file_list = []
    xfiles = glob.glob('data/raids/*.xml')
    for xfile in xfiles:
        match_obj = fname_obj.search(xfile)           
        file_list.append(match_obj.group('fname'))
    file_list.sort()
    return file_list
   

