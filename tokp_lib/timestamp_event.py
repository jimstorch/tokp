#------------------------------------------------------------------------------
#   File:       timestamp_event.py
#   Purpose:    
#   Author:     Jim Storch
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

# Given a line from the log file, returns a tuple consisting on the timestamp
# in datetime format and a string containing the text of the event.
# Returns (None,'') for malformed lines where regex match failed.
# Note: Logs use the format "10/24 23:04:49.453", so we have to guess the year.

import re
import datetime

rawstr = (r'^(?P<month>\d{1,2})/(?P<day>\d{1,2})\s(?P<hour>\d\d):'
            '(?P<minute>\d\d):(?P<second>\d\d).(?P<milli>\d{3})'
            '\s\s(?P<event>.+)')

compile_obj = re.compile(rawstr)
today = datetime.datetime.today()

def timestamp_event(line):

    match_obj = compile_obj.search(line)

    if match_obj:
        month = int(match_obj.group('month'))
        day = int(match_obj.group('day'))
        hour = int(match_obj.group('hour'))
        minute = int(match_obj.group('minute'))
        second = int(match_obj.group('second'))
        milli = int(match_obj.group('milli')) * 1000
        if month <= today.month:
            year = today.year 
        else:
            year = today.year - 1
        timestamp = datetime.datetime(year,month,day,hour,minute,second,milli)
        event = match_obj.group('event')

    else:
        timestamp,event = None,''

    return timestamp,event

