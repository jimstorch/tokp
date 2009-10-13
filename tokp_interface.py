#------------------------------------------------------------------------------
#   File:       tokp_interface.py
#   Purpose:    
#   Author:     James Mynderse
#   Revised:
#   License:    GPLv3 see LICENSE.TXT
#------------------------------------------------------------------------------

from Tkinter import *
import tkSimpleDialog
import tkFileDialog
import time
import sys

#from gui_lib.tkSimpleDialog import Dialog as tkSimpleDialog
from gui_lib.tkSimpleStatusBar import StatusBar as tkSimpleStatusBar
from tokp_lib.member_name_change import member_name_change
from tokp_lib.compute_score import Guild
from tokp_lib.roster import ArmoryGuild
from tokp_lib.roster import write_roster_text
from tokp_lib.roster import get_roster
from tokp_lib.parse_combat import parse_combat
from tokp_lib.parse_chat import parse_chat
from tokp_lib.write_summary import write_summary

base_path = 'data/raids/'

class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        master.title("ToKP")

        # status bar
        self.status = tkSimpleStatusBar(master)
        self.status.pack(side=BOTTOM, fill=X)

        # start the menu system
        self.menu = Menu(master)
        master.config(menu=self.menu)
        # file menu
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu = self.filemenu)
        self.filemenu.add_command(label="Exit", command=self.callback_exit)
        # help menu
        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About...", command=self.callback_help_about)

        self.button_update_scores = \
             Button(frame, text="Update Loot Scores", fg="black", \
             command=self.callback_update_scores)
        self.button_update_scores.grid(row=0, rowspan=2, columnspan=2, sticky=E+W, \
             padx=5, pady=5)

        self.button_parse_combat = \
             Button(frame, text="Parse Combat Log", fg="black", \
             command=self.callback_parse_combat)
        self.button_parse_combat.grid(row=2, columnspan=2, sticky=E+W, \
             padx=5, pady=5)

        self.button_parse_chat = \
             Button(frame, text="Parse Chat Log", fg="black", \
             command=self.callback_parse_chat)
        self.button_parse_chat.grid(row=3, columnspan=2, sticky=E+W, \
             padx=5, pady=5)
        
        self.button_update_roster = \
             Button(frame, text="Update Roster from Armory", fg="black", \
             command=self.callback_update_roster)
        self.button_update_roster.grid(row=4, columnspan=2, sticky=E+W, \
             padx=5, pady=5)
        
        self.button_name_change = \
             Button(frame, text="Name Change", fg="black", \
             command=self.callback_name_change)
        self.button_name_change.grid(row=5, columnspan=2, sticky=E+W, \
             padx=5, pady=5)
     
    def callback_help_about(self):
        #print "This is TOKP"
        w = AboutDialog(root,"About ToKP")
        return

    def callback_exit(self):
        #print "destroying"
        root.destroy()
        return

    def callback_update_scores(self):
        self.status.set("Updating Loot Scores")
        # time at program start
        t1 = time.time()
        # define the guild
        ToK = Guild()
        # load all raids
        #ToK.LoadRaids()
        ToK.LoadAll()
        t2 = time.time()
        #print "[raids loaded] Process time was %1.3f seconds." % (t2 - t1) 
        # compute attendance at every raidweek
        ToK.ComputeAttendance()
        ToK.ComputePointsSpent()
        t2 = time.time()
        #print "[scores computed] Process time was %1.3f seconds." % (t2 - t1) 
        
        self.status.set("Updating Loot Reports")
        # update reports for output
        ToK.UpdateReports()
        t2 = time.time()
        #print "[reports updated] Process time was %1.3f seconds." % (t2 - t1) 
        # display program run time
        t2 = time.time()
        #print "[complete] Process time was %1.3f seconds." % (t2 - t1)
        
        self.status.set("")
        return

    def callback_parse_combat(self):
        self.status.set("Finding Combat Log")
        base_log_dir = 'logs/'
        w = tkFileDialog.askopenfilename(title='Open Combat Log', \
            defaultextension='.txt', \
            initialdir=base_log_dir)
        #print w
        if len(w) != 0:
            self.status.set("Parsing Combat Log")
            raidweek_start = 2
            roster_file = 'roster/roster.txt'
            roster = get_roster(roster_file)
            raids = parse_combat(w, roster)
            loots = []
            print raids
            #write_summary(raids, loots, raidweek_start)
        self.status.set("")
        return
        
    def callback_parse_chat(self):
        self.status.set("Finding Chat Log")
        base_log_dir = 'logs/'
        w = tkFileDialog.askopenfilename(title='Open Chat Log', \
            defaultextension='.txt', \
            initialdir=base_log_dir)
        #print w
        if len(w) != 0:
            self.status.set("Parsing Chat Log")
            name = 'Sarkoris'
            raidweek_start = 2
            roster_file = 'roster/roster.txt'
            roster = get_roster(roster_file)
            raids = []
            loots = parse_chat(w, roster, name)
            print loots
            #write_summary(raids, loots, raidweek_start)
        self.status.set("")
        return

    def callback_update_roster(self):
        self.status.set("Updating Roster")
        w = ArmoryRosterDialog(root,"Guild Armory Info")
        #print w.result
        if w.result is not None:
            # read in the contents of the armory
            Guild1 = ArmoryGuild(w.result[0],w.result[1],w.result[2])
            # merge results with previous
            #outfile = 'roster/roster.txt'
            #Guild2 = read_roster_text(outfile)
            #Guild = merge_rosters(Guild1,Guild2)
            # write out a plain text file with one name per line
            #write_roster_text(Guild.Roster,options.outfile)
        self.status.set("")
        return

    def callback_name_change(self):
        self.status.set("Changing Member Name")
        w = NameChangeDialog(root,"Member Name Change")
        self.status.set("")
        return

class AboutDialog(tkSimpleDialog.Dialog):
    def body(self, master):
        return

    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(padx=5, pady=5)
        self.bind("<Return>", self.cancel)
        self.bind("<Escape>", self.cancel)
        box.pack()
        return

class NameChangeDialog(tkSimpleDialog.Dialog):

    def body(self, master):

        Label(master, text="Old Name:").grid(row=0, sticky=W)
        Label(master, text="New Name:").grid(row=1, sticky=W)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1
        
    def validate(self):
        #if self.e1.isalpha() and self.e2.isalpha():
        #    return 1
        return 1

    def apply(self):
        #member_name_change(self.e1,self.e2,base_path)
        return

class ArmoryRosterDialog(tkSimpleDialog.Dialog):

    def body(self, master):

        Label(master, text="Name:").grid(row=0, sticky=W)
        Label(master, text="Realm:").grid(row=1, sticky=W)
        Label(master, text="Locale:").grid(row=2, sticky=W)
        
        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Entry(master)
        #self.e3 = StringVar(master)
        #self.e3.set("US") # default value
        #w = Optionmenu(master, self.e3, "US", "EU")

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        #w.grid(row=2, column=1)
        return self.e1
        
    def validate(self):
        if self.e1.get().isalpha() and self.e2.get().isalpha() and self.e3.get().isalpha():
            print "not all alpha"
        return 1

    def apply(self):
        self.result = self.e1.get(), self.e2.get(), self.e3.get()
        return


# make the root
root = Tk()
# make the app
app = App(root)
# link the closing to the exit menu
root.protocol("WM_DELETE_WINDOW", app.callback_exit)
# go into the mainloop
root.mainloop()
