#------------------------------------------------------------------------------
#   File:       get_roster.py
#   Purpose:    
#   Author:     Jim Storch
#   Revised:
#   License:    GPL v2    
#------------------------------------------------------------------------------

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
