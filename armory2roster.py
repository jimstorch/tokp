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

from tokp_lib.roster import ArmoryGuild
from tokp_lib.roster import write_roster_text

VERSION = '.001 (pre-alpha)'

#--[ Option Juggling ]---------------------------------------------------------

## Options
usage = "usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option('-n','--guildname', dest='guildname', 
    default='Pain and Suffering', 
    help="Name of the guild. Default is 'Pain and Suffering'")
parser.add_option('-r','--realm', dest='realm', 
    default='Galakrond', 
    help="Name of the realm. Default is 'Galakrond'")
parser.add_option('-l','--locale', dest='locale', 
    default='US', 
    help="Name of the locale. Default is 'US'")
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

if not options.overwrite and os.path.exists(options.outfile):
    print "[error] '%s' already exist.  Use '-y' to overwrite." \
         % options.outfile
    sys.exit()    

# read in the contents of the armory
Guild = ArmoryGuild(options.guildname,options.realm,options.locale)

# write out a plain text file with one name per line
write_roster_text(Guild.Roster,options.outfile)
