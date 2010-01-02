#!/usr/bin/env python
# mmconfig - MorbidMeter configuration gui
# Copyright (c) 2009 EP Studios, Inc.
# license - GPL v 3 or later

import os, sys
from Tkinter import *
import user, timescale
from mm import read_last_user

def start_mm():
    save_config()
    os.execvp('python', create_commandline())

def save_config():
    pass

def cancel():
    sys.exit(0)

def create_window():
    window = Tk()
    window.title("MorbidMeter Configuration")
    user = read_last_user()
    name_label = Label(text='Name ' + user.name)
    name_label.pack()
    birthday_label = Label(text='Birthday ' + user.birthday)
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

