#------------------------------------------------------------------------------
#   File:       compute_score.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import datetime
from string import capwords, lower

import os
import glob
import re
import datetime
from tokp_lib.parse_combat import Raid
from tokp_lib.parse_chat import Loot
from tokp_lib.xml_store import read_raid_xml, raid_files
from tokp_lib.raidweeks_xml import RaidWeek, RaidWeeksXML, raidweek_output
import tokp_lib.system_rules as Rules

#--[ Guild Class ]-------------------------------------------------------------
class Guild(object):

    def __init__(self):
        self.MemberList = {}
        self.RaidWeeks = {}
        self.AllRaids = {}
        self.AllLoots = {}
        self.DebugReport = ""
        self.ScoresReport = ""
        self.LootByPerson = ""
        self.LootByDate = ""
        self.LootByBoss = ""
        self.Seniority = ""
        return

    def LoadAll(self):
        RaidWeeks = RaidWeeksXML()
        RaidWeeks.LoadRaidWeeks()
        #print RaidWeeks.RaidWeeks
        for str_raid_week in RaidWeeks.RaidWeeks:
            #print str_raid_week
            raidfiles = glob.glob('data/raids/%s/*.raid' % str_raid_week)
            lootfiles = glob.glob('data/raids/%s/*.loot' % str_raid_week)
            #print raidfiles
            #print lootfiles
            if str_raid_week not in self.RaidWeeks.keys():
                self.RaidWeeks[str_raid_week] = RaidWeek(str_raid_week)
            for raidfile in raidfiles:
                self.RaidWeeks[str_raid_week].add_raid(self.read_raidfile(raidfile))
            for lootfile in lootfiles:
                self.RaidWeeks[str_raid_week].add_loot(self.read_lootfile(lootfile))
            #print self.RaidWeeks[str_raid_week].Raids
            #print self.RaidWeeks[str_raid_week].Loots
        return

    def read_raidfile(self, raidfile):
        ## Regex for raid files
        fname_str = r'.*[/\\](?P<fname>.+)\.raid'
        fname_obj = re.compile(fname_str)
        match_obj = fname_obj.search(raidfile)
        fname = match_obj.group('fname')
        ## Slice fname into date and zone
        start = datetime.datetime(int(fname[0:4]),int(fname[5:7]),int(fname[8:10]),20,0)
        zone = fname[11:len(fname)]
        ## Make Raid class
        raid = Raid(zone,start)
        ## Regex for raid files
        membername_str = r'(?P<membername>.+) \((?P<memberlevel>.+)\)'
        membername_obj = re.compile(membername_str)
        ## Add everyone from file to raid
        raidfileID = open(raidfile, 'rU')
        for line_number, line in enumerate(raidfileID):
            #print line
            match_obj = membername_obj.search(line)
            if match_obj:
                raid.add_member(match_obj.group('membername'))
                #print match_obj.group('membername')
        #print raid.raid_members
        return raid
        
    def read_lootfile(self, lootfile):
        ## Regex for loot files
        fname_str = r'.*[/\\](?P<fname>.+)\.loot'
        fname_obj = re.compile(fname_str)
        match_obj = fname_obj.search(lootfile)
        fname = match_obj.group('fname')
        ## Slice fname into date and zone
        start = datetime.datetime(int(fname[0:4]),int(fname[5:7]),int(fname[8:10]),20,0)
        zone = fname[11:len(fname)]
        ## Make Loot class
        loot = Loot(zone,start)
        ## Add every item from file to loot
        lootfileID = open(lootfile, 'rU')
        for line_number, line in enumerate(lootfileID):
            if line == '':
                continue
            #print line
            member, item, value = line.strip().split(',')
            if value == '':
                value = 'special'
            loot.add_item( (member,item,value) )
        #print loot.item_list
        return loot
        
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
                    #print self.RaidWeeks[Week].AttendanceDate
                    self.MemberList[Member].add_participation(self.RaidWeeks[Week].AttendanceDate, WeekAttendance[Member])
                else:
                    self.MemberList[Member].add_participation(self.RaidWeeks[Week].AttendanceDate, 0)
        return

    def ComputePointsSpent(self):
        for Week in self.RaidWeeks.keys():
             for CurLoot in self.RaidWeeks[Week].Loots:
                 for Item in CurLoot.item_list:
                     #print Item
                     member = Item[0]
                     date = CurLoot.start_time
                     zone = CurLoot.zone
                     item_name = Item[1]
                     value = Item[2]
                     #print member, date, zone, item_name, value
                     if member not in self.MemberList.keys():
                         self.add_member(member)
                     self.MemberList[member].add_loot(date, zone, item_name, value)
        return

    def UpdateReports(self):
        if not os.path.isdir('output'):
            os.mkdir('output')
        TempDebugReport = ""
        TempScoresReport = ""
        TempLootByPerson = ""
        TempSeniority = ""
        ## Sort the memberlist by name
        keys = self.MemberList.keys()
        keys.sort(lambda x,y: cmp(x.lower(),y.lower()))
        #print keys
        for Member in keys:
            self.MemberList[Member].ScanMemberEvents()
            TempDebugReport += ("%s\n%s\n" % (self.MemberList[Member].Name, self.MemberList[Member].DebugReport))
#            TempScoresReport += ("%d
            if self.MemberList[Member].LootByPerson != "":
                TempLootByPerson += ("%s\n" % self.MemberList[Member].LootByPerson)
            TempSeniority += ("%s%5.1f   |%s\n" % (self.MemberList[Member].Name.ljust(16), self.MemberList[Member].Seniority, self.seniority_to_string(Member)))
        self.update_debug(TempDebugReport)
        self.update_lootbyperson(TempLootByPerson)
        self.update_seniority(TempSeniority)

    def seniority_to_string(self, Member):
        temp = "".join(map(str, self.MemberList[Member].SeniorityVec))
        temp = temp.rjust(len(self.RaidWeeks.keys()))
        temp = temp.replace('0',' ')
        temp = temp.replace('1','-')
        temp = temp.replace('2','=')
        temp = temp.replace('3','x')
        temp = temp.replace('4','@')
        temp = temp.replace('5','*')
        return temp

    def update_debug(self, TempDebugReport):
        self.DebugReport += ("Last updated: %s\n\n" % (datetime.date.today().strftime('%Y-%m-%d')))
        self.DebugReport += TempDebugReport

        DebugReport = open('output\debug.txt','w')
        DebugReport.write(self.DebugReport)
        DebugReport.close()
        return
        
    def update_scoresreport(self, TempScoresReport):
        self.ScoresReport += ("Last updated: %s\n\n" % (datetime.date.today().strftime('%Y-%m-%d')))
        self.ScoresReport += ('%-9s %-9s %-9s %-18s' % (Rules.RevValueLabels[3], Rules.RevValueLabels[2], Rules.RevValueLabels[1], 'Names'))
        self.ScoresReport += TempScoresReport
        
        ScoresReport = open('output\scores.txt','w')
        ScoresReport.write(self.ScoresReport)
        ScoresReport.close()        
        return

    def update_lootbyperson(self, TempLootByPerson):
        self.LootByPerson += ("Last updated: %s\n\n" % (datetime.date.today().strftime('%Y-%m-%d')))
        self.LootByPerson += 'Person       Date       Item                                      Value    $$$  Mob\n'
        self.LootByPerson += '------------------------------------------------------------------------------------------\n'
        self.LootByPerson += TempLootByPerson

        LootByPerson = open('output\lootbyperson.txt','w')
        LootByPerson.write(self.LootByPerson)
        LootByPerson.close()
        return

    def update_lootbydate(self, TempLootByDate):
        self.LootByDate += ("Last updated: %s\n\n" % (datetime.date.today().strftime('%Y-%m-%d')))
        self.LootByDate += 'Date       Mob               Item                               Value    $$$  Person      \n'
        self.LootByDate += '------------------------------------------------------------------------------------------\n'
        self.LootByDate += TempLootByDate

        LootByDate = open('output\lootbydate.txt','w')
        LootByDate.write(self.LootByDate)
        LootByDate.close()
        return

    def update_seniority(self, TempSeniority):
        self.Seniority += ("Last updated: %s\n\n" % (datetime.date.today().strftime('%Y-%m-%d')))
        self.Seniority += "Participation 4:'@', 3:'x', 2:'=', 1:'-', 0:' '\n\n"
        self.Seniority += "Name           Seniority|\n"
        self.Seniority += "------------------------|----------------------------------------------------------------------\n"
        self.Seniority += TempSeniority
        
        Seniority = open('output\seniority.txt','w')
        Seniority.write(self.Seniority)
        Seniority.close()
        return

#--[ GuildMember Class ]-------------------------------------------------------
class GuildMember(object):

    def __init__(self, str_Name):
        self.Name = str_Name
        self.MemberEvents = []
        self.Scores = {1:0.00, 2:0.00, 3:0.00, 4:0.00}
        #self.IncScores = []
        self.IncDaysElapsed = []
        self.CurParticipation = 0
        self.SeniorityVec = []
        self.Seniority = 0
        self.SeniorityLastMonth = 0;
        self.DebugReport = ""
        self.LootByPerson = ""
        NewEvent = [Rules.SystemStartDate, 'Add Member', '', '', '', self.Scores, {}]
        self.add_event(NewEvent)
        return

    def add_participation(self, attendance_date, attendance):
        new_factor = 0
        for factor in Rules.PartFactor.keys():
            if attendance > Rules.PartFactor[factor]:
                new_factor = factor
            else:
                break
        NewEvent = [attendance_date, 'participation', new_factor, '', '', {}, {}]
        self.add_event(NewEvent)
        return

    def add_loot(self, date, zone, item, value):
        #print LootValue
        if lower(value) not in Rules.ValueLabels.keys():
            print '[compute_score] Invalid loot value, assuming special.'
            value = 'special'
        LootValueIndex = Rules.ValueLabels[lower(value)]
        #print LootValueIndex
        NewEvent = [date, 'loot', LootValueIndex, zone, item, {}, {}]
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
        # get the days elapsed between the current event and the previous
##        if index < len(self.MemberEvents)-1:
##            NextEvent = self.MemberEvents[index+1]
##        else:
##            NextEvent = (datetime.date.today(), "Today")
##        Delta = NextEvent[0] - Event[0]
        if index == 0:
            PrevEvent = self.MemberEvents[0]
        else:
            PrevEvent = self.MemberEvents[index-1]
        #print Event[0], PrevEvent[0]
        Delta = Event[0] - PrevEvent[0]
        return Delta.days

    def StoreMemberEvents(self, MemberEvents):
        self.MemberEvents = MemberEvents
        return

    def ScanMemberEvents(self):
        self.WeeksAtZero = 0;
        NewScores = {}

        #print self.Name

        # loop through member events
        for index, Event in enumerate(self.MemberEvents):

            #if self.Name == 'Sarkoris':
            #    print Event

            # find the days until next event
            DaysElapsed = self.get_days_elapsed(index, Event)
            self.IncDaysElapsed.append(DaysElapsed)

            # "add member" event
            if lower(Event[1]) == "add member":
                NewScores = {1:0, 2:0, 3:0, 4:0}
                Event[6] = NewScores
            # "participation" event
            elif lower(Event[1]) == "participation":
                #if self.Name == 'Sarkoris':
                #    print self.Scores, DaysElapsed, self.CurParticipation
                OldScores = self.add_points(self.CurParticipation, DaysElapsed)
                NewScores = OldScores
                #if self.Name == 'Sarkoris':
                #    print OldScores, self.Scores
                self.SeniorityVec.append(Event[2])
                self.CurParticipation = Event[2]
                if Event[2] == 0:
                    self.WeeksAtZero = self.WeeksAtZero + 1
                else:
                    self.WeeksAtZero = 0
                Event[5] = OldScores
                Event[6] = NewScores
            # "loot" event
            elif lower(Event[1]) == "loot":
                OldScores = self.add_points(self.CurParticipation, DaysElapsed)
                NewScores = self.subtract_loot(Event[2])
                Event[5] = OldScores
                Event[6] = NewScores                
            # "bonus" event
            elif lower(Event[1]) == "bonus":
                OldScores = self.add_points(self.CurParticipation, DaysElapsed)
                NewScores = self.bonus_points(Event[2])
                Event[5] = OldScores
                Event[6] = NewScores 
                
            #self.IncScores.append(NewScores)
            self.Scores = NewScores
        # update seniority
        self.update_seniority()
        self.update_debug()
        self.update_lootbyperson()
        return

    def add_points(self, Participation, DaysElapsed):
        NewScores = {}
        
        if Participation == 0:
            # decay saturates at 5 weeks
            if self.WeeksAtZero > 5:
                self.WeeksAtZero = 5
    
            # find points lost based on weeks inactive
            PointDelta = -Rules.PointDecay[self.WeeksAtZero] / 7.0 * DaysElapsed
            
            # make sure we don't decay past zero
            for index in self.Scores.keys():
                if self.Scores[index] > 0 and self.Scores[index] + PointDelta > 0:
                    NewScores[index] = self.Scores[index] + PointDelta
                elif self.Scores[index] > 0 and self.Scores[index] + PointDelta < 0:
                    NewScores[index] = 0
                elif self.Scores[index] <= 0:
                    NewScores[index] = self.Scores[index]
        else:        
            # determine points to add
            PointDelta = Rules.PointsPerDay[Participation] * DaysElapsed

            # make sure we don't exceed max value
            for index in self.Scores.keys():
                NewScores[index] = self.Scores[index] + PointDelta
                if NewScores[index] > Rules.MaxPoints:
                    NewScores[index] = Rules.MaxPoints

        self.Scores = NewScores
        return NewScores

    def subtract_loot(self, LootValueIndex):
        NewScores = Rules.subtract_loot(self.Scores, LootValueIndex)
        return NewScores

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
#            if index > 0:
#                OldScores = self.IncScores[index-1]
#            else:
#                OldScores = {1:0, 2:0, 3:0, 4:0}
#            if index < len(self.MemberEvents):
#                NewScores = self.IncScores[index]
#            else:
#                NewScores = self.Scores
            DaysElapsed = self.IncDaysElapsed[index]
        
            #print Event[0]
        
            NewDebugLine = ""
            NewDebugLine += ("[%s] [%3d] " % (Event[0].strftime('%Y-%m-%d'), DaysElapsed))
            NewDebugLine += ("[%3.0f %3.0f %3.0f] " % (Event[5][1], Event[5][2], Event[5][3]))
            if lower(Event[1]) == "add member":
                NewDebugLine += ("%-40s %-30s [%-8s] " % (Event[1].capitalize(), '', ''))
            elif lower(Event[1]) == "participation":
                NewDebugLine += ("%-40s %-30s [%-8d] " % (Event[1].capitalize(), '', Event[2]))
            elif lower(Event[1]) == "loot":
                NewDebugLine += ("%-40s %-30s [%-8s] " % (Event[4], Event[3], Rules.RevValueLabels[Event[2]].capitalize()))
            elif lower(Event[1]) == "bonus":
                NewDebugLine += ("%-40s %-30s [%-8d] " % (Event[3], '', Event[2]))
            NewDebugLine += ("[%3.0f %3.0f %3.0f]\n" % (Event[6][1], Event[6][2], Event[6][3]))
            self.DebugReport += NewDebugLine
        
        # get the days elapsed between the last event and the current day
        Delta = datetime.datetime.today() - Event[0]
        DaysElapsed = Delta.days
        #print DaysElapsed
        NewScores = self.add_points(self.CurParticipation, DaysElapsed)
        NewDebugLine = ""
        NewDebugLine += ("[%s] [%3d] " % (datetime.date.today().strftime('%Y-%m-%d'), DaysElapsed))
        NewDebugLine += ("[%3.0f %3.0f %3.0f] Today\n" % (NewScores[1], NewScores[2], NewScores[3]))
        self.DebugReport += NewDebugLine
        return

    def update_lootbyperson(self):
        EventDate = datetime.date(2000,01,01)
        firstevent = 1
        for Event in self.MemberEvents:
            if lower(Event[1]) == "loot":
                if firstevent:
                    str_Name = self.Name
                    firstevent = 0
                else:
                    str_Name = ''
                if EventDate == Event[0]:
                    str_EventDate = ''
                else:
                    str_EventDate = EventDate.strftime('%Y-%m-%d')
                EventDate = Event[0]
                self.LootByPerson += ( "%-11s %-10s %-40s %-8s\n" % (str_Name, str_EventDate, Event[3], Event[2]) )
        return
    
#------------------------------------------------------------------------------
