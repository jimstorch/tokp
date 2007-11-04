#------------------------------------------------------------------------------
#   File:       get_roster.py
#   Purpose:    
#   Author:     Jim Storch
#   Revised:
#   License:    GPLv3 see LICENSE.TXT 
#------------------------------------------------------------------------------

import csv


#--[ Get Roster ]--------------------------------------------------------------

def get_roster(roster_file):
    roster = []
    text_file = open(roster_file,'rU')
    for line in text_file:
        guildie = line.strip()
        if not guildie in roster:        
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

def get_roster_csv(csv_file):
    roster = []
    print "[get_roster_csv] reading file '%s'" % csv_file
    reader = csv.reader(open(csv_file,'rU'))
    # skip the header row
    foo = reader.next()
    for row in reader:
        ## only retrieve the level 70's (or greater; cheap futureproof)
        if int(row[3]) >= 70: 
            roster.append(row[0])
    print "[get_roster_csv] Found", len(roster), "level 70 guildmembers."
    #print roster       
    return roster


#--[ Write Roster Text ]-------------------------------------------------------

def write_roster_text(roster, text_file):
    roster.sort()
    print "[writie_roster_text] Writing new roster to", text_file
    out = open(text_file,'w')
    for guildie in roster:
        out.write(guildie + '\n')
    out.close()
    
    


