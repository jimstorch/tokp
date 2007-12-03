#------------------------------------------------------------------------------
#   File:       compute_score.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import datetime
from string import capwords, lower

from tokp_lib.xml_store import read_raid_xml, raid_files
from tokp_lib.raidweeks_xml import RaidWeek, raidweek_output
import tokp_lib.system_rules as Rules

#--[ Guild Class ]-------------------------------------------------------------
class Guild(object):

    def __init__(self):
        self.MemberList = {}
        self.RaidWeeks = {}
        self.AllRaids = {}
        self.AllLoots = {}
        self.DebugReport = ""
        self.LootByPerson = ""
        self.LootByDate = ""
        self.LootByBoss = ""
        return

    def LoadRaids(self):
        file_list = raid_files()
        for fname in file_list:
            if not fname == "raidweeks":
                self.AllRaids[fname] = read_raid_xml(fname+'.xml')
        self.parse_all_raids()
        return

    def parse_all_raids(self):
        # sort all raids and loots into raidweek buckets
        for index in self.AllRaids.keys():
            str_raidweek = raidweek_output(Rules.RaidWeekStart, self.AllRaids[index].start_time)
            if str_raidweek not in self.RaidWeeks.keys():
               self.RaidWeeks[str_raidweek] = RaidWeek(str_raidweek)
            self.RaidWeeks[str_raidweek].add_member(self.AllRaids[index])
        return

    def add_member(self, Member):
        self.MemberList[Member] = GuildMember(Member)
        return

    def del_member(self, Member):
        self.MemberList.remove(Member.Name)
        return

    def ComputeAttendance(self):
        # compute participation in each week
        Attendance = []
        for Week in self.RaidWeeks.keys():
            WeekAttendance = {}
            for CurRaid in self.RaidWeeks[Week].Raids:
                for Member in CurRaid.raid_members:
                    if Member not in self.MemberList.keys():
                        self.add_member(Member)
                    if Member not in WeekAttendance.keys():
                        WeekAttendance[Member] = 0
                    WeekAttendance[Member] += float(1) / float(self.RaidWeeks[Week].NumRaidsThisWeek)
            # store the weekly participation event for each member
            for Member in self.MemberList.keys():
                if Member in WeekAttendance.keys():
                    self.MemberList[Member].add_participation(self.RaidWeeks[Week].AttendanceDate, WeekAttendance[Member])
                else:
                    self.MemberList[Member].add_participation(self.RaidWeeks[Week].AttendanceDate, 0)
        return

    def parse_loot(self, LootList):
        return

    def UpdateReports(self):
        TempDebugReport = ""
        TempLootByPerson = ""
        for Member in self.MemberList.keys():
            self.MemberList[Member].ScanMemberEvents()
            TempDebugReport += ("%s\n%s\n" % (self.MemberList[Member].Name, self.MemberList[Member].DebugReport))
            TempLootByPerson += ("%s\n" % self.MemberList[Member].LootByPerson)
        self.update_debug(TempDebugReport)
        self.update_lootbyperson(TempLootByPerson)

    def update_debug(self, TempDebugReport):
        self.DebugReport += ("Last updated: %s\n\n" % (datetime.date.today().strftime('%Y-%m-%d')))
        self.DebugReport += TempDebugReport

        DebugReport = open('debug.txt','w')
        DebugReport.write(self.DebugReport)
        DebugReport.close()
        return

    def update_lootbyperson(self, TempLootByPerson):
        self.LootByPerson += ("Last updated: %s\n\n" % (datetime.date.today().strftime('%Y-%m-%d')))
        self.LootByPerson += 'Date       Mob               Item                               Value    $$$  Person      \n'
        self.LootByPerson += '------------------------------------------------------------------------------------------\n'
        self.LootByPerson += TempLootByPerson

        LootByPerson = open('lootbyperson.txt','w')
        LootByPerson.write(self.LootByPerson)
        LootByPerson.close()
        return

#--[ GuildMember Class ]-------------------------------------------------------
class GuildMember(object):

    def __init__(self, str_Name):
        self.Name = str_Name
        self.MemberEvents = []
        self.Scores = {1:0.00, 2:0.00, 3:0.00, 4:0.00}
        self.IncScores = []
        self.IncDaysElapsed = []
        self.SeniorityVec = []
        self.Seniority = 0;
        self.SeniorityLastMonth = 0;
        self.DebugReport = ""
        self.LootByPerson = ""
        return

    def add_participation(self, attendance_date, attendance):
        new_factor = 0
        for factor in Rules.PartFactor.keys():
            if attendance > Rules.PartFactor[factor]:
                new_factor = factor
            else:
                break
        NewEvent = (attendance_date, "Participation", new_factor)
        self.add_event(NewEvent)
        return

    def add_event(self, NewEvent):
        self.MemberEvents.append(NewEvent)
        self.MemberEvents.sort()
        return

    def del_event(self, DelEvent):
        self.MemberEvents.remove(DelEvent)
        return

    def get_days_elapsed(self, index, Event):
##        if index < len(self.MemberEvents)-1:
##            NextEvent = self.MemberEvents[index+1]
##        else:
##            NextEvent = (datetime.date.today(), "Today")
##        Delta = NextEvent[0] - Event[0]
        if index == 0:
            PrevEvent = self.MemberEvents[0]
        else:
            PrevEvent = self.MemberEvents[index-1]
        Delta = Event[0] - PrevEvent[0]
        return Delta.days

    def StoreMemberEvents(self, MemberEvents):
        self.MemberEvents = MemberEvents
        return

    def ScanMemberEvents(self):
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
                NewScores = self.bonus_points(Event[2])

            self.IncScores.append(NewScores)
            self.Scores = NewScores
        # update seniority
        self.update_seniority()
        self.update_debug()
        self.update_lootbyperson()
        return

    def add_points(self, Participation, DaysElapsed):
        NewScores = {}
        # determine points to add
        PointsAdded = Rules.PointsPerDay[Participation] * DaysElapsed
        for index in self.Scores.keys():
            NewScores[index] = self.Scores[index] + PointsAdded
        return NewScores

    def decay_points(self, DaysElapsed):
        NewScores = {}
        
        # decay saturates at 5 weeks
        if self.WeeksAtZero > 5:
            self.WeeksAtZero = 5

        # find points lost based on weeks inactive
        PointsLost = Rules.PointDecay[self.WeeksAtZero] / 7.0 * DaysElapsed

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
        ResetCost = Rules.ResetPercent * Score
        # chose which cost to use
        if ResetCost < Rules.MinCost:
            NewScore = Score - Rules.MinCost
        elif ResetCost > Rules.MaxCost:
            NewScore = Score - Rules.MaxCost
        else:
            NewScore = Score - ResetCost
        return NewScore

    def bonus_points(self, Bonus):
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
            NewDebugLine += ("[%s] [%2d] " % (Event[0].strftime('%Y-%m-%d'), DaysElapsed))
            NewDebugLine += ("[%3.0f %3.0f %3.0f] " % (OldScores[1], OldScores[2], OldScores[3]))
            if lower(Event[1]) == "add member":
                 NewDebugLine = NewDebugLine + ("%-20s [%-8s] " % (Event[1], ""))
            elif lower(Event[1]) == "participation":
                NewDebugLine += ("%-20s [%-8d] " % (Event[1], Event[2]))
            elif lower(Event[1]) == "loot":
                NewDebugLine += ("%-20s [%-8s] " % (Event[3], Event[2]))
            elif lower(Event[1]) == "bonus":
                NewDebugLine += ("%-20s [%-8d] " % (Event[3], Event[2]))
            NewDebugLine += ("[%3.0f %3.0f %3.0f]\n" % (NewScores[1], NewScores[2], NewScores[3]))
            self.DebugReport += NewDebugLine
        NewDebugLine = ""
        NewDebugLine += ("[%s] [%2d] " % (datetime.date.today().strftime('%Y-%m-%d'), DaysElapsed))
        NewDebugLine += ("[%3.0f %3.0f %3.0f] Today\n" % (NewScores[1], NewScores[2], NewScores[3]))
        self.DebugReport += NewDebugLine
        return

    def update_lootbyperson(self):
        EventDate = datetime.date(2000,01,01)
        first_loot = 1
        for Event in self.MemberEvents:
            if lower(Event[1]) == "loot":
                if first_loot:
                    str_Name = ("%11s " % self.Name)
                    first_loot = 0
                else:
                    str_Name = ("%11s " % "")
                if EventDate == Event[0]:
                    str_EventDate = ("%10s " % "")
                else:
                    str_EventDate = EventDate.strftime('%Y-%m-%d')
                EventDate = Event[0]
                self.LootByPerson += str_Name
                self.LootByPerson += str_EventDate
                self.LootByPerson += ("%40s " % Event[3])
                self.LootByPerson += ("%8s " % Event[2])
                self.LootByPerson += "\n"
        return
    
#------------------------------------------------------------------------------


