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
        strName = (('character', 'name',0),)
        strClass = (('character', 'class',0),)
        strRace = (('character', 'race',0),)
        strCharStats = (('Name', strName),
                        ('Class', strClass),
                        ('Race', strRace))
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
        strBaseStats = (('strength', 'base',1),
                        ('agility', 'base',1),
                        ('stamina', 'base',1),
                        ('intellect', 'base',1),
                        ('spirit', 'base',1),
                        ('armor', 'base',1))
        strTotalStats = (('strength', 'effective',1),
                         ('agility', 'effective',1),
                         ('stamina', 'effective',1),
                         ('intellect', 'effective',1),
                         ('spirit', 'effective',1),
                         ('armor', 'effective',1))
        strCharStats = (('BaseStats', strBaseStats),
                        ('TotalStats', strTotalStats))
        Stats = self.read_xml_chunk(CharDoc, strCharStats)
        self.BaseStats = Stats['BaseStats']
        self.TotalStats = Stats['TotalStats']

        # Pull out spell damage, hit rating, hit percentage, crit rating and crit percentage
        strSpellDmg = (('spell','bonusDamage','arcane','value',1),
                       ('spell','bonusDamage','fire','value',1),
                       ('spell','bonusDamage','frost','value',1),
                       ('spell','bonusDamage','holy','value',1),
                       ('spell','bonusDamage','nature','value',1),
                       ('spell','bonusDamage','shadow','value',1))
        strSpellHitR = (('spell','bonusDamage','hitRating','value',1),)
        strSpellHit = (('spell','bonusDamage','hitRating','increasedHitPercent',2),)
        strSpellCritR = (('spell','bonusDamage','critChance','rating',1),)
        strSpellCrit = (('spell','bonusDamage','arcane','percent',2),
                        ('spell','bonusDamage','fire','percent',2),
                        ('spell','bonusDamage','frost','percent',2),
                        ('spell','bonusDamage','holy','percent',2),
                        ('spell','bonusDamage','nature','percent',2),
                        ('spell','bonusDamage','shadow','percent',2))
        strCharStats = (('SpellDmg', strSpellDmg),
                        ('SpellHitRating', strSpellHitR),
                        ('SpellHit', strSpellHit),
                        ('SpellCritRating', strSpellCritR),
                        ('SpellCrit', strSpellCrit))
##        print "test 1"
        Stats = self.read_xml_chunk(CharDoc, strCharStats)
##        self.SpellDmg = Stats['SpellDmg']
##        self.SpellCrit = Stats['SpellCrit']

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

    def read_xml_snippet(self, curDoc, EleAttVal):
        # split EleAttVal into Elements, Attribute, ValueType
        numElements = len(EleAttVal) - 2
        allElements = EleAttVal[:numElements]
        strAttribute, ValueType = EleAttVal[numElements:]

        # pull out the value from the nested element
        prevElement = curDoc
        for curElement in allElements:
            print curElement
            print prevElement.getElementsByTagName(curElement)
            newElement = prevElement.getElementsByTagName(curElement)[0]
            print newElement
            prevElement = newElement
        curValue = newElement.getAttribute(strAttribute)

        # modify the value if it is not intended to be a string
        if (ValueType == 1):
            curValue = int(curValue)
        elif (ValueType == 2):
            print strValue
            curValue = float(curValue)
        else:
            curValue = str(curValue)
        return curValue

    def read_xml_chunk(self, curDoc, strEleAttVal):
        dicItems = {}
        for strItemName, curItem in strEleAttVal:
            curElementValue = {}
            for EleAttVal in curItem:
                curValue = self.read_xml_snippet(curDoc,EleAttVal)
                curElementValue[EleAttVal[len(EleAttVal)-3]] = curValue
            if (len(curElementValue) > 1):
                dicItems[strItemName] = curElementValue
            else:
                dicItems[strItemName] = curValue
        return dicItems
#------------------------------------------------------------------------------
