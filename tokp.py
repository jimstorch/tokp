#------------------------------------------------------------------------------
#   File:       tokp.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

from tokp_lib.compute_score import Guild

# define the guild
ToK = Guild()
# load all raids
ToK.LoadRaids()
# compute attendance at every raidweek
ToK.ComputeAttendance()
# update reports for output
ToK.UpdateReports()

