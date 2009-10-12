#------------------------------------------------------------------------------
#   File:       member_name_change.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

'''
Scan all raid files, change member from old name to new name.
'''

import re
import glob
from optparse import OptionParser
from tok_lib.member_name_change import member_name_change

## Options
usage = "usage: %prog [options] -d DATE -n NAME"
parser = OptionParser(usage=usage)
parser.add_option('-o','--old name', dest='old_name', default='',
    help="old name")
parser.add_option('-n','--new name', dest='new_name', default='',
    help="new name")
parser.add_option('-p','--base path', dest='base_path', default='data/raids/',
    help="base path")
(options, args) = parser.parse_args()

if not options.old_name:
    print "[Error] Missing -o OLD_NAME argument. Try '-h' for help."
    exit(1)
if not options.new_name:
    print "[Error] Missing -n NEW_NAME argument. Try '-h' for help."
    exit(1)

member_name_change(options.old_name, options.new_name, options.base_path)
