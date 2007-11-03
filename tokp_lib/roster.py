#------------------------------------------------------------------------------
#   File:       get_roster.py
#   Purpose:    
#   Author:     Jim Storch
#   Revised:
#   License:    GPL v2    
#------------------------------------------------------------------------------

import csv

def get_roster(roster_file):

    roster = []
   
    text_file = open(roster_file,'rU')
    for guildie in text_file:
        guildie = line.strip()
        if not guildie in roster        
            roster.append(guildie)
        else:
            print '[warning] Duplicate guildmember name:', guildie

    print "[get_roster] Found", len(roster), "guildmembers."
    # print roster
    return roster


#--[ Get Roster CSV ]----------------------------------------------------------

# Reads the roster from a CSV file and returns a list of all guildmember names.

# Roster CSV format:
# Index    Value
# 0        Name
# 1        Rank & Title, possible values:
#              '1 - Guild Leader'
#              '2 - Officer'
#              '3 - Banker'
#              '4 - Member'll
#              '5 - Initiate'
#              '6 - Alt Char'
#              '7 - Guest'
# 2        Note
# 3        Level
# 4        Class

def get_roster_csv(roster_csv_file):
    roster = []
    reader = csv.reader(open(roster_file,'rU'))
    # skip the header row
    foo = reader.next()
    for row in reader:
        ## only retrieve the level 70's (or greater; cheap futureproof)
        if int(row[3]) >= 70: 
            roster.append(row[0])
    print "[roster] Found", len(roster), "level 70 guildmembers."
    #print roster       
    return roster


#--[ Write Roster Text ]-------------------------------------------------------

def write_roster_text(roster, roster_text_file):
        pass


