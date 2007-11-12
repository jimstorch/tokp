#------------------------------------------------------------------------------
#   File:       compute_score.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import datetime
import string
from string import lower
from string import capwords

test0 = (datetime.date(2007,10,9), "Add Member")
test1 = (datetime.date(2007,10,9), "Participation", 4)
test2 = (datetime.date(2007,10,16), "Participation", 4)
test3 = (datetime.date(2007,10,23), "Participation", 4)
test4 = (datetime.date(2007,10,30), "Participation", 0)
test5 = (datetime.date(2007,11,1), "Bonus", 10, "a very good reason")
test6 = (datetime.date(2007,11,2), "Loot", "Rare", "Epic Helm of Crap")
test7 = (datetime.date(2007,11,2), "lOOT", "ZG", "Epic Pants of Crap")
test8 = (datetime.date(2007,11,6), "Participation", 0)

test9 = (datetime.date(2007,10,9), "Participation", 4)
test10 = (datetime.date(2007,10,16), "Participation", 4)
test11 = (datetime.date(2007,10,23), "Participation", 4)
test12 = (datetime.date(2007,10,30), "Participation", 0)
test13 = (datetime.date(2007,11,6), "Participation", 0.5)
Events = {"Sarkoris" : [test0, test1, test2, test3, test4, test5, test6, test7, test8],
          "Lias": [test0, test9, test10, test11, test12, test13]}

def test_stuff(Events):
    Scores = {}
    IncScores = ()
    Seniority = {}
    # loop through members
    for Member in Events.keys():
        MemberEvents = Events[Member]
        Sarkoris = GuildMember()
        Sarkoris.ScanMemberEvents(MemberEvents)
    #print Sarkoris.Scores
    #for IncScore in Sarkoris.IncScores:
    #    print IncScore
    #print Sarkoris.SeniorityVec
    #print Sarkoris.Seniority
    #print Sarkoris.SeniorityLastMonth
    print Sarkoris.DebugReport
    return

#--[ ComputeScore Class ]------------------------------------------------------
class GuildMember(object):
    
    # defined by loot system rules:
    PointsPerDay = {0.5:0.00, 1:0.82, 2:1.29, 3:1.68, 4:2.00}
    PointDecay = {0:0.0, 1:0.0, 2:2.0, 3:4.0, 4:8.0, 5:10.0}
    ValueLabels = {"epic":1, "rare":2, "uncommon":3, "zg":4}
    ValueCosts = {1:20 , 2:6, 3:3, 4:1}
    MinCost = 20
    MaxCost = 50

    def __init__(self):
        self.MemberEvents = []
        self.Scores = {1:0.00, 2:0.00, 3:0.00, 4:0.00}
        self.IncScores = []
        self.IncDaysElapsed = []
        self.SeniorityVec = []
        self.Seniority = 0;
        self.SeniorityLastMonth = 0;
        self.DebugReport = ""

    def get_days_elapsed(self, index, Event):
        if index < len(self.MemberEvents)-1:
            NextEvent = self.MemberEvents[index+1]
        else:
            NextEvent = (datetime.date.today(), "End")
        Delta = NextEvent[0] - Event[0]
        return Delta.days

    def ScanMemberEvents(self, MemberEvents):
        self.MemberEvents = MemberEvents
        self.WeeksAtZero = 0;
        NewScores = {}

        # loop through member events
        for index, Event in enumerate(self.MemberEvents):

            # find the days until next event
            DaysElapsed = self.get_days_elapsed(index, Event)
            self.IncDaysElapsed.append(DaysElapsed)

            # "add member" event
            if lower(Event[1]) == "add member":
                NewScores = {1:0, 2:0, 3:0, 4:0}
            # "participation" event
            elif lower(Event[1]) == "participation":
                self.SeniorityVec.append(Event[2])
                if Event[2] == 0:
                    self.WeeksAtZero = self.WeeksAtZero + 1
                    NewScores = self.decay_points(DaysElapsed)
                else:
                    self.WeeksAtZero = 0
                    NewScores = self.add_points(Event[2], DaysElapsed)
            # "loot" event
            elif lower(Event[1]) == "loot":
                NewScores = self.subtract_loot(Event[2])
            # "bonus" event
            elif lower(Event[1]) == "bonus":
                NewScores = self.bonus_points(Event[2], Event[3])

            self.IncScores.append(NewScores)
            self.Scores = NewScores
        # update seniority
        self.update_seniority()
        self.update_debug()
        return

    def add_points(self, Participation, DaysElapsed):
        NewScores = {}
        # determine points to add
        PointsAdded = self.PointsPerDay[Participation] * DaysElapsed
        for index in self.Scores.keys():
            NewScores[index] = self.Scores[index] + PointsAdded
        return NewScores

    def decay_points(self, DaysElapsed):
        NewScores = {}
        
        # decay saturates at 5 weeks
        if self.WeeksAtZero > 5:
            self.WeeksAtZero = 5

        # find points lost based on weeks inactive
        PointsLost = self.PointDecay[self.WeeksAtZero] / 7.0 * DaysElapsed

        # make sure we don't decay past zero
        for index in self.Scores.keys():
            if self.Scores[index] > 0 and self.Scores[index] - PointsLost > 0:
                NewScores[index] = self.Scores[index] - PointsLost
            elif self.Scores[index] > 0 and self.Scores[index] - PointsLost < 0:
                NewScores[index] = 0
            elif self.Scores[index] <= 0:
                NewScores[index] = self.Scores[index]   
        return NewScores

    def subtract_loot(self, LootValue):
        # pull out the index for the loot value:
        # reset equal and less valuable scores
        # subtract from more valuable scores
        NewScores = {}
        LootValueIndex = self.ValueLabels[lower(LootValue)]
        for index in self.Scores.keys():
            if index >= LootValueIndex:
                NewScores[index] = self.reset_score(self.Scores[index])
            else:
                NewScores[index] = self.Scores[index] - self.ValueCosts[LootValueIndex]
        return NewScores

    def reset_score(self, Score):
        # reset cost
        ResetCost = 0.75 * Score
        # chose which cost to use
        if ResetCost < self.MinCost:
            NewScore = Score - self.MinCost
        elif ResetCost > self.MaxCost:
            NewScore = Score - self.MaxCost
        else:
            NewScore = Score - ResetCost
        return NewScore

    def bonus_points(self, Bonus, Reason):
        NewScores = {}
        for index in self.Scores.keys():
            NewScores[index] = self.Scores[index] + Bonus
        return NewScores

    def update_seniority(self):
        self.Seniority = sum(self.SeniorityVec)
        self.SeniorityLastMonth = sum(self.SeniorityVec[len(self.SeniorityVec)-4:])
        return

    def update_debug(self):
        self.DebugReport = ""
        for index, Event in enumerate(self.MemberEvents):
            if index > 0:
                OldScores = self.IncScores[index-1]
            else:
                OldScores = {1:0, 2:0, 3:0, 4:0}
            if index < len(self.MemberEvents):
                NewScores = self.IncScores[index]
            else:
                NewScores = self.Scores
            DaysElapsed = self.IncDaysElapsed[index]
        
            NewDebugLine = ""
            NewDebugLine = NewDebugLine + "[" + Event[0].strftime('%Y-%m-%d') + "] "
            NewDebugLine = NewDebugLine + ("[%d] " % DaysElapsed)
            NewDebugLine = NewDebugLine + "["
            for index in OldScores.keys():
                NewDebugLine = NewDebugLine + (" %3d" % OldScores[index])
            NewDebugLine = NewDebugLine + " ] "
            if lower(Event[1]) == "add member":
                 NewDebugLine = NewDebugLine + ("%-20s [%-8s] " % (Event[1], ""))
            elif lower(Event[1]) == "participation":
                NewDebugLine = NewDebugLine + ("%-20s [%-8d] " % (Event[1], Event[2]))
            elif lower(Event[1]) == "loot":
                NewDebugLine = NewDebugLine + ("%-20s [%-8s] " % (Event[3], Event[2]))
            elif lower(Event[1]) == "bonus":
                NewDebugLine = NewDebugLine + ("%-20s [%-8d] " % (Event[3], Event[2]))
            NewDebugLine = NewDebugLine + "["
            for index in NewScores.keys():
                NewDebugLine = NewDebugLine + (" %3d" % NewScores[index])
            NewDebugLine = NewDebugLine + " ]\n"
            self.DebugReport = self.DebugReport + NewDebugLine
#------------------------------------------------------------------------------
    
