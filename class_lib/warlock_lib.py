#------------------------------------------------------------------------------
#   File:       warlock_spec.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

def ParseSpec(TalentTree):
    ii = (0, 21, 43)
    Spec = {'ImpCor':int(TalentTree[ii[0]+1]),
            'ImpCoA':int(TalentTree[ii[0]+6]),
            'AmpCurse':int(TalentTree[ii[0]+8]),
            'Nightfall':int(TalentTree[ii[0]+10]),
            'EmpCor':int(TalentTree[ii[0]+11]),
            'SiphonLife':int(TalentTree[ii[0]+13]),
            'ShadowMastery':int(TalentTree[ii[0]+15]),
            'Contagion':int(TalentTree[ii[0]+16]),
            'UA':int(TalentTree[ii[0]+20]),
            'DemonicAeg':int(TalentTree[ii[1]+9]),
            'UnholyPow':int(TalentTree[ii[1]+11]),
            'SucSac':int(TalentTree[ii[1]+13]),
            'MasterD':int(TalentTree[ii[1]+16]),
            'SoulLink':int(TalentTree[ii[1]+18]),
            'DemonicKno':int(TalentTree[ii[1]+19]),
            'DemonicTac':int(TalentTree[ii[1]+20]),
            'Felguard':int(TalentTree[ii[1]+21]),
            'ISB':int(TalentTree[ii[2]+0]),
            'Bane':int(TalentTree[ii[2]+2]),
            'Deva':int(TalentTree[ii[2]+6]),
            'Ruin':int(TalentTree[ii[2]+13]),
            'BackLash':int(TalentTree[ii[2]+16]),
            'SnF':int(TalentTree[ii[2]+19])}
    return Spec

def WarlockSpecs():
    ## Define the empty spec
    EmptySpec = {'ImpCor':0,
                 'ImpCoA':0,
                 'AmpCurse':0,
                 'Nightfall':0,
                 'EmpCor':0,
                 'SiphonLife':0,
                 'ShadowMastery':0,
                 'Contagion':0,
                 'UA':0,
                 'DemonicAeg':0,
                 'UnholyPow':0,
                 'SucSac':0,
                 'MasterD':0,
                 'SoulLink':0,
                 'DemonicKno':0,
                 'DemonicTac':0,
                 'Felguard':0,
                 'ISB':0,
                 'Bane':0,
                 'Deva':0,
                 'Ruin':0,
                 'BackLash':0,
                 'SnF':0,
                 }

    ## Define the Unstable Affliction / Destructive Reach spec
    UADRSpec = {'ImpCor':5,
                'ImpCoA':2,
                'AmpCurse':1,
                'Nightfall':1,
                 'EmpCor':3,
                 'SiphonLife':1,
                 'ShadowMastery':5,
                 'Contagion':5,
                 'UA':1,
                 'DemonicAeg':0,
                 'UnholyPow':0,
                 'SucSac':0,
                 'MasterD':0,
                 'SoulLink':0,
                 'DemonicKno':0,
                 'DemonicTac':0,
                 'Felguard':0,
                 'ISB':1,
                 'Bane':5,
                 'Deva':5,
                 'Ruin':0,
                 'BackLash':0,
                 'SnF':0,
                 }

    ## Define the Dark Pact / Ruin spec
    DPRSpec = {'ImpCor':5,
               'ImpCoA':2,
               'AmpCurse':1,
               'Nightfall':1,
                 'EmpCor':3,
                 'SiphonLife':1,
                 'ShadowMastery':5,
                 'Contagion':5,
                 'UA':0,
                 'DemonicAeg':0,
                 'UnholyPow':0,
                 'SucSac':0,
                 'MasterD':0,
                 'SoulLink':0,
                 'DemonicKno':0,
                 'DemonicTac':0,
                 'Felguard':0,
                 'ISB':1,
                 'Bane':5,
                 'Deva':5,
                 'Ruin':1,
                 'BackLash':0,
                 'SnF':0,
                 }

    ## Define the felguard / destructive reach spec
    FGDRSpec = {'ImpCor':0,
                'ImpCoA':0,
                'EmpCor':0,
                'AmpCurse':0,
                'Nightfall':0,
                 'SiphonLife':0,
                 'ShadowMastery':0,
                 'Contagion':0,
                 'UA':0,
                 'DemonicAeg':1,
                 'UnholyPow':5,
                 'SucSac':0,
                 'MasterD':5,
                 'SoulLink':1,
                 'DemonicKno':3,
                 'DemonicTac':5,
                 'Felguard':1,
                 'ISB':5,
                 'Bane':5,
                 'Deva':5,
                 'Ruin':0,
                 'BackLash':0,
                 'SnF':0,
                 }

    ## Define the Demonic Tactics / Ruin spec
    DTRSpec = {'ImpCor':0,
               'ImpCoA':0,
                 'EmpCor':0,
                 'SiphonLife':0,
                 'ShadowMastery':0,
                 'Contagion':0,
                 'UA':0,
                 'DemonicAeg':1,
                 'UnholyPow':5,
                 'SucSac':1,
                 'MasterD':5,
                 'SoulLink':1,
                 'DemonicKno':3,
                 'DemonicTac':5,
                 'Felguard':0,
                 'ISB':5,
                 'Bane':5,
                 'Deva':5,
                 'Ruin':1,
                 'BackLash':0,
                 'SnF':0,
                 }

    ## Collect common Warlock specs
    WarlockSpecs = {'Empty':EmptySpec,
                    'FGDR':FGDRSpec,
                    'UADR':UADRSpec,
                    'DTR':DTRSpec,
                    'DPR':DPRSpec}
    return WarlockSpecs

def WarlockDoT():

    ## Curse of Agony
    CoA = {'Name':'Curse of Agony',
           'BaseDamage':1356,
           'BaseCast':0,
           'Duration':24,
           'Ticks':12,
           'DmgPerc':1.20,
           'Mana':265,
           'Shadow':1,
           }

    ## Curse of Doom
    CoD = {'Name':'Curse of Doom',
           'BaseDamage':4200,
           'BaseCast':0,
           'Duration':60,
           'Ticks':1,
           'DmgPerc':2.00,
           'Mana':380,
           'Shadow':1,
           }

    ## Corruption
    Cor = {'Name':'Corruption',
           'BaseDamage':906,
           'BaseCast':2,
           'Duration':18,
           'Ticks':6,
           'DmgPerc':0.93,
           'Mana':370,
           'Shadow':1,
           }

    ## Siphon Life
    SL =  {'Name':'Siphon Life',
           'BaseDamage':630,
           'BaseCast':0,
           'Duration':30,
           'Ticks':10,
           'DmgPerc':1.00,
           'Mana':410,
           'Shadow':1,
           }
    
    ## Unstable Affliction
    UA =  {'Name':'Unstable Affliction',
           'BaseDamage':1050,
           'BaseCast':1.5,
           'Duration':18,
           'Ticks':6,
           'DmgPerc':1.20,
           'Mana':400,
           'Shadow':1,
           }

    WarlockDoT = {'CoA':CoA, 'CoD':CoD, 'Cor':Cor, 'SL':SL, 'UA':UA}
    return WarlockDoT

def WarlockNuke():

    SB = {'Name':'Shadow Bolt',
          'BaseDamage':mean(541,603),
          'BaseCast':3,
          'DmgPerc':0.8571,
          'Mana':420,
          'Shadow':1,
          }

    Inc = {'Name':'Incinerate',
           'BaseDamage':mean(444,514),
           'BaseCast':2.5,
           'DmgPerc':0.8571,
           'Mana':355,
           'Shadow':0,
           }

    WarlockNuke = {'SB':SB}
    return WarlockNuke


def mean(x,y):
    return (x+y)/2
