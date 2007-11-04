#------------------------------------------------------------------------------
#   File:       datetime_range.py
#   Purpose:    
#   Author:     Jim Storch
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

# Given a month/day string in the format MM/DD returns two datetime objects
# equaling 6:00 am the given day and 6:00am the next

import datetime
import re

rawstr = r"""(?P<month>0[1-9]|1[012])[- /.](?P<day>0[1-9]|[12][0-9]|3[01])"""
compile_obj = re.compile(rawstr)
today = datetime.datetime.today()

def datetime_range(date_arg):

    match_obj = compile_obj.search(date_arg)
    
    if match_obj:
        month = int(match_obj.group('month'))
        day = int(match_obj.group('day'))

        if month <= today.month:
            year = today.year
        else:
            year = today.year - 1
        one_day = datetime.timedelta(days=1)   
        parse_from = datetime.datetime(year,month,day,6,0)
        parse_to = parse_from + one_day

    else:
        parse_from, parse_to = None, None

    return parse_from, parse_to


