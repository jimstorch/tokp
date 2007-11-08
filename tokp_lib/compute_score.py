#------------------------------------------------------------------------------
#   File:       compute_score.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import datetime
from string import lower

test1 = (datetime.date(2007,10,9), "Participation", 4)
test2 = (datetime.date(2007,10,16), "Participation", 4)
test3 = (datetime.date(2007,10,23), "Participation", 4)
test4 = (datetime.date(2007,10,30), "Participation", 0)
test5 = (datetime.date(2007,11,2), "Loot", "Rare", "Epic Helm of Crap")
test6 = (datetime.date(2007,11,2), "lOOT", "common", "Epic Pants of Crap")
test7 = (datetime.date(2007,11,6), "Participation", 0.5)
Events = {"Sarkoris" : [test1, test2, test3, test4, test5, test6, test7]}
Scores = {"Sarkoris" : [0.00, 0.00, 0.00, 0.00]}

PointsPerDay = {0.5 : 0.00, 1 : 0.40, 2: 0.80, 3: 1.60, 4 : 2.00}
PointDecay = {0:0.0, 1:0.0, 2:2.0, 3:4.0, 4:8.0, 5:10.0}
ValueCosts = {"epic":20 , "rare":6, "uncommon":3, "common":1}

def scan_player_changes(Events, Scores):

    for Member in Events.keys():
        MemberEvents = Events[Member]
        WeeksAtZero = 0;
        for index, Event in enumerate(MemberEvents):
            # deal with the current event
            if lower(Event[1]) == "participation":
                # find the days until next event
                if index < len(MemberEvents)-1:
                    NextEvent = MemberEvents[index+1]
                else:
                    NextEvent = (datetime.date.today(), "End")
                Delta = NextEvent[0] - Event[0]
                DaysElapsed = Delta.days
                # update weeks at zero
                if Event[2] == 0:
                    WeeksAtZero = WeeksAtZero + 1
                    Scores[Member] = decay_points(Scores[Member], WeeksAtZero, DaysElapsed)
                else:
                    WeeksAtZero = 0
                    Scores[Member] = add_points(Scores[Member], Event[2], DaysElapsed)
            elif lower(Event[1]) == "loot":
                Scores[Member] = subtract_loot(Event[2], Scores[Member])
            print "%4.1f %4.1f %4.1f %4.1f" % (Scores[Member][0], Scores[Member][1], Scores[Member][2], Scores[Member][3])
    return


def add_points(OldScores, Participation, DaysElapsed):
    NewScores = [0, 0, 0, 0]

    # determine points to add
    PointsAdded = PointsPerDay[Participation] * DaysElapsed
    for index, OldScore in enumerate(OldScores):
        NewScores[index] = OldScore + PointsAdded
    return NewScores

def decay_points(OldScores, WeeksAtZero, DaysElapsed):
    NewScores = [0, 0, 0, 0]

    if WeeksAtZero > 5:
        WeeksAtZero = 5
    PointsLost = PointDecay[WeeksAtZero] / 7.0 * DaysElapsed

    # make sure we don't decay past zero
    for index, OldScore in enumerate(OldScores):
        if OldScore > 0 and OldScore - PointsLost > 0:
            NewScores[index] = OldScore - PointsLost
        elif OldScore > 0 and OldScore - PointsLost < 0:
            NewScores[index] = 0
        elif OldScore <= 0:
            NewScores[index] = OldScore    
    return NewScores

def subtract_loot(LootValue, Scores):
    NewScores = [0, 0, 0, 0]

    if lower(LootValue) == "epic":
        NewScores[0] = reset_score(LootValue, Scores[0])
        NewScores[1] = reset_score(LootValue, Scores[1])
        NewScores[2] = reset_score(LootValue, Scores[2])
        NewScores[3] = reset_score(LootValue, Scores[3])
    elif lower(LootValue) == "rare":
        NewScores[0] = Scores[0] - ValueCosts[lower(LootValue)]
        NewScores[1] = reset_score(LootValue, Scores[1])
        NewScores[2] = reset_score(LootValue, Scores[2])
        NewScores[3] = reset_score(LootValue, Scores[3])
    elif lower(LootValue) == "uncommon":
        NewScores[0] = Scores[0] - ValueCosts[lower(LootValue)]
        NewScores[1] = Scores[1] - ValueCosts[lower(LootValue)]
        NewScores[2] = reset_score(LootValue, Scores[2])
        NewScores[3] = reset_score(LootValue, Scores[3])
    elif lower(LootValue) == "common":
        NewScores[0] = Scores[0] - ValueCosts[lower(LootValue)]
        NewScores[1] = Scores[1] - ValueCosts[lower(LootValue)]
        NewScores[2] = Scores[2] - ValueCosts[lower(LootValue)]
        NewScores[3] = reset_score(LootValue, Scores[3])
    else:
        print "you fucked up"
        
    return NewScores

def reset_score(LootValue, Score):

    # defined by loot system rules:
    MinCost = 20
    MaxCost = 50

    # reset cost
    ResetCost = 0.75 * Score

    # chose which cost to use
    if ResetCost < MinCost:
        NewScore = Score - MinCost
    elif ResetCost > MaxCost:
        NewScore = Score - MaxCost
    else:
        NewScore = Score - ResetCost
    
    return NewScore
