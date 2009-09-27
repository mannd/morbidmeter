#!/usr/bin/env python
# mmgui - Class for gui display  in MorbidMeter
# Copyright (c) 2009 EP Studios, Inc.
# license - GPL v 3 or later

from Tkinter import *

class SimpleWindow(Frame):
    def __init__(self, parent=None, text=None):
        Frame.__init__(self, parent)
        label = Label(self, text=text)
        label.pack()

