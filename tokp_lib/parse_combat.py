#------------------------------------------------------------------------------
#   File:       parse_combat.py
#   Purpose:    
#   Author:     Jim Storch
#   Revised:    
#------------------------------------------------------------------------------

import datetime
import re
from tokp_lib.timestamp_event import timestamp_event
from tokp_lib.zones import get_mob_dict

#--[ Regular Expressions to extract names from battle spam ]-------------------

# ' fades from '
fades_str = r"^.+\sfades\sfrom\s(?P<name>.+)\."
fades_obj = re.compile(fades_str)
# ' gains '
gains_str = r"^(?P<name>.+)\s\gains\s"
gains_obj = re.compile(gains_str)
# 'its '  (matches hits or crits)
hits_str = r"^(?P<name>.[^']+\b).*\s(?:h|cr)its\s"
hits_obj = re.compile(hits_str)
# ' suffers '
suffers_str = r"^(?P<name>.+)\ssuffers\s"
suffers_obj = re.compile(suffers_str)
# ' heals '
heals_str = r"^(?P<name>.[^']+\b).*\sheals\s"
heals_obj = re.compile(heals_str)
# ' is afflicted '
afflicted_str = r"^(?P<name>.+)\sis\safflicted\s"
afflicted_obj = re.compile(afflicted_str)


#--[ Find Name ]---------------------------------------------------------------

def find_name(event):
    ## Given an event text, attempts to extract a meaningful name
    name = None

    if ' fades from ' in event:
        match_obj = fades_obj.search(event)
        if match_obj:
            name = match_obj.group('name')
    elif ' gains ' in event:
        match_obj = gains_obj.search(event)
        if match_obj:
            name = match_obj.group('name')        
    elif 'its ' in event:
        match_obj = hits_obj.search(event)
        if match_obj:
            name = match_obj.group('name')               
    elif ' suffers ' in event:
        match_obj = suffers_obj.search(event)
        if match_obj:    
            name = match_obj.group('name') 
    elif ' heals ' in event:
        match_obj = heals_obj.search(event)
        if match_obj:
            name = match_obj.group('name') 
    elif ' is afflicted ' in event:
        match_obj = afflicted_obj.search(event)
        if match_obj:
            name = match_obj.group('name') 
    return name


#--[ Raid Class ]--------------------------------------------------------------

class Raid(object):

    def __init__(self, zone, start_time):
        self.zone = zone
        self.raid_members = []
        self.start_time = start_time
        self.last_pulse = start_time
        self.end_time = None

    def add_member(self, name, timestamp):
        if name not in self.raid_members:
            self.raid_members.append(name)
            print "[%s] Add %s at %s." % ( self.zone, name, 
                timestamp.strftime('%H:%M.%S'))

    def pulse(self, timestamp):
        ## updates time when we last saw a unique zone mob.
        self.last_pulse = timestamp

    def decay_time(self,timestamp):
        ## given a timestamp, returns the number of seconds since
        ## we last saw a unique zone mob.
        td = timestamp - self.last_pulse
        return td.seconds


#--[ Parse Combat ]------------------------------------------------------------

def parse_combat(parse_from, parse_to, combat_log, roster, you):

    log = open(combat_log, 'rU')
    mob_dict = get_mob_dict()
    raid_list = []
    current_raid = None    
    inc_lines=0
    
    print "[parse_combat] Scanning combat log..."

    ## Read each line of the combat log
    for line_number, line in enumerate(log):
               
        ## Convert into a timestamp and event text      
        timestamp,event = timestamp_event(line)
        if timestamp == None:
            print "[parse_combat] Error parsing line number",line_number+1 
            continue 

        ## Is the timestamp within our target window?
        if timestamp >= parse_from and timestamp <= parse_to:
            inc_lines += 1

            ## Now, look for familiar faces...
            name = find_name(event)          

            if name:
                
                ## Is it a raid zone mob?            
                if mob_dict.has_key(name):
                    zone = mob_dict[name]

                    ## start a raid?
                    if current_raid == None:
                        print "[parse_combat] Raid detected in %s at %s." % (
                            zone,timestamp.strftime('%H:%M:%S'))
                        current_raid = Raid(zone,timestamp)
                        ## Always add the log's creator
                        current_raid.add_member(you,timestamp)
                        raid_list.append(current_raid)
                        
                    ## have we moved zones?       
                    elif current_raid.zone != zone:
                        print "[parse_combat] Zone changed to %s at %s." % (
                            zone,timestamp.strftime('%H:%M:%S'))
                        ## close the first one
                        current_raid.end_time = current_raid.last_pulse
                        ## start a new raid
                        current_raid = Raid(zone,timestamp)
                        # Always add the log's creator
                        current_raid.add_member(you,timestamp)
                        raid_list.append(current_raid)
                        
                    else:
                        ## otherwise, keep raid timer beating
                        current_raid.pulse(timestamp)
           
                ## or is it a guildie?    
                elif name in roster:
                    if current_raid:
                        current_raid.add_member(name,timestamp)

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