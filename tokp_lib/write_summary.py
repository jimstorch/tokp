#------------------------------------------------------------------------------
#   File:       write_summary.py
#   Purpose:    
#   Author:     
#   Revised:    
#   License:    GPLv3 see LICENSE.TXT
#------------------------------------------------------------------------------

import os
import datetime

from raidweeks_xml import raidweek_output

#def write_summary(options, raid_date, raids, loots):
def write_summary(options, raids, loots):

    for raid in raids:
        # make the file name
        datestr = raid.start_time.strftime('%Y-%m-%d')
        raidweekstr = raidweek_output(options.raidweek_start, raid.start_time)
        output_path = ('data/raids/%s' % raidweekstr)
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        filename = ('%s/%s %s.txt' % (output_path, datestr, options.name))
        summary = open(filename,'w')    
    
        line = 'Raided %s from %s until %s.\n' % (raid.zone, 
            raid.start_time.strftime('%H:%M'),
            raid.end_time.strftime('%H:%M'))
        summary.write(line)
        summary.write('Guild members in attendance:\n\n')
        raid.raid_members.sort()
        for member in raid.raid_members:
            summary.write('    ' + member + '\n')
        summary.close()
        
        # do it again with the old formatting
        datestr = raid.start_time.strftime('%Y-%m-%d')
        raidweekstr = raidweek_output(options.raidweek_start, raid.start_time)
        output_path = ('data/raids/%s' % raidweekstr)
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        filename = ('%s/%s_%s.raid' % (output_path, datestr, raid.zone))
        summary = open(filename,'w')
        raid.raid_members.sort()
        for member in raid.raid_members:
            summary.write(member + ' (0)' + '\n')
        summary.close()

    for loot in loots:
        # write loot files with the old formatting
        datestr = loot.start_time.strftime('%Y-%m-%d')
        raidweekstr = raidweek_output(options.raidweek_start, loot.start_time)
        output_path = ('data/raids/%s' % raidweekstr)
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        filename = ('%s/%s %s.loot' % (output_path, datestr, loot.zone))
        print filename
        summary = open(filename,'w')
        for item in loot.item_list:
            summary.write(item[0] + ',' + item[1] + ',\n')
        summary.close()
            
#    summary.write('\n\nLoot received this day:\n\n')
#    for loot in loots:
#        line = "    %s -- '%s' at %s.\n" % (loot[1], loot[2], 
#            loot[3].strftime('%H:%M'))
#        summary.write(line)            
#    summary.close()

    return 1
