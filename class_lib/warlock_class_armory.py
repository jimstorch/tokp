#------------------------------------------------------------------------------
#   File:       warlock_class.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

from read_armory import ArmoryCharacter
from warlock_lib import ParseSpec
from warlock_lib import WarlockSpecs
from warlock_lib import WarlockDoT
from warlock_lib import WarlockNuke

GCD = 1.5;
FelArmorDmg = 100
        
#--[ Warlock Class ]-----------------------------------------------------------
class Warlock(object):

    def __init__(self, Name, Server, Locale):
        print 'test1'
        self.Name = Name
        self.Server = Server
        self.Locale = Locale
        self.GetArmoryStats()
        self.DoT = WarlockDoT()
        self.Nuke = WarlockNuke()
        self.Nuke_Priority = {1:'SB'}
##        self.DoT_Priority = {1:'CoA',2:'Corruption',3:'UA'}
        self.DoT_Priority = {1:'corruption',2:'unstable_affliction'}
        return

    def GetArmoryStats(self):
        stats = ArmoryCharacter(self.Name, self.Server, self.Locale)
        self.SpellDmg = stats.SpellDmg
        self.SpellCrit = stats.SpellCrit
##        self.TalentTree = stats.TalentTree
        self.Spec = ParseSpec(stats.TalentTree)
##        self.CritRate = 0.15
##        self.Spec = WarlockSpecs()['Empty']
        print self.Spec
        return

    def SetCommonSpec(self, SpecName):
        if SpecName in WarlockSpecs().keys():
            self.Spec = WarlockSpecs()[SpecName]
            self.update_stats()
            self.update_dot_spells()
            self.update_nuke_spells()
            self.update_utility_spells()
        else:
            print "Unknown spec!"
        return

    def update_stats(self):
        # Update spell damage
        self.SpellDmg = self.DmgBonus
        self.SpellDmg += self.FelArmorDmg * (1 + self.Spec['DemonicAeg'] * 0.10)
        self.SpellDmg += self.DemonStats * (self.Spec['DemonicKno'] * 0.05)

        # Update critical rate
        self.CritRate += (0.01 * self.Spec['DemonicTac'])
        
    def update_dot_spells(self):
        AllDoT = WarlockDoT()
        for CurDoTName in AllDoT:
            CurDoT = AllDoT[CurDoTName]
            
            ## Update current DoT total damage
            if CurDoT['Name'] == 'Corruption':
                DoTSpellDmg = self.SpellDmg * (1 + self.Spec['EmpCor']*0.12)
            else:
                DoTSpellDmg = self.SpellDmg
            CurDoT['Damage'] = CurDoT['BaseDamage']
            CurDoT['Damage'] += (CurDoT['DmgPerc'] * DoTSpellDmg)
            CurDoT['Damage'] *= (1 + CurDoT['Shadow'] * self.Spec['ShadowMastery'] * 0.02)
            if CurDoT['Name'] == 'Curse of Agony' or CurDoT['Name'] == 'Corruption':
                CurDoT['Damage'] *= (1 + self.Spec['Contagion'] * 0.05)
            CurDoT['Damage'] *= (1 + CurDoT['Shadow'] * self.Spec['SucSac'] * 0.15)
            CurDoT['Damage'] *= (1 + self.Spec['SoulLink'] * 0.05)

            ## Deal with cast time
            if CurDoT['Name'] == 'Corruption':
                CurDoT['Cast'] = CurDoT['BaseCast'] - (self.Spec['ImpCor'] * 0.4)
            else:
                CurDoT['Cast'] = CurDoT['BaseCast']
            if CurDoT['Cast'] < GCD:
                CurDoT['Cast'] = GCD

            ## Update current DoT damage per second and damage per tick
            CurDoT['DPS'] = CurDoT['Damage'] / (CurDoT['Duration'] + CurDoT['Cast'])
            CurDoT['DPT'] = CurDoT['Damage'] / CurDoT['Ticks']

            ## Store the current DoT
            AllDoT[CurDoTName] = CurDoT
        ## Save the updates
        self.DoT = AllDoT
        return
    
    def update_nuke_spells(self):
        AllNuke = WarlockNuke()
        for CurNukeName in AllNuke.keys():
            CurNuke = AllNuke[CurNukeName]

            ## Update current nuke total damage
            if CurNuke['Name'] == 'Shadow Bolt' or CurNuke['Name'] == 'Incinerate':
                NukeSpellDmg = self.SpellDmg * (1 + self.Spec['SnF']*0.04)
            else:
                NukeSpellDmg = self.SpellDmg
            CurNuke['Damage'] = CurNuke['BaseDamage']
            CurNuke['Damage'] += (CurNuke['DmgPerc'] * NukeSpellDmg)
            CurNuke['Damage'] *= (1 + CurNuke['Shadow'] * self.Spec['ShadowMastery'] * 0.02)
            CurNuke['Damage'] *= (1 + CurNuke['Shadow'] * self.Spec['SucSac'] * 0.15)
            CurNuke['Damage'] *= (1 + self.Spec['SoulLink'] * 0.05)

            ## Deal with critical damage
            NukeCritRate = self.CritRate + (self.Spec['Deva'] * 0.01)
            CurNuke['CritDamage'] = CurNuke['Damage'] * (1.5 + 0.5*self.Spec['Ruin'])
            CurNuke['TotalDamage'] = CurNuke['Damage'] + (NukeCritRate * CurNuke['CritDamage'])

            ## Deal with cast time
            if CurNuke['Name'] == 'Shadow Bolt':
                CurNuke['Cast'] = CurNuke['BaseCast'] - (self.Spec['Bane'] * 0.1)
            else:
                CurNuke['Cast'] = CurNuke['BaseCast']
            if CurNuke['Cast'] < GCD:
                CurNuke['Cast'] = GCD
                                                         
            ## Update current DoT damage per second
            CurNuke['DPS'] = CurNuke['TotalDamage'] / CurNuke['Cast']
            
            ## Store the current nuke
            AllNuke[CurNukeName] = CurNuke
        ## Save the updates
        self.Nuke = AllNuke
        return

    def update_utility_spells(self):
        return
    
#--[ Warlock Class ]-----------------------------------------------------------
