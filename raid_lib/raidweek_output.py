#------------------------------------------------------------------------------
#   File:       raidweek_output.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:    
#------------------------------------------------------------------------------

# Based on raid date, define the folder name for the current raid week.

# raidweek_start - day of the week on which the raid week starts and ends
#                  (monday=1, tuesday=2 ...)
# raid_date - date triplet

import datetime

def raidweek_output(raidweek_start,raid_date):
    
    raidweek = []
    raid_day = raid_date.isoweekday()
    week_start = datetime.date
    week_end = datetime.date

    # pull out dates of start and end of the week
    if raid_day <= raidweek_start:
        temp1 = datetime.timedelta(raidweek_start-raid_day-7)
        temp2 = datetime.timedelta(raidweek_start-raid_day)
##        print "temp1:", temp1
##        print "temp2:", temp2
        week_start = raid_date + temp1
        week_end = raid_date + temp2
    else:
        temp1 = datetime.timedelta(raidweek_start-raid_day)
        temp2 = datetime.timedelta(raidweek_start-raid_day+7)
##        print "temp1:", temp1
##        print "temp2:", temp2
        week_start = raid_date + temp1
        week_end = raid_date + temp2

##    print week_start.isoformat()
##    print week_end.isoformat()

    # form the string for the raidweek
    str_raidweek = week_start.isoformat() + " " + week_end.isoformat()
##    print str_raidweek

    return str_raidweek
    

def raidweek2(timestamp):
    start_date = timestamp
    dow = start_date.weekday()
    if dow < 6:
        start_date -= datetime.timedelta(days=dow+1)
    end_date = start_date + datetime.timedelta(days=6)
    dir_name = "%s thru %s" % (start_date.strftime('%y-%m-%d'),
        end_date.strftime('%y-%m-%d'))
    return dir_name
    
    
    
 
    

