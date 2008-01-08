#! /usr/bin/env python

#    grabtooltip.py - This file implements the functions nessecary to grab an items attributes from wowarmory.com
#    Copyright (C) 2008 Justin Snow
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.



import urllib, urllib2
from xml.dom import minidom

WOWHEAD_URL = 'http://www.wowhead.com/?item='
ARMORY_URL  = 'http://www.wowarmory.com/item-tooltip.xml?i='

def retrieveItemId(item):
	""" Retrieve and return the item id of an item name passed as a string from wowhead.com """
	
	request = urllib
	urlItemId = urllib2.urlopen(WOWHEAD_URL + item + '&xml')
	xmlItemId = minidom.parse(urlItemId)
	itemId    = xmlItemId.firstChild.firstChild.attributes["id"].value
	urlItemId.close()
	return itemId

def retrieveXML(id):
	""" Retrieve the xml feed from wowarmory.com for a given item id """
 	
	# You have to trick the armory with a modern webbrowser's user agent to get xml data
	headers = {'User-Agent':'Firefox/2.0'}
	request = urllib2.Request(url=ARMORY_URL+id, headers=headers)
	urlData = urllib2.urlopen(request)
	xmlData  = minidom.parse(urlData)
	urlData.close()
	return xmlData

def parseItemName(name):
	""" Take an item's name and change it to meet the name requirement of wowhead.com's item search """

	# To get the name needed for the url we first need to split the string by its whitespace
	name = name.strip()
	broken_name = name.split()
	
	# Now we have to filter any punctuation out ie. the ' character.
	# Since wowhead drops all characters in a word that occur after the ' character we just need the first part.
	link = ""
	for _word in broken_name:
		if _word.find("'") != -1:
			link = _word.partition("'")[0]
		link = link + "+" + _word  

	# A leading '+' symbol is added and we don't want that so we need to remove it.
	link = link.lstrip('+')

	return link


def grabXML():
	""" Just a small little function to make the user interaction look neat. No error checking so if you mistype
		the program may crash. """

	item_name = raw_input("Please enter the item you wish to lookup: ")
	if item_name != None:
		parsed_item_name = parseItemName(item_name)
		item_id = retrieveItemId(parsed_item_name)
		item_xml = retrieveXML(item_id)

	print "This is the XML for the item you requested:"
	print item_xml.toxml()


# Test functions as they get built
if __name__ == "__main__":
	grabXML()
