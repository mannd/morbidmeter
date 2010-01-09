#!/usr/bin/env python
# mmgui - Class for gui display  in MorbidMeter
# Copyright (c) 2009 EP Studios, Inc.
# license - GPL v 3 or later

from Tkinter import *
from threading import *
from time import sleep
from timescale import *
from user import *

class SimpleWindow(Frame):
    def __init__(self, parent, ts, user,
                 show_msec=True,
                 update_interval=1000):
        Frame.__init__(self, parent)
        parent.title("MorbidMeter")
        self.ts = ts
        self.user=user
        self.show_msec = show_msec
        self.update_interval = update_interval
        self.v = StringVar()
        self.v.set(self.format_time())
        self.label = Label(self, textvariable=self.v)
        self.update_label()
        # setting icon doesn't seem to work in Linux :(
        # iconimage = PhotoImage(file="skull.xpm")
        # iconlabel = parent.Label(self, image=iconimage)
        # parent.iconwindow(iconimage)
        parent.minsize(250,0) 

    def update_label(self):
        self.v.set(self.format_time())
        self.label.textvariable = self.v
        self.label.pack()
        self.label.after(self.update_interval, self.update_label)

    def format_time(self):
        t = self.ts.proportional_time(self.user.percent_alive())
        if self.show_msec:
            return t.strftime(self.ts.format_string) + \
                " " + str(t.microsecond / 1000).zfill(3) + " msec"
        else:
            return t.strftime(" " + self.ts.format_string 
                              + " ")
