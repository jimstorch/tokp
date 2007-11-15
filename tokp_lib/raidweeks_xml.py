#------------------------------------------------------------------------------
#   File:       raidweeks_xml.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import datetime
import os
import re
from xml.etree import cElementTree as et
from xml_store import indent

class RaidWeek(object):

    def __init__(self, str_raidweek):
        self.NumRaidsThisWeek = 0
        self.Raids = []
        self.AttendanceDate = datetime.date(2000,1,1)
        self.set_raid_week(str_raidweek)
    
    def add_member(self, Raid):
        self.Raids.append(Raid)
        self.Raids.sort()
        self.NumRaidsThisWeek += 1

    def del_member(self, Raid):
        self.Raids.remove(Raid)
        self.NumRaidsThisWeek -= 1

    def set_raid_week(self, str_raidweek):
        """Given a string in the format 'YYYY-MM-DD YYYY-MM-DD',
        update the class with the datetime object"""

        ## Regex for SetRaidWeek()
        rawstr = r"^(?P<year1>\d{2,})-(?P<month1>\d\d)-(?P<day1>\d\d)\s" + \
                   "(?P<year2>\d{2,})-(?P<month2>\d\d)-(?P<day2>\d\d)$"
        compile_obj = re.compile(rawstr)    

        match_obj = compile_obj.search(str_raidweek)
        if match_obj:
            year1 = int(match_obj.group('year1'))
            month1 = int(match_obj.group('month1'))
            day1 = int(match_obj.group('day1'))
            year2 = int(match_obj.group('year2'))
            month2 = int(match_obj.group('month2'))
            day2 = int(match_obj.group('day2'))
            self.AttendanceDate = datetime.date(year1, month1, day1)
            return 
        else:
            raise ValueError('Could not parse datetime string')

#--[ RaidWeeksXML Class ]------------------------------------------------------
class RaidWeeksXML(object):

    def __init__(self):
        self.XMLFile = r"data\raids\raidweeks.xml"
        self.RaidWeeks = []

    ## Get the text out of a nodelist
    def getText(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        rc = str(rc)
        return rc

    ## Load the raidweeks.xml file into the raidweeks variable
    def LoadRaidWeeks(self):

        # define empty raidweeks list
        vec_raidweeks = []

        # does the raidweeks.xml file exist?
        if not os.path.isfile(self.XMLFile):
            print "Missing raidweeks.xml"
            return vec_raidweeks

        # load the raidweeks.xml file
        tree = et.parse(self.XMLFile)

        # does the base element "weeks" exist?
    ##    doc = tree.getroot().findall("weeks")
    ##    if not len(doc) == 1:
    ##        print "Badly formatted raidweeks.xml"
    ##        return vec_raidweeks

        # loop through all "week" elements
        weeks = tree.getroot().findall("week")
        for week in weeks:
            # pull out the "dir" children (if more than one, use the first)
            raidweek_dir = week.findall("dir")
            if not len(raidweek_dir) == 1:
                print "Error: Too many <dir></dir> elements in raidweeks.xml"
            raidweek_dir_str = raidweek_dir[0].text
            self.RaidWeeks.append(raidweek_dir_str)

        return

    ## Write the raidweeks list to raidweeks.xml
    def save_raidweeks(self):

        # make the xml tree
        xml = et.Element('weeks')
        for str_raidweek in self.RaidWeeks:
            el_week = et.SubElement(xml,'week')
            el_dir = et.SubElement(el_week,'dir')
            el_dir.text = str_raidweek
        tree = et.ElementTree(xml)
        indent(xml)
        indent(xml)

        # write the xml tree to file
        f = open(self.XMLFile,'w')
        tree.write(f, 'utf-8')
        
        # finished successfully
        return 1


    ## Update the raidweeks to include the week corresponding to the current raid
    def UpdateRaidWeeks(self, options, raid_date):

        # load the raidweeks
        self.LoadRaidWeeks()
        
        # form current raidweek
        str_raidweek = raidweek_output(options.raidweek_start, raid_date)
                
        # check for existence of the current raidweek in the list
        # insert the current raidweek if necessary
        if not str_raidweek in self.RaidWeeks:
            vec_raidweeks.append(str_raidweek)
            vec_raidweeks.sort()

        # save the updated raidweeks.xml
        self.save_raidweeks()

        return 

    ## Jim's implementation
    def raidweek2(timestamp):
        start_date = timestamp
        dow = start_date.weekday()
        if dow < 6:
            start_date -= datetime.timedelta(days=dow+1)
        end_date = start_date + datetime.timedelta(days=6)
        dir_name = "%s thru %s" % (start_date.strftime('%y-%m-%d'),
            end_date.strftime('%y-%m-%d'))
        return dir_name
#------------------------------------------------------------------------------

## Define a string for the raid week corresponding to the selected date
def raidweek_output(raidweek_start, raid_date):
    
    raid_day = raid_date.isoweekday()
    week_start = datetime.date
    week_end = datetime.date

    # pull out dates of start and end of the week
    if raid_day <= raidweek_start:
        temp1 = datetime.timedelta(raidweek_start-raid_day-7)
        temp2 = datetime.timedelta(raidweek_start-raid_day)
        week_start = raid_date + temp1
        week_end = raid_date + temp2
    else:
        temp1 = datetime.timedelta(raidweek_start-raid_day)
        temp2 = datetime.timedelta(raidweek_start-raid_day+7)
        week_start = raid_date + temp1
        week_end = raid_date + temp2

    # form the string for the raidweek
    str_raidweek = week_start.strftime('%Y-%m-%d') + " " + week_end.strftime('%Y-%m-%d')

    return str_raidweek
