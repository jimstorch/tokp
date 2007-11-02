#------------------------------------------------------------------------------
#   File:       parse_chat.py
#   Purpose:    
#   Author:     Jim Storch
#   Revised:    
#------------------------------------------------------------------------------

import datetime
import re

from raid_lib.timestamp_event import timestamp_event
from raid_lib.zones import get_loot_dict

# regex to pull name & item
loot_str = r"^(?P<name>.+)\sreceive[s]?\sloot:\s(?P<item>.+)\."
loot_obj = re.compile(loot_str)


def parse_chat(parse_from, parse_to, chat_log, roster, you):

    log = open(chat_log, 'rU')
    loot_dict = get_loot_dict()
    loot_list = []
    inc_lines=0
   
    print "[parse_chat] Scanning chat log..."

    ## Read each line of the chat log
    for line_number, line in enumerate(log):
               
        ## Convert into a timestamp and event text      
        timestamp,event = timestamp_event(line)
        if timestamp == None:
            print "[parse_chat] Error parsing line number",line_number+1 
            continue
            
        ## Is the timestamp within our target window?
        if timestamp >= parse_from and timestamp <= parse_to:
            inc_lines += 1

            ## something get looted?
            if ' loot:' in event:
                match_obj = loot_obj.search(event)
                if match_obj:
                    name = match_obj.group('name')
                    item = match_obj.group('item')

                    if name == 'You':
                        name = you

                    if loot_dict.has_key(item) and name in roster:
                        zone = loot_dict[item]
                        print "[%s] %s looted '%s' at %s." % (
                            zone, name, item, timestamp.strftime('%H:%M:%S'))
                        loot_list.append( (zone,name,item,timestamp) )
           
    print "[parse_chat] End of scan. Found",len(loot_list),"items(s)."                   
    print "[parse_chat] Date matched",inc_lines,"of",line_number+1,"lines."

    return loot_list                                     
