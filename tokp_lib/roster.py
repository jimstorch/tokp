#------------------------------------------------------------------------------
#   File:       roster.py
#   Purpose:    Various roster creation functions
#   Author:     
#   Revised:
#   License:    GPLv3 see LICENSE.TXT 
#------------------------------------------------------------------------------

import csv
import urllib
import urllib2
from xml.etree import cElementTree as et

#----[ ARMORYGUILD CLASS ]-------------------------------------------------
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
        #self.write_roster()
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
        self.strGuildFile = self.open_url(strURL)
        # Parse the XML into a dictionary
        tree = et.fromstring(self.strGuildFile)
        self.dicGuild = self.dig_xml(tree)
        return

    #--[ ]--   
    def dig_xml(self, root):
        if root.tag == 'character':
            # we're looking at a particular character
            if (int(root.attrib['level']) >= self.MinLevel) and (int(root.attrib['rank']) >= self.MinRank) and (int(root.attrib['rank']) <= self.MaxRank):
               self.Roster.append(root.attrib['name'])
        out = {}
        children = root.getchildren()
        if len(children) > 0:
            for child in children:
                out[child.tag] = self.dig_xml(child)
        return out

    def write_roster(self):
       filename = ('%s_roster.txt' % (self.strGuild.replace(' ', '_')))
       roster_file = open(filename,'w')
       self.Roster.sort()
       for member in self.Roster:
           roster_file.write(member + '\n')
       roster_file.close()   
       return
#------------------------------------------------------------------------------

#--[ Get Roster ]--------------------------------------------------------------

def get_roster(roster_file):
    roster = []
    text_file = open(roster_file,'rU')
    for line in text_file:
        guildie = line.strip()
        if not guildie in roster:        
            roster.append(guildie)
        else:
            print '[warning] Duplicate guildmember name:', guildie
    print "[get_roster] Found", len(roster), "guildmembers."
    # print roster
    return roster


#--[ Get Roster CSV ]----------------------------------------------------------

# Reads the roster from a CSV file and returns a list of all guildmember names.

# Roster CSV format:
# Index    Value
# 0        Name
# 1        Rank & Title, possible values:
#              '1 - Guild Leader'
#              '2 - Officer'
#              '3 - Banker'
#              '4 - Member'
#              '5 - Initiate'
#              '6 - Alt Char'
#              '7 - Guest'
# 2        Note
# 3        Level
# 4        Class

def get_roster_csv(csv_file):
    roster = []
    print "[get_roster_csv] reading file '%s'" % csv_file
    reader = csv.reader(open(csv_file,'rU'))
    # skip the header row
    foo = reader.next()
    for row in reader:
        ## only retrieve the level 70's (or greater; cheap futureproof)
        if int(row[3]) >= 70: 
            roster.append(row[0])
    print "[get_roster_csv] Found", len(roster), "level 70 guildmembers."
    #print roster       
    return roster


#--[ Write Roster Text ]-------------------------------------------------------

def write_roster_text(roster, text_file):
    roster.sort()
    print "[writie_roster_text] Writing new roster to", text_file
    out = open(text_file,'w')
    for guildie in roster:
        out.write(guildie + '\n')
    out.close()
    
    


