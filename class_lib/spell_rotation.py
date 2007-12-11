#------------------------------------------------------------------------------
#   File:       spell_rotation.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

GCD = 1.5

class SpellRotation(object):

    def __init__(self,Rotation):
        self.Rotation = Rotation
        self.TotalDamage = 0
        self.TotalCastTime = 0
        self.TotalManaCost = 0
        self.DPS = 0
        self.MPS = 0
        self.DPM = 0
        self.update_rotation()
        return

    def update_rotation(self):
        for CurSpell in self.Rotation:
            self.TotalDamage += CurSpell['TotalDamage']
            if CurSpell['Cast'] >= GCD:
                self.TotalCastTime += CurSpell['Cast']
            else:
                self.TotalCastTime += GCD
            self.TotalManaCost += CurSpell['Mana']
        self.DPS = self.TotalDamage / self.TotalCastTime
        self.DPM = self.TotalDamage / self.TotalManaCost
        self.MPS = self.TotalManaCost / self.TotalCastTime
        return

    
