#------------------------------------------------------------------------------
#   File:       read_armory.py
#   Purpose:    
#   Author:     Peter Clive Wilkinson
#   Revised:    James Mynderse
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

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
    
    def read_character_tab(self):
        # Look the data up in the armory
        strCharURL = 'character-sheet.xml'
        strURL = '%s%s?r=%s&n=%s' % (self.strBaseURL,
                                     strCharURL,
                                     self.strRealm.replace(' ', '+'),
                                     self.strCharacter)

        # Open url.
        # Need to specify firefox as user agent as this makes the server
        # return an XML file. If this is not done we get html.
        oOpener = urllib2.build_opener()
        oOpener.addheaders = [
           ('user-agent',
            'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4'),
           ]
        req = urllib2.Request(strURL)
        self.strCharFile = oOpener.open(req).read()
        return

    def read_talent_tab(self):
        # Look the data up in the armory
        strTalentURL = 'character-talents.xml'
        strURL = '%s%s?r=%s&n=%s' % (self.strBaseURL,
                                     strTalentURL,
                                     self.strRealm.replace(' ', '+'),
                                     self.strCharacter)         

        # Open url.
        # Need to specify firefox as user agent as this makes the server
        # return an XML file. If this is not done we get html.
        oOpener = urllib2.build_opener()
        oOpener.addheaders = [
           ('user-agent',
            'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4'),
           ]
        req = urllib2.Request(strURL)
        self.strTalentFile = oOpener.open(req).read()
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
        strCharStats = (('Name', strName),
                        ('Class', strClass),
                        ('Race', strRace))
        self.read_xml_chunk(CharDoc, strCharStats, 0)
        self.Name = self.Stats['Name']
        self.Class = self.Stats['Class']
        self.Race = self.Stats['Race']
        
        # Pull out talent spec numbers
        strTalentSpec = (('talentSpec', 'treeOne'),
                         ('talentSpec', 'treeTwo'),
                         ('talentSpec', 'treeThree'))
        strCharStats = (('TalentSpec', strTalentSpec),)
        self.read_xml_chunk(CharDoc, strCharStats, 1)
##        self.TalentSpec = (self.Stats['treeOne'],
##                           self.Stats['treeTwo'],
##                           self.Stats['treeThree'])
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
        strCharStats = (('BaseStats', strBaseStats),
                        ('TotalStats', strTotalStats))
        self.read_xml_chunk(CharDoc, strCharStats, 1)

        return

    def parse_talent_file(self):
        # Now have raw xml file, can print it if interested
##        print self.strTalentFile

        # Use xml dom to parse the file
        TalentDoc = xml.dom.minidom.parseString(self.strTalentFile)

        # Pull out talent spec (string of digits)
        strTalentTree = (('talentTree', 'value'),)
        strTalentStats = (('TalentTree', strTalentTree),)
        self.read_xml_chunk(TalentDoc, strTalentStats, 0)
        return

    def read_xml_chunk(self, CurDoc, strStats, IsIntValue):
        Stats = {}
        for strStatName, strCurStat in strStats:
            strElementValue = {}
            for strElement, strAttribute in strCurStat:
                DocElement = CurDoc.getElementsByTagName(strElement)[0]
                strValue = DocElement.getAttribute(strAttribute)
                if IsIntValue:
                    curValue = int(strValue)
                else:
                    curValue = str(strValue)
                strElementValue[strElement] = curValue
            if (len(strElementValue) > 1):
                self.Stats[strStatName] = strElementValue
            else:
                self.Stats[strStatName] = curValue
        return Stats
#------------------------------------------------------------------------------
