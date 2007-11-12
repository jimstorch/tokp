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
test8 = (datetime.date(2007,11,6), "Participation", 0.5)

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
    for IncScore in Sarkoris.IncScores:
        print IncScore
    #print Sarkoris.SeniorityVec
    #print Sarkoris.Seniority
    #print Sarkoris.SeniorityLastMonth
    #print Sarkoris.DebugReport
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
        #self.Scores = [0.00, 0.00, 0.00, 0.00]
        self.Scores = {1:0.00, 2:0.00, 3:0.00, 4:0.00}
        self.IncScores = []
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
        vecIncScores = ()

        # loop through member events
        for index, Event in enumerate(self.MemberEvents):

            # find the days until next event
            DaysElapsed = self.get_days_elapsed(index, Event)  
            NewDebugLine = self.debug_line_start(Event, DaysElapsed)

            # "add member" event
            if lower(Event[1]) == "add member":
                NewDebugLine = NewDebugLine + ("%-20s [%-8s] " % (Event[1], ""))
            # "participation" event
            elif lower(Event[1]) == "participation":
                self.SeniorityVec.append(Event[2])
                NewDebugLine = NewDebugLine + ("%-20s [%-8d] " % (Event[1], Event[2]))
                if Event[2] == 0:
                    self.WeeksAtZero = self.WeeksAtZero + 1
                    self.decay_points(DaysElapsed)
                else:
                    self.WeeksAtZero = 0
                    self.add_points(Event[2], DaysElapsed)
            # "loot" event
            elif lower(Event[1]) == "loot":
                NewDebugLine = NewDebugLine + ("%-20s [%-8s] " % (Event[3], Event[2]))
                self.subtract_loot(Event[2])
            # "bonus" event
            elif lower(Event[1]) == "bonus":
                NewDebugLine = NewDebugLine + ("%-20s [%-8d] " % (Event[3], Event[2]))
                self.bonus_points(Event[2], Event[3])
            NewDebugLine = self.debug_line_end(NewDebugLine)
            self.inc_scores(Event[0],DaysElapsed,capwords(Event[1]),self.Scores)
        # update seniority
        self.update_seniority()
        return

    def debug_line_start(self, Event, DaysElapsed):
        NewDebugLine = ""
        NewDebugLine = NewDebugLine + "[" + Event[0].strftime('%Y-%m-%d') + "] "
        NewDebugLine = NewDebugLine + ("[%d] " % DaysElapsed)
        NewDebugLine = NewDebugLine + "["
        for Score in self.Scores:
            NewDebugLine = NewDebugLine + (" %3d" % Score)
        NewDebugLine = NewDebugLine + " ] "
        return NewDebugLine

    def debug_line_end(self, NewDebugLine):
        NewDebugLine = NewDebugLine + "["
        for Score in self.Scores:
            NewDebugLine = NewDebugLine + (" %3d" % Score)
        NewDebugLine = NewDebugLine + " ]\n"
        self.DebugReport = self.DebugReport + NewDebugLine
        return

    def inc_scores(self, Date, DaysElapsed, Event, Scores):
        tempIncScores = {}
        tempIncScores["Date"] = Date
        tempIncScores["DaysElapsed"] = DaysElapsed
        tempIncScores["Event"] = Event
        tempIncScores["Scores"] = Scores
        self.IncScores.append(tempIncScores)
        return
                            
    def add_points(self, Participation, DaysElapsed):
        # determine points to add
        PointsAdded = self.PointsPerDay[Participation] * DaysElapsed
        for index in self.Scores.keys():
            self.Scores[index] = self.Scores[index] + PointsAdded
        return

    def decay_points(self, DaysElapsed):
        # decay saturates at 5 weeks
        if self.WeeksAtZero > 5:
            self.WeeksAtZero = 5

        # find points lost based on weeks inactive
        PointsLost = self.PointDecay[self.WeeksAtZero] / 7.0 * DaysElapsed

        # make sure we don't decay past zero
        for index in self.Scores.keys():
            if self.Scores[index] > 0 and self.Scores[index] - PointsLost > 0:
                self.Scores[index] = self.Scores[index] - PointsLost
            elif self.Scores[index] > 0 and self.Scores[index] - PointsLost < 0:
                self.Scores[index] = 0
            elif self.Scores[index] <= 0:
                self.Scores[index] = self.Scores[index]   
        return

    def subtract_loot(self, LootValue):
        # pull out the index for the loot value:
        # reset equal and less valuable scores
        # subtract from more valuable scores
        LootValueIndex = self.ValueLabels[lower(LootValue)]
        for index in self.Scores.keys():
            if index >= LootValueIndex:
                self.Scores[index] = self.reset_score(self.Scores[index])
            else:
                self.Scores[index] = self.Scores[index] - self.ValueCosts[LootValueIndex]
        return                

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
        for index in self.Scores.keys():
            self.Scores[index] = self.Scores[index] + Bonus
        return

    def update_seniority(self):
        self.Seniority = sum(self.SeniorityVec)
        self.SeniorityLastMonth = sum(self.SeniorityVec[len(self.SeniorityVec)-4:])
        return

#------------------------------------------------------------------------------
    
