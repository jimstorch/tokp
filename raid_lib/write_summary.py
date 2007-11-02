#------------------------------------------------------------------------------
#   File:       write_summary.py
#   Purpose:    
#   Author:     
#   Revised:    
#------------------------------------------------------------------------------

import os
import datetime

from raid_lib.raidweek_output import raidweek_output

def write_summary(options, raid_date, raids, loots):

    # make the file name
    datestr = raid_date.strftime('%Y-%m-%d')
    raidweekstr = raidweek_output(options.raidweek_start, raid_date)
    output_path = ('raids/%s' % raidweekstr)
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    filename = ('%s/%s_%s.txt' % (output_path, datestr, options.name))
    summary = open(filename,'w')

    for raid in raids:
        line = 'Raided %s from %s until %s.\n' % (raid.zone, 
            raid.start_time.strftime('%H:%M'),
            raid.end_time.strftime('%H:%M'))
        summary.write(line)
        summary.write('Guild members in attendance:\n\n')
        raid.raid_members.sort()
        for member in raid.raid_members:
            summary.write('    ' + member + '\n')    
            
    summary.write('\n\nLoot received this day:\n\n')
    for loot in loots:
        line = "    %s -- '%s' at %s.\n" % (loot[1], loot[2], 
            loot[3].strftime('%H:%M'))
        summary.write(line)            
    summary.close()

    return 1
