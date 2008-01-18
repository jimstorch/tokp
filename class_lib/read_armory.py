#------------------------------------------------------------------------------
#   File:       read_armory.py
#   Purpose:    
#   Author:     Peter Clive Wilkinson
#   Revised:    James Mynderse
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import urllib
import urllib2
import xml.dom.minidom

nullValue = ('null', 'value')
nullStat = ('null', nullValue)

#----[ ARMORYCHARACTER CLASS ]-------------------------------------------------
class ArmoryCharacter(object):

    def __init__(self,strCharacter,strRealm,strLocale):
        self.strCharacter = strCharacter
        self.strRealm = strRealm
        self.strLocale = strLocale
        self.Stats = {}
        self.read_armory()
        self.parse_armory()
        return

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

    def parse_armory(self):
        # Parse character and talent tabs from xml read
        self.parse_char_file()
        self.parse_talent_file()
        return

    def open_url(self, strURL):
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4'
        strHeaders = {'User-Agent':user_agent}
        values = {}
        strData = urllib.urlencode(values)
        request = urllib2.Request(strURL,strData,strHeaders)
        response = urllib2.urlopen(request)
        strXMLFile = response.read()

##        oOpener = urllib2.build_opener()
##        oOpener.addheaders = [
##           ('user-agent',
##            'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4'),
##           ]
##        req = urllib2.Request(strURL)
##        strXMLFile = oOpener.open(req).read()
        
        return strXMLFile
    
    def read_character_tab(self):
        # Look the data up in the armory
        strCharURL = 'character-sheet.xml'
        strURL = '%s%s?r=%s&n=%s' % (self.strBaseURL,
                                     strCharURL,
                                     self.strRealm.replace(' ', '+'),
                                     self.strCharacter)
        self.strCharFile = self.open_url(strURL)
        return

    def read_talent_tab(self):
        # Look the data up in the armory
        strTalentURL = 'character-talents.xml'
        strURL = '%s%s?r=%s&n=%s' % (self.strBaseURL,
                                     strTalentURL,
                                     self.strRealm.replace(' ', '+'),
                                     self.strCharacter)
        self.strTalentFile = self.open_url(strURL)
        return

    def parse_char_file(self):
        # Now have raw xml file, can print it if interested
##        print self.strCharFile
         
        # Use xml dom to parse the file
        CharDoc = xml.dom.minidom.parseString(self.strCharFile)

        # Pull out name, class, race (string values)
        strName = (('character', 'name'),)
        strClass = (('character', 'class'),)
        strRace = (('character', 'race'),)
        strCharStats = (('Name', strName, 0),
                        ('Class', strClass, 0),
                        ('Race', strRace, 0))
        Stats = self.read_xml_chunk(CharDoc, strCharStats)
        self.Name = Stats['Name']
        self.Class = Stats['Class']
        self.Race = Stats['Race']
##        self.Name = self.Stats['Name']
##        self.Class = self.Stats['Class']
##        self.Race = self.Stats['Race']
        
        # Pull out talent spec numbers
        strTalentSpec = (('talentSpec', 'treeOne', 1),
                         ('talentSpec', 'treeTwo', 1),
                         ('talentSpec', 'treeThree', 1))
        self.TalentSpec = (self.read_xml_snippet(CharDoc, strTalentSpec[0]),
                           self.read_xml_snippet(CharDoc, strTalentSpec[1]),
                           self.read_xml_snippet(CharDoc, strTalentSpec[2]))
##        self.Stats['TalentSpec'] = self.TalentSpec

        # Pull out base stats and effective stats (integer values)
        strBaseStats = (('strength', 'base'),
                        ('agility', 'base'),
                        ('stamina', 'base'),
                        ('intellect', 'base'),
                        ('spirit', 'base'),
                        ('armor', 'base'))
        strTotalStats = (('strength', 'effective'),
                         ('agility', 'effective'),
                         ('stamina', 'effective'),
                         ('intellect', 'effective'),
                         ('spirit', 'effective'),
                         ('armor', 'effective'))
        strCharStats = (('BaseStats', strBaseStats, 1),
                        ('TotalStats', strTotalStats, 1))
        Stats = self.read_xml_chunk(CharDoc, strCharStats)
        self.BaseStats = Stats['BaseStats']
        self.TotalStats = Stats['TotalStats']

        # Pull out spell damage, crit rating and crit chance
        strSpellDmg = (('arcane', 'value'),
                       ('fire', 'value'),
                       ('frost', 'value'),
                       ('holy', 'value'),
                       ('nature', 'value'),
                       ('shadow', 'value'))
        strSpellCritR = (('critChance', 'rating', 1),)
        strSpellCrit = (('arcane', 'percent'),
                        ('fire', 'percent'),
                        ('frost', 'percent'),
                        ('holy', 'percent'),
                        ('nature', 'percent'),
                        ('shadow', 'percent'))
        strCharStats = (('SpellDmg', strSpellDmg, 1),
                        ('SpellCrit', strSpellCrit, 2))
        print "test 1"
        self.SpellCritRating = self.read_xml_snippet(CharDoc, strSpellCritR[0])
        print "test 2"
        Stats = self.read_xml_chunk(CharDoc, strCharStats)
        self.SpellDmg = Stats['SpellDmg']
        self.SpellCrit = Stats['SpellCrit']

        return

    def parse_talent_file(self):
        # Now have raw xml file, can print it if interested
##        print self.strTalentFile

        # Use xml dom to parse the file
        TalentDoc = xml.dom.minidom.parseString(self.strTalentFile)

        # Pull out talent spec (string of digits)
        strTalentTree = (('talentTree', 'value'),)
        strTalentStats = (('TalentTree', strTalentTree, 0),)
        Stats = self.read_xml_chunk(TalentDoc, strTalentStats)
        self.TalentTree = Stats['TalentTree']
        return

    def read_xml_snippet(self, CurDoc, strStats):
        print strStats
        strElement, strAttribute, ValueType = strStats
        DocElement = CurDoc.getElementsByTagName(strElement)[0]
        strValue = DocElement.getAttribute(strAttribute)
        print strValue
        if (ValueType == 1):
            curValue = int(strValue)
        elif (ValueType == 2):
            print strValue
            curValue = float(strValue)
        else:
            curValue = str(strValue)
        return curValue

    def read_xml_chunk(self, CurDoc, strStats):
        Stats = {}
        for strStatName, strCurStat, ValueType  in strStats:
            strElementValue = {}
            for strElement, strAttribute in strCurStat:
                curValue = self.read_xml_snippet(CurDoc,(strElement,strAttribute,ValueType))
                strElementValue[strElement] = curValue
            if (len(strElementValue) > 1):
                Stats[strStatName] = strElementValue
##                self.Stats[strStatName] = strElementValue
            else:
                Stats[strStatName] = curValue
##                self.Stats[strStatName] = curValue
        return Stats
#------------------------------------------------------------------------------
