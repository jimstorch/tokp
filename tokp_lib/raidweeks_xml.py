#------------------------------------------------------------------------------
#   File:       raidweeks_xml.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:    
#------------------------------------------------------------------------------

import datetime
import os
import xml.dom.minidom

xml_file = "c:\\james\\svn\\tokp\\raids\\raidweeks.xml"

## Create an empty raidweeks.xml file
def create_raidweeks():

    empty_raidweeks = """\
    <weeks>
    </weeks>
    """
    
    raidweeks_dom = xml.dom.minidom.parseString(empty_raidweeks)


    
    return 1

## Get the text out of a nodelist
def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    rc = str(rc)
    return rc

## Load the raidweeks.xml file into the raidweeks variable
def load_raidweeks():

    vec_raidweeks = []

    if not os.path.isfile(xml_file):
        create_raidweeks()

    raidweeks_dom = xml.dom.minidom.parse(xml_file)

    # does it have the base element "weeks"?
    # if not, make a new xml and try again
    if not raidweeks_dom.getElementsByTagName("weeks"):
        create_raidweeks()
        raidweeks_dom = xml.dom.minidom.parse(xml_file)

    # pull out all "week" elements and add them to the raidweeks list
    raidweeks = raidweeks_dom.getElementsByTagName("week")
    for raidweek in raidweeks:
        raidweek_dir = raidweek.getElementsByTagName("dir")[0]
        raidweek_dir_str = getText(raidweek_dir.childNodes)
        # print "%s" % raidweek_dir_str
        vec_raidweeks.append(raidweek_dir_str)

    return vec_raidweeks


## Write the raidweeks list to raidweeks.xml
def save_raidweeks():

    # load the raidweeks
    vec_raidweeks = load_raidweeks()

    # form current raidweek
    str_raidweek = raidweek_output()

    # finished successfully
    return 1

## Update the raidweeks to include the week corresponding to the current raid
def update_raidweeks(options, raid_date):

    return 1

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
    
    
