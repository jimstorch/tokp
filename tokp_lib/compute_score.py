#------------------------------------------------------------------------------
#   File:       
#   Purpose:    
#   Author:     
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

GuildMember.Name = "Sarkoris"
GuildMember.Participation = 0.60
GuildMember.Scores.Uber = 0;
GuildMember.Scores.Good = 0;
GuildMember.Scores.Decent = 0;
GuildMember.Scores.Rot = 0;

AttendanceUpper = [0.10, 0.25, 0.50, 0.75, 1.00]
PointsPerDay = [0.0, 0.4, 0.8, 1.6, 2.0]
PointDecay = [0.0/7.0, 0.0/7.0, 2.0/7.0, 4.0/7.0, 8.0/7.0, 10.0/7.0]

days = 2;

def add_points(GuildMember, days)

    # are points decaying?
    if GuildMember.Participation == 0
        WeeksAtZero = days // 7.0
        
        for 
        return 0

    # determine points to add
    for CurAttendanceUpper, CurPointsPerDay in AttendanceUpper, PointsPerDay
        if GuildMember.Participation < CurArrendanceUpper
            Points = CurPointsPerDay * days
            return Points
