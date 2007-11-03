#------------------------------------------------------------------------------
#   File:       raidweeks_xml.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:    
#------------------------------------------------------------------------------

import datetime
import os
import xml.parsers.expat

xml_file = "raids\raidweeks.xml"

## Create an empty raidweeks.xml file
def create_raidweeks()




## Load the raidweeks.xml file into the raidweeks variable
def load_raidweeks():

    if not os.path.isfile(xml_file):
        print "Error!"

    raidweeks = "temp"

    return raidweeks


## Save the raidweeks variable to raidweeks.xml
def save_raidweeks():

    # finished successfully
    return 1


## Define a string for the raid week corresponding to the selected date
def raidweek_output(raidweek_start,raid_date):
    
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
    
    
