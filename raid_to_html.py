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
rfiles = glob.glob('data/raids/*/*.raid')
for rfile in rfiles:
    match_obj = fname_obj.search(rfile)
    folder = match_obj.group('folder')
    fname = match_obj.group('fname')
    if folder not in file_list.keys():
        file_list[folder] = []
    file_list[folder].append(fname)

# Create an html file from the file list
html = ''
html += '<html>\n<body>\n'
for folder in file_list.keys():
    html += '<a href=../data/raids/%s/%s.raid>' % (folder, fname)
    html += '%s: %s</a>\n' % (folder, fname)
    html += '<br>\n'
html += '</body>\n</html>\n'
filename = 'data/raids/html_test.html'
output = open(filename,'w')
output.write(html)
output.close()
