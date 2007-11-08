#------------------------------------------------------------------------------
#   File:       
#   Purpose:    
#   Author:     
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import datetime

test1 = (datetime.date(2007,10,23), "Participation", 1)
test2 = (datetime.date(2007,10,30), "Participation", 4)
test3 = (datetime.date(2007,11,02), "Loot", "Epic", "Epic Helm of Crap")
test4 = (datetime.date(2007,11,06), "Participation", 3)
Events = {"Sarkoris" : [test1, test2, test3, test4]}
Scores = {"Sarkoris" : [0, 0, 0]}

AttendanceUpper = [0.10, 0.25, 0.50, 0.75, 1.00]
PointsPerDay = [0.0, 0.4, 0.8, 1.6, 2.0]
PointDecay = [0.0, 0.0, 2.0, 4.0, 8.0, 10.0]

days = 2;

def scan_player_changes(Events, Scores):

    for Member in Events.keys():
        MemberEvents = Events[Member]
        print Member
        for index, Event in enumerate(MemberEvents):

            # deal with the current event
            if Event[1] == "Participation":
                print "participation"
                # find the days until next event
                if index < len(MemberEvents)-1:
                    NextEvent = MemberEvents[index+1]
                else:
                    NextEvent = (datetime.date.today(), "End")
                DaysElapsed = NextEvent[0] - Event[0]
                temp = add_points(Scores[Member], Event[2], DaysElapsed)
            elif Event[1] == "Loot":
                print "loot"
#                Scores(Member) = subtract_loot(Event[2], Scores[Member])
    return


def add_points(OldScores, Participation, DaysElapsed):
    NewScores = [0, 0, 0]

    # are points decaying?
    if Participation == 0:
        WeeksAtZero = days // 7.0
        ExtraDays = days - WeeksAtZero * 7
        PointsLost = 0
####
####        if WeeksAtZero > 1
####            PointsLost = PointsLost - PointDecay[0]
####        if WeeksAtZero > 1
####            PointsLost = PointsLost - PointDecay[0]

        for OldScore, NewScore in OldScores, NewScores:
            if OldScore > 0 and OldScore - PointsLost > 0:
                NewScore = OldScore - PointsLost
            elif OldScore > 0:
                NewScore = 0
            else:
                NewScore = OldScore    
        return NewScores

    # determine points to add
    PointsAdded = 0
    for CurAttendanceUpper, CurPointsPerDay in AttendanceUpper, PointsPerDay:
        if Participation < CurArrendanceUpper:
            PointsAdded = CurPointsPerDay * days

    for OldScore, NewScore in OldScores, NewScores:
        NewScore = OldScore + PointsAdded
    return NewScores

def subtract_loot(LootValue, Scores):

    return [0, 0, 0]
