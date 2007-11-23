#------------------------------------------------------------------------------
#   File:       raid_to_html.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

'''
Create html listing of all old-style *.raid files.
(for display of raid listings)
'''

import re
import glob

## Regex for raid_files()
##fname_str = r'.*[/\\](?P<folder>)[/\\](?P<fname>)\.raid'
fname_str = r'.*[/\\](?P<folder>.+)[/\\](?P<fname>.+)\.raid'
fname_obj = re.compile(fname_str)

# Create a list of matching *.raid files in the raid folders
file_list = {}
rfiles = glob.glob('raids/*/*.raid')
for rfile in rfiles:
    match_obj = fname_obj.search(rfile)
    folder = match_obj.group('folder')
    fname = match_obj.group('fname')
    if folder not in file_list.keys():
        file_list[folder] = []
    file_list[folder].append(fname)

# Make a sorted list of folders
folder_list = dict.fromkeys(file_list).keys()
folder_list.sort()

# Create html files from the folder list
week_html = '<html>\n<body>\n'
for folder in folder_list:
    week_html += '<a href="raids/%s/raidlist.html">%s</a><br>\n' % (folder, folder)
    raid_html = '<html>\n<body>\n'
    for fname in file_list[folder]:
        raid_html += '<a href="%s.raid">%s</a>\n<br>\n' % (fname, fname)
    raid_html += '</body>\n</html>\n'
    filename = 'raids/%s/raidlist.html' % (folder)
    raid_list = open(filename,'w')
    raid_list.write(raid_html)
    raid_list.close()
week_html += '</body>\n</html>\n'
week_list = open('weeklist.html','w')
week_list.write(week_html)
week_list.close()
