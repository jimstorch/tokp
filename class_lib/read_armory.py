#------------------------------------------------------------------------------
#   File:       read_armory.py
#   Purpose:    
#   Author:     Peter Clive Wilkinson
#   Revised:    James Mynderse
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import urllib2
import xml.dom.minidom

class ArmoryCharacter(object):

    def __init__(self,strCharacter,strRealm,strLocale):
##    def __init__(self):
        self.strCharacter = strCharacter
        self.strRealm = strRealm
        self.strLocale = strLocale
##        print '%s %s %s' % (self.strCharacter, self.strRealm, self.strLocale)
##        self.strCharacter = 'Sarkoris'
##        self.strRealm = 'Alleria'
##        self.strLocale = 'US'
        self.read_armory()
        self.parse_armory()
        return

    def read_armory(self):
        # Set base URL
        if self.strLocale == 'US':
            self.strBaseURL = 'http://www.wowarmory.com/'
        elif self.strLocale == 'EU':
            self.strBaseURL = 'http://armory.wow-europe.com/'
        else:
            self.strBaseURL = 'http://www.wowarmory.com/'
        self.read_character_tab()
        self.read_talen_tab()
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

    def parse_armory(self):
        self.parse_char_file()
        self.parse_talent_file()
        return

    def parse_char_file(self):
        # Now have raw xml file, can print it if interested
##        print self.strCharFile
         
        # Use xml dom to parse the file
        oDoc = xml.dom.minidom.parseString(self.strCharFile)
         
        # Quick hack to display certain attributes of certain elements.
        strAttributes = (('character', 'level'),
                         ('character', 'guildName'),
                         ('agility', 'effective'))
         
        for strElement, strAttribute in strAttributes:
            oElement = oDoc.getElementsByTagName(strElement)[0]
            strValue = oElement.getAttribute(strAttribute)
            print strElement, strAttribute, strValue

        return

    def parse_talent_file(self):
        # Now have raw xml file, can print it if interested
        print self.strTalentFile
