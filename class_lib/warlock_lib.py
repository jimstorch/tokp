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

    ## Define the felguard / destructive reach spec
    FGDRSpec = {'ImpCoA':0,
                 'EmpCor':0,
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

    ## Define the 
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
    WarlockSpecs = {'Empty':EmptySpec, 'FGDR':FGDRSpec, 'DTR':DTRSpec}
    return WarlockSpecs

def WarlockDoT():

    ## Curse of Agony
    CoA = {'BaseDamage':1356,
           'Duration':24,
           'Ticks':12,
           'DmgPerc':1.20,
           'Shadow':1,
           }

    ## Curse of Doom
    CoD = {'BaseDamage':4200,
           'Duration':60,
           'Ticks':1,
           'DmgPerc':2.00,
           'Shadow':1,
           }

    ## Corruption
    Cor = {'BaseDamage':906,
           'Duration':18,
           'Ticks':6,
           'DmgPerc':0.93,
           'Shadow':1,
           }

    ## Siphon Life
    SL =  {'BaseDamage':630,
           'Duration':30,
           'Ticks':10,
           'DmgPerc':1.00,
           'Shadow':1,
           }
    
    ## Unstable Affliction
    UA =  {'BaseDamage':1050,
           'Duration':18,
           'Ticks':6,
           'DmgPerc':1.20,
           'Shadow':1,
           }

    WarlockDoT = {'CoA':CoA, 'CoD':CoD, 'Cor':Cor, 'SL':SL, 'UA':UA}
    return WarlockDoT

def WarlockNuke():

    SB = {'BaseDamage':600,
          'BaseCast':3,
          'DmgPerc':0.8571,
          'Shadow':1,
          }

    WarlockNuke = {'SB':SB}
    return WarlockNuke


