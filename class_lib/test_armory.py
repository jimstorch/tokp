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
print Sarkoris.Name
print Sarkoris.Class
print Sarkoris.Race
print Sarkoris.Stats
##print Sarkoris.TalentSpec
##print Sarkoris.Stats['Name']
##print Sarkoris.Stats['Class']
##print Sarkoris.Stats['Race']
print Sarkoris.Stats['BaseStats']
print Sarkoris.Stats['TotalStats']
print Sarkoris.Stats['TalentTree']
