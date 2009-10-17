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
    def __init__(self, parent, ts, user, show_msec=True):
        Frame.__init__(self, parent)
        parent.title("MorbidMeter")
        self.show_msec = show_msec
        self.ts = ts
        self.user=user
        self.v = StringVar()
        self.v.set(self.format_time())
        self.label = Label(self, textvariable=self.v)
        self.update_label()
        # setting icon doesn't seem to work in Linux :(
        # iconimage = parent.PhotoImage(file="skull.bmp")
        # iconlabel = parent.Label(self, image=iconimage)
        # parent.iconwindow(iconlabel)
        

    def update_label(self):
        self.v.set(self.format_time())
        self.label.textvariable = self.v
        self.label.pack()
        self.label.after(1000, self.update_label)

    def format_time(self):
        t = self.ts.proportional_time(self.user.percent_alive())
        if self.show_msec:
            return t.strftime("%b %d %I:%M:%S %p") + \
                " " + str(t.microsecond / 1000).zfill(3) + " msec"
        else:
            return t.strftime("        %b %d %I:%M:%S %p        ")
