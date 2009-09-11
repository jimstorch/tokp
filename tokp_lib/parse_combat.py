#------------------------------------------------------------------------------
#   File:       parse_combat.py
#   Purpose:    
#   Author:     Jim Storch
#   License:    GPLv3 see LICENSE.TXT    
#------------------------------------------------------------------------------

import datetime
import re
from tokp_lib.timestamp_event import timestamp_event
from tokp_lib.zones import get_mob_dict

#--[ Raid Class ]--------------------------------------------------------------

class Raid(object):

    def __init__(self, zone, start_time):
        self.zone = zone
        self.raid_members = []
        self.start_time = start_time
        self.last_pulse = start_time
        self.end_time = None

    def add_member(self, name):
        if name not in self.raid_members:
            self.raid_members.append(name)
            #print "[%s] Add %s." % (self.zone,name)

    def pulse(self, timestamp):

        """Updates time when we last saw a unique zone mob."""

        self.last_pulse = timestamp

    def decay_time(self,timestamp):
    
        """Given a timestamp, returns the number of seconds since
        we last saw a unique zone mob."""

        td = timestamp - self.last_pulse        
        return td.seconds


#--[ Parse Combat ]------------------------------------------------------------

#def parse_combat(parse_from, parse_to, combat_log, roster):   
def parse_combat(combat_log, roster):   

    log = open(combat_log, 'rU')
    mob_dict = get_mob_dict()
    #print mob_dict
    raid_list = []
    current_raid = None    
    inc_lines=0
    
    print "[parse_combat] Scanning combat log..."

    ## Read each line of the combat log
    for line_number, line in enumerate(log):
               
        ## Use regex to break up the line
#        date_str = r"(?P<month>(0?[1-9]|1[012]))/(?P<day>(0?[1-9]|[12][0-9]|3[01]))"
#        date_obj = re.compile(date_str)
#        match_date = date_obj.search(line)
#        
#        time_str = r"(?P<time>([012][0-9]:[0-5][0-9]:[0-5][0-9].[0-9][0-9][0-9]))"
#        time_obj = re.compile(time_str)
#        match_time = time_obj.search(line)
#        
        
#        if match_date:
#            print match_date.group('month')
#            print match_date.group('day')
#        if match_time:
#            print match_time.group('time')
#        if match_name:
#            print match_name.group('name')
#            print match_name.group('target')
#            print match_name.group('effect')
#
        ## Convert into a timestamp and event text      
        timestamp,event = timestamp_event(line)
        if timestamp == None:
            print "[parse_combat] Error parsing line number",line_number+1 
            continue 

        ## Is the timestamp within our target window?
        #if timestamp >= parse_from and timestamp <= parse_to:
        if 1:
            inc_lines += 1

            #name_str = r'"(?P<name>[^"]+)",[0-9x,]*,"(?P<target>[^"]+)",[0-9x,]*,"(?P<effect>[^"]+)"'
            name_str = r'"(?P<name>[^"]+)",[0-9a-zA-Z,]*,"(?P<target>[^"]+)"'
            name_obj = re.compile(name_str)
            match_name = name_obj.search(line)

#            ## Now, look for familiar faces...
#            name = find_name(event)          
#
            if match_name:
                name = match_name.group('name')
                #target = match_name.group('target')
                #print name, target
#                target = match_name.group('target')

                ## or is it a guildie?    
                if name in roster:
                    if current_raid:
                        current_raid.add_member(name)
                
                ## Is it a raid zone mob?            
                elif mob_dict.has_key(name):
                    zone = mob_dict[name]

                    ## start a raid?
                    if current_raid == None:
                        #print "[parse_combat] Raid detected in %s at %s." % (zone,timestamp.strftime('%H:%M:%S'))
                        print "[parse_combat] Raid detected in %s at %s." % (zone,timestamp.strftime('%Y-%m-%d %H:%M:%S'))
                        current_raid = Raid(zone,timestamp)
                        ## Always add the log's creator
                        #current_raid.add_member(you)
                        raid_list.append(current_raid)
                        
                    ## have we moved zones?       
                    elif current_raid.zone != zone:
                        #print "[parse_combat] Zone changed to %s at %s." % (zone,timestamp.strftime('%H:%M:%S'))
                        print "[parse_combat] Zone changed to %s at %s." % (zone,timestamp.strftime('%Y-%m-%d %H:%M:%S'))
                        #print name, zone
                        ## close the first one
                        current_raid.end_time = current_raid.last_pulse
                        ## start a new raid
                        current_raid = Raid(zone,timestamp)
                        # Always add the log's creator
                        #current_raid.add_member(you)
                        raid_list.append(current_raid)
                        
                    else:
                        ## otherwise, keep raid timer beating
                        current_raid.pulse(timestamp)

            ## Test for raid decay.
            if current_raid:
           
                seconds_cold = current_raid.decay_time(timestamp)
                ## Have 20 minutes elasped since we last saw a zone mob?
                if seconds_cold > 1200:
                    print "[parse_combat] Raid timed out at", \
                        timestamp.strftime('%H:%M:%S.')
                    current_raid.end_time = current_raid.last_pulse
                    current_raid = None
    
    ## Done with log so (if in progress) end the current raid.            
    if current_raid:
        current_raid.end_time = current_raid.last_pulse             
                    
    print "[parse_combat] End of scan. Found",len(raid_list),"raid(s)."                   
    print "[parse_combat] Date matched",inc_lines,"of",line_number+1,"lines."

    return raid_list
