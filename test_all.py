#------------------------------------------------------------------------------
#   File:       test_all.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

"""
Follow up to xml_test.py: read the saved raids, perform attendance calculations,
store everyone to a dictionary, compute current scores.
"""

from tokp_lib.xml_store import read_raid_xml, raid_files
from tokp_lib.raidweeks_xml import RaidWeek, raidweek_output
from tokp_lib.compute_score import GuildMember

AllRaids = {}
file_list = raid_files()
for fname in file_list:
    if not fname == "raidweeks":
        AllRaids[fname] = read_raid_xml(fname+'.xml')
#print AllRaids
    
# scan the raid dictionary:
# create dictionary of guild members
# update guild as new members found
# update participation

# define the guild
Guild = {}
RaidWeekStart = 2
RaidWeeks = {}

# sort the raids into raidweek buckets
for index in AllRaids.keys():
    str_raidweek = raidweek_output(RaidWeekStart, AllRaids[index].start_time)
    if str_raidweek not in RaidWeeks.keys():
        RaidWeeks[str_raidweek] = RaidWeek()
        RaidWeeks[str_raidweek].SetRaidWeek(str_raidweek)
    RaidWeeks[str_raidweek].add_member(AllRaids[index])
    # can add loot to the Guild dictionary here!    

# compute participation in each week
Attendance = []
for week in RaidWeeks.keys():
    WeekAttendance = {}
    for CurRaid in RaidWeeks[week].Raids:
        for Member in CurRaid.raid_members:
            if Member not in Guild.keys():
                Guild[Member] = GuildMember(Member)
            if Member not in WeekAttendance.keys():
                WeekAttendance[Member] = 0
            WeekAttendance[Member] += float(1) / float(RaidWeeks[week].NumRaidsThisWeek)
    # store the weekly participation event for each member
    for Member in Guild.keys():
        if Member in WeekAttendance.keys():
            Guild[Member].add_participation(RaidWeeks[week].AttendanceDate, WeekAttendance[Member])
        else:
            Guild[Member].add_participation(RaidWeeks[week].AttendanceDate, 0)

# scan events for all guild members
for Member in Guild.keys():
    Guild[Member].ScanMemberEvents()

##print Guild["Celeborn"].Name
##print Guild["Celeborn"].Scores
##print Guild["Celeborn"].IncScores
