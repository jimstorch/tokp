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
class ArmoryGuild(object):

    #--[ ]--
    def __init__(self,strGuild,strRealm,strLocale):
        self.strGuild = strGuild
        self.strRealm = strRealm
        self.strLocale = strLocale
        self.MinRank = 1;
        self.MaxRank = 8;
        self.MinLevel = 80;
        self.Roster = []
        self.read_armory()
        self.write_roster()
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
        self.read_guild()
        return

    #--[ ]--
    def parse_armory(self):
        # Parse guild from xml read
        self.parse_guild_file()
        return

    #--[ ]--
    def open_url(self, strURL):
        # Define the user_agent as Mozilla
        #user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4'
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5 (.NET CLR 3.5.30729)'
        strHeaders = {'User-Agent':user_agent}
        values = {}
        # Encode and Request the URL
        strData = urllib.urlencode(values)
        request = urllib2.Request(strURL,strData,strHeaders)
        response = urllib2.urlopen(request)
        strXMLFile = response.read()
        return strXMLFile
    
    #--[ ]--
    def read_guild(self):
        # Look the data up in the armory
        strCharURL = 'guild-info.xml'
        strURL = '%s%s?r=%s&n=%s' % (self.strBaseURL,
                                     strCharURL,
                                     self.strRealm.replace(' ', '+'),
                                     self.strGuild.replace(' ', '+'))
        print strURL
        self.strGuildFile = self.open_url(strURL)
        # Parse the XML into a dictionary
        tree = et.fromstring(self.strGuildFile)
        self.dicGuild = self.dig_xml(tree)
        return

    #--[ ]--   
    def dig_xml(self, root):
        #print root.tag
        if root.tag == 'character':
            # we're looking at a particular character
            #print 'found a character'
            if (int(root.attrib['level']) >= self.MinLevel) and (int(root.attrib['rank']) >= self.MinRank) and (int(root.attrib['rank']) <= self.MaxRank):
               #print root.attrib['name']
               self.Roster.append(root.attrib['name'])

        out = {}
        children = root.getchildren()
        if len(children) > 0:
            for child in children:
                out[child.tag] = self.dig_xml(child)
#        else:
#            # get all the element attributes
#            for Attr in root.attrib.keys():
#                out[Attr] = self.sort_alnum_values(root.attrib.get(Attr))
#
#            # get the text value (if it exists)
#            if root.text:
#                self.sort_alnum_values(root.text)
        return out

#    #--[ ]--
#    def sort_alnum_values(self, value):
#        # determine what type of value is represented: int, float, str
#        # (leading value of zero is a special case for talent tree)
#        if value.isdigit() and value[0] != '0':
#            out = int(value)
#        elif value.replace('.','0',1).isdigit() and value[0] != '0':
#            out = float(value)
#        else:
#            out = value
#        return out
#
#    #--[ ]--
#    def parse_guild_file(self):
#        # 
#        #key_list = ['guildInfo','guild']
#        #print key_list
#        #member_list = self.read_dict(self.dicGuild, key_list)
#        #print member_list
#        return
#
#    #--[ ]--
#    def read_dict(self, root, key_list):
#        out = root
#        for key in key_list:
#            out = out[key]
#        return out

    def write_roster(self):
       filename = ('%s_roster.txt' % (self.strGuild.replace(' ', '_')))
       roster_file = open(filename,'w')
       self.Roster.sort()
       for member in self.Roster:
           roster_file.write(member + '\n')
       roster_file.close()   
       return

#------------------------------------------------------------------------------
