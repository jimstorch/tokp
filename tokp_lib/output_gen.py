#------------------------------------------------------------------------------
#   File:       output_gen.py
#   Purpose:    
#   Author:     Jim Storch
#   Revised:    
#------------------------------------------------------------------------------

def output_folder(timestamp):
    ## Given a datetime, returns a string 
    start_date = timestamp
    dow = start_date.weekday()
    if dow < 6:
        start_date -= datetime.timedelta(days=dow+1)
    end_date = start_date + datetime.timedelta(days=6)
    dir_name = "%s thru %s" % (start_date.strftime('%y-%m-%d'),
        end_date.strftime('%y-%m-%d'))
    return dir_name
