#------------------------------------------------------------------------------
#   File:       compute_score.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import datetime
import string
#from string import lower

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
    #print Sarkoris.IncScores
    print Sarkoris.SeniorityVec
    print Sarkoris.Seniority
    print Sarkoris.SeniorityLastMonth
    #print Sarkoris.DebugReport
    return

#--[ ComputeScore Class ]------------------------------------------------------
class GuildMember(object):
    
    # defined by loot system rules:
    PointsPerDay = {0.5:0.00, 1:0.82, 2:1.29, 3:1.68, 4:2.00}
    PointDecay = {0:0.0, 1:0.0, 2:2.0, 3:4.0, 4:8.0, 5:10.0}
    ValueCosts = {"epic":20 , "rare":6, "uncommon":3, "zg":1}
    MinCost = 20
    MaxCost = 50

    def __init__(self):
        self.MemberEvents = []
        self.Scores = [0.00, 0.00, 0.00, 0.00]
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

        # loop through member events
        for index, Event in enumerate(self.MemberEvents):
            NewDebugLine = ""
            # find the days until next event
            DaysElapsed = self.get_days_elapsed(index, Event)  

            # store old scores, days elapsed
            NewDebugLine = NewDebugLine + "[" + Event[0].strftime('%Y-%m-%d') + "] "
            NewDebugLine = NewDebugLine + ("[%d] " % DaysElapsed)
            NewDebugLine = NewDebugLine + "["
            for Score in self.Scores:
                NewDebugLine = NewDebugLine + (" %3d" % Score)
            NewDebugLine = NewDebugLine + " ] "
            #self.IncScores[Event[0]] = []
            #self.IncScores[Event[0]].append(self.Scores)
            #self.IncScores[Event[0]].append(DaysElapsed)
            #print self.Scores

            if lower(Event[1]) == "add member":
                NewDebugLine = NewDebugLine + ("%-20s [%-8s] " % (Event[1], ""))
            elif lower(Event[1]) == "participation":
                self.SeniorityVec.append(Event[2])
                NewDebugLine = NewDebugLine + ("%-20s [%-8d] " % (Event[1], Event[2]))

                # update weeks at zero
                if Event[2] == 0:
                    self.WeeksAtZero = self.WeeksAtZero + 1
                    self.decay_points(DaysElapsed)
                else:
                    self.WeeksAtZero = 0
                    self.add_points(Event[2], DaysElapsed)
            elif lower(Event[1]) == "loot":
                NewDebugLine = NewDebugLine + ("%-20s [%-8s] " % (Event[3], Event[2]))
                self.subtract_loot(Event[2])
            elif lower(Event[1]) == "bonus":
                NewDebugLine = NewDebugLine + ("%-20s [%-8d] " % (Event[3], Event[2]))
                self.bonus_points(Event[2], Event[3])
            # store updated scores
            #self.IncScores[Event[0]].append(self.Scores)
            #print self.IncScores[Event[0]]
            NewDebugLine = NewDebugLine + "["
            for Score in self.Scores:
                NewDebugLine = NewDebugLine + (" %3d" % Score)
            NewDebugLine = NewDebugLine + " ]\n"
            self.DebugReport = self.DebugReport + NewDebugLine
            self.update_seniority()
        return


    def add_points(self, Participation, DaysElapsed):
        # determine points to add
        PointsAdded = self.PointsPerDay[Participation] * DaysElapsed
        for index, OldScores in enumerate(self.Scores):
            self.Scores[index] = self.Scores[index] + PointsAdded
        return

    def decay_points(self, DaysElapsed):
        # decay saturates at 5 weeks
        if self.WeeksAtZero > 5:
            self.WeeksAtZero = 5

        # find points lost based on weeks inactive
        PointsLost = self.PointDecay[self.WeeksAtZero] / 7.0 * DaysElapsed

        # make sure we don't decay past zero
        for index, OldScore in enumerate(self.Scores):
            if self.Scores[index] > 0 and self.Scores[index] - PointsLost > 0:
                self.Scores[index] = self.Scores[index] - PointsLost
            elif self.Scores[index] > 0 and self.Scores[index] - PointsLost < 0:
                self.Scores[index] = 0
            elif self.Scores[index] <= 0:
                self.Scores[index] = self.Scores[index]   
        return

    def subtract_loot(self, LootValue):
        if lower(LootValue) == "epic":
            # reset epic, rare, uncommon, common
            # subtract epic value from none
            self.Scores[0] = self.reset_score(LootValue, self.Scores[0])
            self.Scores[1] = self.reset_score(LootValue, self.Scores[1])
            self.Scores[2] = self.reset_score(LootValue, self.Scores[2])
            self.Scores[3] = self.reset_score(LootValue, self.Scores[3])
        elif lower(LootValue) == "rare":
            # reset rare, uncommon, common
            # subtract epic value from epic
            self.Scores[0] = self.Scores[0] - self.ValueCosts[lower(LootValue)]
            self.Scores[1] = self.reset_score(LootValue, self.Scores[1])
            self.Scores[2] = self.reset_score(LootValue, self.Scores[2])
            self.Scores[3] = self.reset_score(LootValue, self.Scores[3])
        elif lower(LootValue) == "uncommon":
            # reset uncommon, common
            # subtract epic value from epic, rare
            self.Scores[0] = self.Scores[0] - self.ValueCosts[lower(LootValue)]
            self.Scores[1] = self.Scores[1] - self.ValueCosts[lower(LootValue)]
            self.Scores[2] = self.reset_score(LootValue, self.Scores[2])
            self.Scores[3] = self.reset_score(LootValue, self.Scores[3])
        elif lower(LootValue) == "zg":
            # reset common
            # subtract epic value from epic, rare, uncommon
            self.Scores[0] = self.Scores[0] - self.ValueCosts[lower(LootValue)]
            self.Scores[1] = self.Scores[1] - self.ValueCosts[lower(LootValue)]
            self.Scores[2] = self.Scores[2] - self.ValueCosts[lower(LootValue)]
            self.Scores[3] = self.reset_score(LootValue, self.Scores[3])
        else:
            print "you fucked up"
            
        return

    def reset_score(self, LootValue, Score):
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
        for index, OldScore in enumerate(self.Scores):
            self.Scores[index] = self.Scores[index] + Bonus
        return

    def update_seniority(self):
        self.Seniority = sum(self.SeniorityVec)
        self.SeniorityLastMonth = sum(self.SeniorityVec[len(self.SeniorityVec)-4:])
        return

#------------------------------------------------------------------------------
    
