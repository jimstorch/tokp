#------------------------------------------------------------------------------
#   File:       member_name_change.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import re
import glob

def member_name_change(old_name,new_name,base_path):
    
    ## Regex for raid_files()
    ##fname_str = r'.*[/\\](?P<folder>)[/\\](?P<fname>)\.raid'
    fname_str = r'.*[/\\](?P<folder>.+)[/\\](?P<fname>.+)\.raid'
    fname_obj = re.compile(fname_str)
    member_str = r'(?P<member>.+) [(](?P<level>.+)[)]'
    member_obj = re.compile(member_str)
    member_nolvl_str = r'(?P<member>.+)'
    member_nolvl_obj = re.compile(member_nolvl_str)
    
    # Create a list of matching *.raid files in the raid folders
    rfiles = glob.glob(base_path + '/*/*.raid')
    num_instances = 0
    for rfile in rfiles:
        # Pull out the folder and file name
        match_obj = fname_obj.search(rfile)
        folder = match_obj.group('folder')
        fname = match_obj.group('fname')
    
        # Scan file for member name and replace it
        cur_path = ('%s/%s/%s.raid') % (base_path, folder, fname)
        cur_file = open(cur_path,'r+U')
        add_new_name = 0
        for line_numer, line in enumerate(cur_file):
            match_obj = member_obj.search(line)
            nolvl = member_nolvl_obj.search(line)
            if (match_obj is None) & (nolvl is not None):
                print ('WARNING! Bad entry in %s') % (fname)
                break
            member = match_obj.group('member')
            level = match_obj.group('level')
    
            # If old name exists, create string to append to raid file
            if (member == old_name) & (not add_new_name):
    ##            print ('%s %s %s') % (member, options.old_name, options.new_name)
                add_new_name = 1
                new_line = ('%s (%s)\n') % (new_name, level)
    ##            print new_line
            elif (member == new_name) & (add_new_name):
                add_new_name = 0
    
        # Append the new name to the file
        if add_new_name:
            num_instances += 1
            cur_file.write(new_line)
        # Close the file and move on
        cur_file.close()
    
    print ('DONE! %d instances appended.') % num_instances
