#------------------------------------------------------------------------------
#   File:       warlock_spec.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

def WarlockSpecs():
    ## Define the empty spec
    EmptySpec = {'ImpCoA':0,
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
    UADRSpec = {'ImpCoA':2,
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
    DPRSpec = {'ImpCoA':2,
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
    FGDRSpec = {'ImpCoA':0,
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
    DTRSpec = {'ImpCoA':0,
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
           'Duration':24,
           'Ticks':12,
           'DmgPerc':1.20,
           'Shadow':1,
           }

    ## Curse of Doom
    CoD = {'Name':'Curse of Doom',
           'BaseDamage':4200,
           'Duration':60,
           'Ticks':1,
           'DmgPerc':2.00,
           'Shadow':1,
           }

    ## Corruption
    Cor = {'Name':'Corruption',
           'BaseDamage':906,
           'Duration':18,
           'Ticks':6,
           'DmgPerc':0.93,
           'Shadow':1,
           }

    ## Siphon Life
    SL =  {'Name':'Siphon Life',
           'BaseDamage':630,
           'Duration':30,
           'Ticks':10,
           'DmgPerc':1.00,
           'Shadow':1,
           }
    
    ## Unstable Affliction
    UA =  {'Name':'Unstable Affliction',
           'BaseDamage':1050,
           'Duration':18,
           'Ticks':6,
           'DmgPerc':1.20,
           'Shadow':1,
           }

    WarlockDoT = {'CoA':CoA, 'CoD':CoD, 'Cor':Cor, 'SL':SL, 'UA':UA}
    return WarlockDoT

def WarlockNuke():

    SB = {'Name':'Shadow Bolt',
          'BaseDamage':mean(541,603),
          'BaseCast':3,
          'DmgPerc':0.8571,
          'Shadow':1,
          }

    Inc = {'Name':'Incinerate',
           'BaseDamage':mean(444,514),
           'BaseCast':2.5,
           'DmgPerc':0.8571,
           'Shadow':0,
           }

    WarlockNuke = {'SB':SB}
    return WarlockNuke


def mean(x,y):
    return (x+y)/2
