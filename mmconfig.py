#!/usr/bin/env python
# mmconfig - MorbidMeter configuration gui
# Copyright (c) 2009 EP Studios, Inc.
# license - GPL v 3 or later

import os, sys
from Tkinter import *

def start_mm():
    os.execvp('python', create_commandline())

def cancel():
    sys.exit(0)

def create_window():
    window = Tk()
    window.title("MorbidMeter Configuration")
    start_button = Button(window, text='Start', command=start_mm)
    cancel_button = Button(window, text='Cancel', command=cancel)
    start_button.pack(side=LEFT)
    cancel_button.pack(side=RIGHT)
    return window

def create_commandline():
    return ['python','mm.py','--gui']

def main():
    window = create_window()
    window.mainloop()

if __name__ == "__main__":
    main()

