#------------------------------------------------------------------------------
#   File:       zones.py
#   Purpose:    loads raid zone related lookups from text files
#   Author:     Jim Storch
#   Revised:
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import glob
import re


#--[ Get Mod Dict ]------------------------------------------------------------

## Regex for get_mob_dict()
mobstr = r'.*[/\\](?P<zone>.+)\.mobs'
mob_obj = re.compile(mobstr)

def get_mob_dict():

    """Find all *.mobs files and make a dictionary matching the filename
    (zone) to the mob name.""" 

    mob_dict = {}
    mob_files = glob.glob('zones/*.mobs')
    
    for mob_file in mob_files:
        print "[zones] Reading mob file '%s'." % mob_file
        match_obj = mob_obj.search(mob_file)           
        zone = match_obj.group('zone')
        mobfile = open(mob_file,'rU')

        for line in mobfile:
            mob = line.strip()
            if not mob_dict.has_key(mob):        
                mob_dict[mob] = zone
            else:
                print '[warning] Duplicate mob name:', mob

    print '[zones] Created list of', len(mob_dict),'unique zone mobs.'
    #print mob_dict
    return mob_dict     


#--[ Get Loot Dict ]-----------------------------------------------------------

## Regex for get_loot_dict()
lootstr = r'.*[/\\](?P<zone>.+)\.loot'
loot_obj = re.compile(lootstr)

boss_str = r'\[(?P<boss>.+)\]'
boss_obj = re.compile(boss_str)

def get_loot_dict():

    """Find all *.loot files and build a master list of items we care about."""

    loot_dict={}
    loot_files = glob.glob('zones/*.loot')
    
    for loot_file in loot_files:
        print "[zones] Reading loot file '%s'." % loot_file
        match_obj = loot_obj.search(loot_file)           
        zone = match_obj.group('zone')
        lootfile = open(loot_file,'rU')
        
        for line in lootfile:
            loot = line.strip()
            if not loot_dict.has_key(loot):        
                loot_dict[loot] = zone
            else:
                print '[warning] Duplicate loot item:', loot

    print '[zones] Created list of', len(loot_dict),'epic loot items.'
    #print loot_dict
    return loot_dict

## Repeat of above, but include some boss names
def get_boss_loot_dict():

    """Find all *.loot files and build a master list of items we care about."""

    boss_dict = {}
    loot_dict = {}
    loot_files = glob.glob('zones/*.loot')
    
    for loot_file in loot_files:
        print "[zones] Reading loot file '%s'." % loot_file
        match_obj = loot_obj.search(loot_file)
        zone = match_obj.group('zone')
        lootfile = open(loot_file,'rU')
        
        cur_boss = ''
        
        for line in lootfile:
            match_obj = boss_obj.search(line)
            if match_obj:
                cur_boss = match_obj.group('boss')
            else:
                loot = line.strip()
                #if cur_boss == 'Ignis the Furnace Master':
                #    print loot
                if not loot_dict.has_key(loot):        
                    loot_dict[loot] = zone
                else:
                    print '[warning] Duplicate loot item:', loot
                if not boss_dict.has_key(loot):
                    boss_dict[loot] = (zone, cur_boss)
                else:
                    print '[warning] Duplicate boss:', cur_boss

    print '[zones] Created list of', len(loot_dict),'epic loot items.'
    #print loot_dict
    return loot_dict, boss_dict
    