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

from warlock_class_armory import Warlock
from spell_rotation import SpellRotation

## Assumptions
Assumptions = {'SW':5,
               'Misery':5,
               'ISB':5}

## Define the Warlock
Lavode = Warlock('Lavode','Alleria','US',Assumptions)

## Define the Spec
##Lavode.SetCommonSpec('UADR')

##temp = [Lavode.Nuke['SB'], Lavode.Nuke['SB']]
##SB_only = SpellRotation(temp)
##print SB_only.TotalDamage
##print SB_only.TotalCastTime
##print SB_only.TotalManaCost
##print SB_only.DPS
##print SB_only.DPM

#### Define the fight duration [sec]
##fight_duration = 10 * 60
##
#### Begin the fight
##current_time = 0
##current_action = {}
##all_actions = []
##current_dot = []
##while current_time < fight_duration:
##    ## If the cast time has expired, clear the current action
##    if not current_action == {}:
##        if (current_action['Time'] + current_action['Cast'] < current_time):
##            current_action = {}
##    
##    ## Tick all DoTs
##    for dot in current_dot
##        tick = tick_dot(Lavode, dot, current_time)
##        all_actions.append(tick)
##
##    ## If no current action, choose a new current action
##    if current_action == {}
##        current_action = choose_next_spell(Lavode, current_dot)
##
##    ## Increase time and loop
##    current_time += 0.1
##    
## 
##def tick_dot(Warlock, DoT, current_time):
##    TickDamage = 0
##    Tick = {'Time':current_time,
##            'Spell':DoT['Name'],
##            'Damage':TickDamage
##            }
##    return Tick
