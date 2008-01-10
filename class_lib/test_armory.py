#------------------------------------------------------------------------------
#   File:       test_armory.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:    
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

from read_armory import ArmoryCharacter

# Pull out a character from the Armory
Sarkoris = ArmoryCharacter('Sarkoris','Alleria','US')

# Print output for verification
print '%s: %s %s' % (Sarkoris.Name, Sarkoris.Race, Sarkoris.Class)
print '%s: %s' % (Sarkoris.TalentSpec, Sarkoris.Stats['TalentTree'])
##print Sarkoris.Stats
##print Sarkoris.Stats['Name']
##print Sarkoris.Stats['Class']
##print Sarkoris.Stats['Race']
##print Sarkoris.Stats['BaseStats']
##print Sarkoris.Stats['TotalStats']
##print Sarkoris.Stats['TalentTree']
