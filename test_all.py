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
from tokp_lib.compute_score import Guild, GuildMember

AllRaids = {}
file_list = raid_files()
for fname in file_list:
    if not fname == "raidweeks":
        AllRaids[fname] = read_raid_xml(fname+'.xml')
#print AllRaids
AllLoot = {}
# scan the raid dictionary:
# create dictionary of guild members
# update guild as new members found
# update participation

# define the guild
ToK = Guild()
# enter all raids and loots into the guild history
ToK.parse_all_raids(AllRaids, AllLoot)
# compute attendance at every raidweek
ToK.compute_attendance()
# update reports for output
ToK.UpdateReports()

