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
test8 = (datetime.date(2007,10,9), "Participation", 4)
test9 = (datetime.date(2007,10,16), "Participation", 4)
test10 = (datetime.date(2007,10,23), "Participation", 4)
test11 = (datetime.date(2007,10,30), "Participation", 0)
test12 = (datetime.date(2007,11,6), "Participation", 0.5)
Events = {"Sarkoris" : [test1, test2, test3, test4, test5, test6, test7],
          "Lias": [test8, test9, test10, test11, test12]}

def test_stuff(Events):
    Scores = {}
    IncScores = {}
    Seniority = {}
    # loop through members
    for Member in Events.keys():
        MemberEvents = Events[Member]
        Stuff = ComputeScore(MemberEvents)
        Scores[Member] = Stuff.return_scores()
        IncScores[Member] = Stuff.return_incscores()
        Seniority[Member] = Stuff.return_seniority()
    #print Scores
    print IncScores["Sarkoris"]
    #print Seniority
    return

#--[ ComputeScore Class ]------------------------------------------------------
class ComputeScore(object):
    
    # defined by loot system rules:
    PointsPerDay = {0.5 : 0.00, 1 : 0.40, 2: 0.80, 3: 1.60, 4 : 2.00}
    PointDecay = {0:0.0, 1:0.0, 2:2.0, 3:4.0, 4:8.0, 5:10.0}
    ValueCosts = {"epic":20 , "rare":6, "uncommon":3, "common":1}
    MinCost = 20
    MaxCost = 50

    def __init__(self, MemberEvents):
        self.MemberEvents = MemberEvents
        self.Scores = [0.00, 0.00, 0.00, 0.00]
        self.IncScores = {}
        self.Seniority = []
        self.scan_player_changes()

    def return_scores(self):
        return self.Scores

    def return_incscores(self):
        return self.IncScores

    def return_seniority(self):
        return self.Seniority

    def print_scores(self):
        # stupid, i know, but it simplifies one line!
        print "%4.1f %4.1f %4.1f %4.1f" % (self.Scores[0], self.Scores[1], self.Scores[2], self.Scores[3])
        return

    def scan_player_changes(self):
        self.WeeksAtZero = 0;

        # loop through member events
        for index, Event in enumerate(self.MemberEvents):
            # find the days until next event
            if index < len(self.MemberEvents)-1:
                NextEvent = self.MemberEvents[index+1]
            else:
                NextEvent = (datetime.date.today(), "End")
            Delta = NextEvent[0] - Event[0]
            DaysElapsed = Delta.days

            # store old scores, days elapsed
            CurDate = Event[0]
            CurScores = self.Scores
            self.IncScores[CurDate] = []
            self.IncScores[CurDate].append(CurScores)
            self.IncScores[CurDate].append(DaysElapsed)
            print self.Scores

            if lower(Event[1]) == "participation":
                self.Seniority.append(Event[2])

                # update weeks at zero
                if Event[2] == 0:
                    self.WeeksAtZero = self.WeeksAtZero + 1
                    self.decay_points(DaysElapsed)
                else:
                    self.WeeksAtZero = 0
                    self.add_points(Event[2], DaysElapsed)
            elif lower(Event[1]) == "loot":
                self.subtract_loot(Event[2])

            # store updated scores
            self.IncScores[CurDate].append(self.Scores)
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
        elif lower(LootValue) == "common":
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
#------------------------------------------------------------------------------
    
