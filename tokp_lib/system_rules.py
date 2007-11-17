#------------------------------------------------------------------------------
#   File:       system_rules.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------


# defined by loot system rules:
RaidWeekStart = 2
PartFactor = {0.5:0.00, 1:0.10, 2:0.25, 3:0.50, 4:0.75}
PointsPerDay = {0.5:0.00, 1:0.82, 2:1.29, 3:1.68, 4:2.00}
PointDecay = {0:0.0, 1:0.0, 2:2.0, 3:4.0, 4:8.0, 5:10.0}
ValueLabels = {"epic":1, "rare":2, "uncommon":3, "zg":4}
ValueCosts = {1:20 , 2:6, 3:3, 4:1}
MinCost = 20
MaxCost = 50
ResetPercent = 0.75
