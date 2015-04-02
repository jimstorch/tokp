ToKP is/will be a collection of Python scripts for parsing WoW log files to create and maintain an attendance and loot record.

## Modules ##

  1. raid\_parser.py - Parses WoW's combat and chat logs to identify raids and epic loot received.
  1. csv2roster.py - Creates the roster.txt file from a CVS created using (some damn mod that I don't know the name of).  This is an optional utility -- you can edit roster.txt by hand.
  1. armory2roster.py - Reads guild listing from the WoW armory to make the roster file.
  1. tokp.py - administers the loot system.

### raid\_parser ###

Raid Parser does the following:

  1. Reads 'roster/roster.txt' for a list of guild members.
  1. Reads 'zones/someplace.mobs' for a list of raid zone creatures.
  1. Scans a combat log looking for mobs unique to the raid zones we're interested in.
  1. Builds a list of raids based on the mobs found.
  1. Adds guild member names found in combat during the raids.
  1. Reads 'zones/someplace.loot' for a list of epic items.
  1. Scans a chat log for the looting of epic items from the raid zones we're interested in.
  1. Builds a list of items looted and who by.

Optional arguments:

  * -b BATTLELOG - The path/filename of the combat log to scan.  Default is 'logs/WoWCombatLog.txt'.
  * -c CHATLOG - The path/filename of the chat log to scan.  Default is 'logs/WoWChatLog.txt'.
  * -r ROSTERFILE - The path/filename of the roster file to load.  Default is 'roster/roster.txt'.

Notes:

  * WoW logs do not record the year in the timestamp.  The parser takes the simplistic approach of any month greater than the current one must be last year.  If your log contains data that is greater than 11 months old it will have the wrong year (as well as being a huge ass file).
  * Raids timeout after 20 minutes without seeing a unique zone mob engaged.  A long break may generate two raids.
  * In the chat log, doing an emote of looting an item produces the EXACT same text as actually looting it.  Some joker may find his DKP docked.
  * Looting an unwanted item to disenchant is still looting an item as far as the parser is concerned.  You'll need to correct it after the fact.
  * The mobs in the zones/someplace.mobs files should only contain those with names unique to the zone.  If you're seeing phantom raids, e.g. An SSC raid when you actually did a five-man Coilfang Reservoir, then we must have a non-unique mob in 'zones/SerpentShrine Caverns.mobs'.


### csv2roster ###

This is a utility to create the name of guild members found in roster/roster.txt from a CSV file that is generated from some WoW mod I don't know the name of yet.  This is an optional program and you are free to edit roster.txt by hand.

Arguments:

  * -i CSVFILE  -  The name of the CSV file to import from.  Default is 'roster/ToK Roster.csv'.
  * -o ROSTERFILE  -  The name of the plain text roster file to create.  Default is 'roster/roster.txt.'
  * -y - Authorize overwriting the roster text file.  You'll need this if the file already exists.  Just a safety thing.

Notes:

  * Only imports the names of level 70 characters.


### armory2roster ###

This is a utility to create a roster of guild members taken from the WoW armory listing for the guild. As with cvs2roster, this is an optional program and you are free to edit roster.txt by hand.


Arguments:

  * -n GUILDNAME  -  The name of the guild.  Default is 'Pain and Suffering'.
  * -r REALM - The name of the realm. Default is 'Galakrond'.
  * -l LOCALE - The name of the locale. Default is 'US'.
  * -o ROSTERFILE  -  The name of the plain text roster file to create.  Default is 'roster/roster.txt.'
  * -y - Authorize overwriting the roster text file.  You'll need this if the file already exists.  Just a safety thing.

Notes:

  * Only imports members of level 80 or higher.
  * Only imports members with guild ranks between 1 and 8 (guild leader and initiate for Pain and Suffering).