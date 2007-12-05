#------------------------------------------------------------------------------
#   File:       warlock_dps.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

'''
Quantify ideal Warlock dps based on talents and spell selection
'''

from warlock_class import Warlock

## Define the Warlock
Lavode = Warlock()

## Define the Spec
Lavode.SetCommonSpec('UADR')

## Define the fight duration [sec]
fight_duration = 10 * 60

## Begin the fight
current_time = 0
actions = {}
current_dot = []
while current_time < fight_duration:
    current_time += 0.1
    
# 
