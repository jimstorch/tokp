from Tkinter import *

class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        master.title("ToKP")

        # status bar
        self.status = StatusBar(master)
        self.status.pack(side=BOTTOM, fill=X)

        # start the menu system
        self.menu = Menu(master)
        master.config(menu=self.menu)
        # file menu
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu = self.filemenu)
        self.filemenu.add_command(label="Exit", command=callback_exit)
        # help menu
        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About...", command=self.callback_help_about)

        self.button = Button(frame, text="QUIT", fg="red", command=callback_exit)
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print "hi there, everyone!"
        return
      
    def callback_help_about(self):
        print "This is TOKP"
        return
        

class StatusBar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

def callback_exit():
    print "destroying"
    root.destroy()
    return

# make the root
root = Tk()
# link the closing to the exit menu
root.protocol("WM_DELETE_WINDOW", callback_exit)
# make the app
app = App(root)
# go into the mainloop
root.mainloop()
