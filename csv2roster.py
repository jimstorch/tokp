#!/usr/bin/env python
#------------------------------------------------------------------------------
#   File:       csv2roster.py
#   Purpose:    converts a CSV file of guild members into a straight text file
#               of names
#   Author:     Jim Storch
#   Revised:
#   License:    GPLv3 see LICENSE.TXT
#------------------------------------------------------------------------------

import csv
from optparse import OptionParser
import sys
import os

from tokp_lib.roster import get_roster_csv
from tokp_lib.roster import write_roster_text

VERSION = '.001 (pre-alpha)'

#--[ Option Juggling ]---------------------------------------------------------

## Options
usage = "usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option('-i','--infile', dest='infile', 
    default='roster/ToK Roster.csv', 
    help="Name of the CSV roster file. Default is 'roster/ToK Roster.csv'")
parser.add_option('-o','--outfile', dest='outfile', 
    default='roster/roster.txt', 
    help="Name of the roster text file to create. "+
        "Default is 'roster/roster.txt'")
parser.add_option('-y','--yes', action="store_true", dest="overwrite", 
    default=False, help="OK to overwrite existing roster file.")
parser.add_option('-v','--version', action="store_true", dest="version", 
    default=False, help="Show program version number and exit.")

(options, args) = parser.parse_args()

if options.version:
    print "Version number is", VERSION
    sys.exit()

if not os.path.exists(options.infile) or not os.path.isfile(options.infile):
    print "[error] CSV file '%s' is not readible." % options.infile
    sys.exit()

if not options.overwrite and os.path.exists(options.outfile):
    print "[error] '%s' already exist.  Use '-y' to overwrite." \
         % options.outfile
    sys.exit()    

# read in the contents of the CSV file
roster = get_roster_csv(options.infile)

# write out a plain text file with one name per line
write_roster_text(roster,options.outfile)
 
    


