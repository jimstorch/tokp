#------------------------------------------------------------------------------
#   File:       read_armory.py
#   Purpose:    
#   Author:     James Mynderse
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import urllib
import urllib2
from xml.etree import cElementTree as et

#----[ ARMORYCHARACTER CLASS ]-------------------------------------------------
class ArmoryCharacter(object):

    #--[ ]--
    def __init__(self,strCharacter,strRealm,strLocale):
        self.strCharacter = strCharacter
        self.strRealm = strRealm
        self.strLocale = strLocale
        self.Stats = {}
        self.read_armory()
        self.parse_armory()
        return

    #--[ ]--
    def read_armory(self):
        # Set base URL based on character location
        if self.strLocale == 'US':
            self.strBaseURL = 'http://www.wowarmory.com/'
        elif self.strLocale == 'EU':
            self.strBaseURL = 'http://armory.wow-europe.com/'
        else:
            self.strBaseURL = 'http://www.wowarmory.com/'
        # Read character and talent tabs from armory
        self.read_character_tab()
        self.read_talent_tab()
        return

    #--[ ]--
    def parse_armory(self):
        # Parse character and talent tabs from xml read
        self.parse_char_file()
        self.parse_talent_file()
        return

    #--[ ]--
    def open_url(self, strURL):
        # Define the user_agent as Mozilla
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4'
        strHeaders = {'User-Agent':user_agent}
        values = {}
        # Encode and Request the URL
        strData = urllib.urlencode(values)
        request = urllib2.Request(strURL,strData,strHeaders)
        response = urllib2.urlopen(request)
        strXMLFile = response.read()
        return strXMLFile
    
    #--[ ]--
    def read_character_tab(self):
        # Look the data up in the armory
        strCharURL = 'character-sheet.xml'
        strURL = '%s%s?r=%s&n=%s' % (self.strBaseURL,
                                     strCharURL,
                                     self.strRealm.replace(' ', '+'),
                                     self.strCharacter)
        self.strCharFile = self.open_url(strURL)
        # Parse the XML into a dictionary
        tree = et.fromstring(self.strCharFile)
        self.dicChar = self.dig_xml(tree)
        return

    #--[ ]--
    def read_talent_tab(self):
        # Look the data up in the armory
        strTalentURL = 'character-talents.xml'
        strURL = '%s%s?r=%s&n=%s' % (self.strBaseURL,
                                     strTalentURL,
                                     self.strRealm.replace(' ', '+'),
                                     self.strCharacter)
        self.strTalentFile = self.open_url(strURL)
        # Parse the XML into a dictionary
        tree = et.fromstring(self.strTalentFile)
        self.dicTalent = self.dig_xml(tree)
        return

    #--[ ]--   
    def dig_xml(self, root):
        out = {}
        children = root.getchildren()
        if len(children) > 0:
            for child in children:
                out[child.tag] = self.dig_xml(child)
        else:
            # get all the element attributes
            for Attr in root.attrib.keys():
                out[Attr] = self.sort_alnum_values(root.attrib.get(Attr))

            # get the text value (if it exists)
            if root.text:
                self.sort_alnum_values(root.text)
        return out

    #--[ ]--
    def sort_alnum_values(self, value):
        # determine what type of value is represented: int, float, str
        # (leading value of zero is a special case for talent tree)
        if value.isdigit() and value[0] != '0':
            out = int(value)
        elif value.replace('.','0',1).isdigit() and value[0] != '0':
            out = float(value)
        else:
            out = value
        return out

    #--[ ]--
    def parse_char_file(self):
        # Name, Class and Race
        key_list = ['characterInfo','character','name']
        self.Name = self.read_dict(self.dicChar, key_list)
        key_list = ['characterInfo','character','class']
        self.Class = self.read_dict(self.dicChar, key_list)
        key_list = ['characterInfo','character','race']
        self.Race = self.read_dict(self.dicChar, key_list)

        # Talent Spec
        tree = (('characterInfo','characterTab','talentSpec','treeOne'),
                ('characterInfo','characterTab','talentSpec','treeTwo'),
                ('characterInfo','characterTab','talentSpec','treeThree'))
        self.TalentSpec = (self.read_dict(self.dicChar, tree[0]),
                           self.read_dict(self.dicChar, tree[1]),
                           self.read_dict(self.dicChar, tree[2]))
        
        # Base and Effective Stats
        key_list = ['characterInfo','characterTab','baseStats']
        stat_list = ['strength','agility','stamina','intellect','spirit','armor']
        self.BaseStats = {}
        self.EffectiveStats = {}
        for stat in stat_list:
            base = []
            base.extend(key_list)
            base.extend([stat, 'base'])
            eff = []
            eff.extend(key_list)
            eff.extend([stat, 'effective'])
            self.BaseStats[stat] = self.read_dict(self.dicChar, base)
            self.EffectiveStats[stat] = self.read_dict(self.dicChar, eff)

        # Spell Damage
        key_list = ['characterInfo','characterTab','spell']
        stat_list = ['arcane','fire','frost','holy','nature','shadow']
        self.SpellDmg = {}
        self.SpellCrit = {}
        for stat in stat_list:
            dmg = []
            dmg.extend(key_list)
            dmg.extend(['bonusDamage', stat, 'value'])
            self.SpellDmg[stat] = self.read_dict(self.dicChar, dmg)
            crit = []
            crit.extend(key_list)
            crit.extend(['critChance', stat, 'percent'])
            self.SpellCrit[stat] = self.read_dict(self.dicChar, crit)
        return

    #--[ ]--
    def parse_talent_file(self):
        # Talent Tree
        key_list = ('characterInfo','talentTab','talentTree','value')
        self.TalentTree = self.read_dict(self.dicTalent, key_list)
        return

    #--[ ]--
    def read_dict(self, root, key_list):
        out = root
        for key in key_list:
            out = out[key]
        return out

#------------------------------------------------------------------------------
