#!/usr/bin/env python
# mmgui - Class for gui display in MorbidMeter
# Copyright (c) 2009 EP Studios, Inc.
# license - GPL v 3 or later

from Tkinter import *
from threading import *
from time import sleep
from timescale import *
from user import *
from mmshared import os_is_windows

class SimpleWindow(Frame):
    def __init__(self, parent, ts, user,
                 show_msec=True,
                 update_interval=1000, reverse_time=False,
                 use_sound=False):
        Frame.__init__(self, parent)
        parent.title("MorbidMeter")
        self.ts = ts
        self.user=user
        self.show_msec = show_msec
        self.update_interval = update_interval
        self.reverse_time = reverse_time
        self.use_sound = use_sound
        self.v = StringVar()
        self.v.set(self.format_time())
        self.label = Label(self, textvariable=self.v)
        self.update_label()
        icon_name = 'skull'
        if os_is_windows():
            icon_file = icon_name + '.ico'
        else:
            icon_file = '@' + icon_name + '.xbm'
        try:
            parent.iconbitmap(icon_file)
        except TclError:
            print 'No ico file found.'
        parent.minsize(250,0) 

    def update_label(self):
        self.v.set(self.format_time())
        self.label.textvariable = self.v
        self.label.pack(expand=YES, fill=BOTH)
        self.label.after(self.update_interval, self.update_label)

    def format_time(self):
        if self.ts.name == "age":
            t = self.ts.proportional_time(self.user.percent_alive()) - self.user.birthday
        else:
            t = self.ts.proportional_time(self.user.percent_alive())
        if self.reverse_time:
            t = self.ts.reverse_proportional_time(self.user.percent_alive())
        if self.ts.name == "percent":
            return "%.6f" % t 
        elif self.ts.name == "universe":
            return "%.2f" % t
        elif self.ts.name == "age":
            return t
        elif self.reverse_time:
            return t
        elif self.show_msec:
            return t.strftime(self.ts.format_string) + \
                " " + str(t.microsecond / 1000).zfill(3) + " msec"
        else:
            # if self.use_sound:
            #     sound_on = False
            #     if t.timedelta.seconds % 3600 != 0:
            #         sound_on = True
            #     if t.timedelta.seconds % 3600 == 0 and sound_on:
            #         sound_on = False
            #         os.system("cvlc Bells.wav")

            return t.strftime(" " + self.ts.format_string 
                              + " ")
