#------------------------------------------------------------------------------
#   File:       system_rules.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import datetime

# defined by loot system rules:
SystemStartDate = datetime.datetime(2008,11,13,6,0)
RaidWeekStart = 2
PartFactor = {0.5:0.00, 1:0.10, 2:0.25, 3:0.50, 4:0.75}
PointsPerDay = {0.5:0.00, 1:0.82, 2:1.29, 3:1.68, 4:2.00}
PointDecay = {0:0.0, 1:0.0, 2:2.0, 3:4.0, 4:8.0, 5:10.0}
ValueLabels = {"epic":1, "rare":2, "uncommon":3, "zg":4, "special":5}
RevValueLabels = {1:"epic", 2:"rare", 3:"uncommon", 4:"zg", 5:"special"}
ValueCosts = {1:20 , 2:6, 3:3, 4:1, 5:0}
MinCost = 20
MaxCost = 50
ResetPercent = 0.75
MinPoints = -50
MaxPoints = 150


def subtract_loot(OldScores, LootValueIndex):
    # reset equal and less valuable scores
    # subtract from more valuable scores
    NewScores = {}
    #print OldScores
    #print LootValueIndex
    for index in OldScores.keys():
        #print index
        if index >= LootValueIndex:
            NewScores[index] = reset_score(OldScores[index])
        else:
            NewScores[index] = OldScores[index] - ValueCosts[LootValueIndex]
        if NewScores[index] < MinPoints:
            NewScores[index] = MinPoints
    #print OldScores, LootValueIndex, NewScores
    return NewScores

def reset_score(OldScore):
    if 1:
        # this is the old system, here for posterity
        # reset cost
        ResetCost = ResetPercent * OldScore
        # chose which cost to use
        if ResetCost < MinCost:
            NewScore = OldScore - MinCost
        elif ResetCost > MaxCost:
            NewScore = OldScore - MaxCost
        else:
            NewScore = OldScore - ResetCost
    else:
        NewScore = OldScore
    return NewScore