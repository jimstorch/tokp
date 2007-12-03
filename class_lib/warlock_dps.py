#------------------------------------------------------------------------------
#   File:       warlock_dps.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

'''
Quantify ideal Warlock dps based on talents and spell selection
'''

from warlock_lib import WarlockSpecs
from warlock_lib import WarlockDoT
from warlock_lib import WarlockNuke

#--[ Warlock Class ]-----------------------------------------------------------
class Warlock(object):

    def __init__(self):
        self.DmgBonus = 500
        self.CritRate = 0.15
        self.DemonStats = 0
        self.FelArmorDmg = 100
        
        self.Spec = WarlockSpecs()['Empty']

        self.DoT_Priority = {1:'CoA',2:'Corruption',3:'UA',4:'Immolate'}
        self.DoT = WarlockDoT()

        self.DoT_Priority = {1:'SB'}
        self.Nuke = WarlockNuke()
        return

    def SetCommonSpec(self, SpecName):
        self.Spec = WarlockSpecs()[SpecName]
        self.update_spells()
        return

    def update_spells(self):
        self.SpellDmg = self.DmgBonus
        self.SpellDmg += self.FelArmorDmg * (1 + self.Spec['DemonicAeg'] * 0.10)
        self.SpellDmg += self.DemonStats * (self.Spec['DemonicKno'] * 0.05)
        
        AllDoT = WarlockDoT()
        for CurNukeName in AllDoT.keys():
            CurDoT = AllDoT[CurDoTName]

            ## Update current DoT total damage
            if CurDoTName == 'Cor':
                DoTSpellDmg = self.SpellDmg * (1 + self.Spec['EmpCor']*0.12)
            else:
                DoTSpellDmg = self.SpellDmg
            CurDoT['Damage'] = CurDoT['BaseDamage']
            CurDoT['Damage'] += (CurDoT['DmgPerc'] * DoTSpellDmg)
            CurDoT['Damage'] *= (1 + CurDoT['Shadow'] * self.Spec['ShadowMastery'] * 0.02)
            if CurDoTName == 'CoA' or CurDoTName == 'Cor':
                CurDoT['Damage'] *= (1 + self.Spec['Contagion'] * 0.05)
            CurDoT['Damage'] *= (1 + CurNuke['Shadow'] * self.Spec['SucSac'] * 0.15)
            CurDoT['Damage'] *= (1 + self.Spec['SoulLink'] * 0.05)

            ## Update current DoT damage per second and damage per tick
            CurDoT['DPS'] = CurDoT['Damage'] / CurDoT['Duration']
            CurDoT['DPT'] = CurDoT['Damage'] / CurDoT['Ticks']

            ## Store the current DoT
            AllDoT[CurDoTName] = CurDoT

        AllNuke = WarlockNuke()
        for CurNukeName in AllNuke.keys():
            CurNuke = AllNuke[CurNukeName]

            ## Update current nuke total damage
            if CurNukeName == 'SB' or CurNukeName == 'Inc':
                NukeSpellDmg = self.SpellDmg * (1 + self.Spec['SnF']*0.04)
            else:
                NukeSpellDmg = self.SpellDmg
            CurNuke['Damage'] = CurNuke['BaseDamage']
            CurNuke['Damage'] += (CurNuke['DmgPerc'] * NukeSpellDmg)
            CurNuke['Damage'] *= (1 + CurNuke['Shadow'] * self.Spec['ShadowMastery'] * 0.02)
            CurNuke['Damage'] *= (1 + CurNuke['Shadow'] * self.Spec['SucSac'] * 0.15)
            CurNuke['Damage'] *= (1 + self.Spec['SoulLink'] * 0.05)

            ## Deal with critical damage
            NukeCritRate = self.CritRate + (self.Spec['Deva'] * 0.01) + (self.Spec['DemonicTac'] * 0.05)
            CurNuke['CritDamage'] = CurNuke['Damage'] * (1.5 + self.Spec['Ruin'] * 0.5)
            CurNuke['TotalDamage'] = CurNuke['Damage'] + (NukeCritRate * CurNuke['CritDamage'])

            ## Deal with cast time
            if CurNukeName == 'SB':
                CurNuke['Cast'] = CurNuke['BaseCast'] - (self.Spec['Bane' * 0.1)
            else:
                CurNuke['Cast'] = CurNuke['BaseCast']
                                                         
            ## Update current DoT damage per second
            CurNuke['DPS'] = CurNuke['TotalDamage'] / CurNuke['Cast']
            
            ## Store the current nuke
            AllNuke[CurNukeName] = CurNuke

        ## Save the updates
        self.DoT = AllDoT
        self.Nuke = AllNuke
        print self.DoT['CoA']
        print self.Nuke['SB']
        return
    
    
#--[ Warlock Class ]-----------------------------------------------------------

##def TestCombat():
Lavode = Warlock()
Lavode.SetCommonSpec('FGDR')
