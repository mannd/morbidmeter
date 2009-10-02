#!/usr/bin/env python
# mmgui - Class for gui display  in MorbidMeter
# Copyright (c) 2009 EP Studios, Inc.
# license - GPL v 3 or later

from Tkinter import *

class SimpleWindow(Frame):
    def __init__(self, parent, callback):
        Frame.__init__(self, parent)
        self.callback = callback
        self.v = StringVar()
        self.v.set(self.format_time())
        label = Label(self, textvariable=self.v)
        label.pack()
        parent.title("MorbidMeter")
        # setting icon doesn't seem to work in Linux :(
        #parent.iconbitmap('mm.ico')
        self.listenID = self.after(500, self.test_label)

    def format_time(self):
        t = self.callback
        return t.strftime("%b %d %I:%M:%S %p"), \
             t.microsecond / 1000, "msec"


    def test_label(self):
        self.v.set(self.format_time())

    def update(self):
        self.listenID = self.after(500, self.test_label)
