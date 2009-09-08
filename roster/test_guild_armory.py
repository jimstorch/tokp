#------------------------------------------------------------------------------
#   File:       test_guild_armory.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:    
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

from tictoc import TicToc
from read_guild_armory import ArmoryGuild

# Pull out a guild from the Armory
T = TicToc()
T.tic()
PainAndSuffering = ArmoryGuild('Pain and Suffering','Galakrond','US')
T.toc()

print PainAndSuffering.Roster

# Print output for verification
##print '%s: %s %s' % (Sarkoris.Name, Sarkoris.Race, Sarkoris.Class)
##print '%s: %s' % (Sarkoris.TalentSpec, Sarkoris.TalentTree)
##print Sarkoris.Stats
##print Sarkoris.Stats['Name']
##print Sarkoris.Stats['Class']
##print Sarkoris.Stats['Race']
##print Sarkoris.Stats['BaseStats']
##print Sarkoris.Stats['TotalStats']
##print Sarkoris.Stats['TalentTree']
##print Sarkoris.SpellDmg
##print Sarkoris.SpellCrit

