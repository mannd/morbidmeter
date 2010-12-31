#!/usr/bin/env python
# mm - MorbidMeter
# Copyright (c) 2009 EP Studios, Inc.
# license - GPL v 3 or later

from optparse import OptionParser
import ConfigParser
import os
from datetime import *
from user import User
from timescale import TimeScale, DateTimeScale
from time import sleep
from Tkinter import *
from mmgui import SimpleWindow
from mmshared import os_is_windows, play_sound
import thread

#global for threading
terminate_it = 0

def stop_it():
    global terminate_it
    while True:
        if raw_input() == 'q':
            terminate_it = 1
    
def parse_options():
    program_name = "MorbidMeter"
    short_program_name = "mm"
    version = "0.3.0"
    if os_is_windows():
        program_invocation = "python " + short_program_name + ".py"
    else:
        program_invocation = "./mm"
    usage = "usage: " + program_invocation + " [options]"
    parser = OptionParser(usage=usage, version=program_name + " version " +
                          version)
    parser.add_option("-i", "--interactive",
                      action="store_true", dest="interactive",
                      default=False,
                      help="run morbidmeter in interactive mode")
    parser.add_option("--gui", 
                      action="store_true", dest="gui", default=False,
                      help="run gui version of program")
    parser.add_option("--msec",
                      action="store_true", dest="show_msec",
                      default=False,
                      help="show msec (when available)")
    parser.add_option("--example",
                      action="store_true", dest="example", default=False,
                      help="show an example of how morbidmeter works")
    parser.add_option("-t", "--timescale", action="store",
                      type="string", dest="timescale", default="year",
                      help="set time scale")
    parser.add_option("--interval", action="store",
                      type="int", dest="interval", default=1000,
                      help="set update time interval in msec")
    parser.add_option("-u", "--user", action="store",
                      type="string", dest="user",
                      help="select user, new if blank")
    parser.add_option("--reset", action="store_true",
                      dest="reset_user", default=False,
                      help="reset user information")
    parser.add_option("-r", "--reverse", action="store_true",
                      dest="reverse_time", default=False,
                      help="display time remaining")
    parser.add_option("--sound", action="store_true",
                      dest="use_sound", default=False,
                      help="play sounds on the hour")
    parser.add_option("-p", "--print", action="store_true",
                      dest="print_info", default=False,
                      help="print current user data")
    parser.add_option("-z", "--zen", action="store_true",
                      dest="zen", default=False)
    (options, args) = parser.parse_args()
    # check available timescales
    if (options.timescale not in ["year", "day", "hour", "month", 
                                  "percent", "universe", "age"]):
        print "Timescale", options.timescale, "not supported."
        return
    if (options.example):
        example()
    elif (options.interactive):
        interactive(options.show_msec, options.timescale, 
                    options.interval, options.reset_user,
                    options.reverse_time)
    elif (options.gui):
        gui(options.show_msec, options.timescale, 
            options.interval, options.reset_user, options.reverse_time,
            options.use_sound)
    elif (options.zen):
        zen()
    elif (options.print_info):
        print_user()
    else:
        print "Right now morbidmeter doesn't do much, but rerun as: "
        print program_invocation + " --example"
        print "or as "
        print program_invocation + " --interactive"
        print "or as "
        print program_invocation + " --gui"
        print "to see what it will do."

def create_config():
    if (not os.path.exists('mm.conf')):
        config = ConfigParser.RawConfigParser()
        config.add_section('DefaultUser')
        config.set('DefaultUser', 'name', 'default')
        configfile = open('mm.conf', 'wb')
        config.write(configfile)

def read_config():
    config = ConfigParser.RawConfigParser()
    config.read('mm.conf')
    user = config.get('DefaultUser', 'name')

def write_last_user(name, birthday, longevity):
    config = ConfigParser.RawConfigParser()
    config.add_section('LastUser')
    config.set('LastUser', 'longevity', longevity)
    config.set('LastUser', 'day', birthday.day)
    config.set('LastUser', 'month', birthday.month)
    config.set('LastUser', 'year', birthday.year)
    config.set('LastUser', 'name', name)
    configfile = open('mm.conf', 'wb')
    config.write(configfile)

def read_last_user():
    if (not os.path.exists('mm.conf')):
        return None
    config = ConfigParser.RawConfigParser()
    config.read('mm.conf')
    u = User("Default")
    u.name = config.get('LastUser', 'name')
    y = int(config.get('LastUser', 'year'))
    m = int(config.get('LastUser', 'month'))
    d = int(config.get('LastUser', 'day'))
    u.longevity = float(config.get('LastUser', 'longevity'))
    # TODO handle times here (times are allowed in User)
    u.birthday = datetime(y,m,d,0,0,0)
    if u.name != 'default':
        return None
    else:
        return u

def main():
    parse_options()
    # create_config()
    # read_config()

def print_user():
    u = read_last_user()
    if u == None:
        print "No user has been selected."
    else:
        print "User birthdate is ", u.birthday.strftime("%x") + "."
        print "User longevity is", u.longevity, "years."
    
def zen():
    print "Time is running out -- MorbidMeter tells you how fast..."

def example():
    print "Run python mm.py --interactive for an example."
    return
    days = days_alive(datetime.date(1950,1,1),date.today())
    proportionaldate = proportional_date(days, 80)
    proportionaltime = proportional_time(days, 80)
    print "Here is an example of how morbidmeter works."
    print "Assume your birthday is Jan 1, 1950."
    print "Further assume your predicted life span is 80 years."
    print "If your life took place over just one year,"
    print "today would be", (proportionaldate).strftime("%b %d")
    print "If your life took place over a single day,"
    print "the time would be", (proportionaltime).strftime("%I:%M:%S %p")

def get_timescale(timescale):
    if (timescale == "year"):
        return DateTimeScale("year", 
                           datetime(2000,1,1), datetime(2001,1,1),
                           "%b %d %I:%M:%S %p")
    elif (timescale == "day"):
        return DateTimeScale("day",
                           datetime(2000,1,1), datetime(2000, 1, 2),
                           "%I:%M:%S %p")
    elif (timescale == "hour"):
        return DateTimeScale("hour",
                           datetime(2000, 1, 1, 0, 0, 0),
                           datetime(2000, 1, 1, 1, 0, 0),
                           "%I:%M:%S")
    elif (timescale == "month"):
        return DateTimeScale("month",
                             datetime(2000,1,1), datetime(2000,2,1),
                             "%b %d %I:%M:%S %p")
    elif (timescale == "universe"): # big bang to age of universe
        return TimeScale("universe",
                         0, 15000000000)
    elif (timescale == "percent"):
        return TimeScale("percent", 0, 100)
    elif (timescale == "age"):
        return DateTimeScale("age", 0, 0,"")
    else:
        return None
    
def get_user_timescale(timescale, new_user):
    if (not new_user):
        u = read_last_user()
    if (new_user or u is None):
        u = User("default")
        if not u.get_data():
            return (None, None)
        write_last_user(u.name, u.birthday, u.longevity)
    ts = get_timescale(timescale)
    if (ts.name == "age"):
        ts.maximum = u.deathday()
        ts.minimum = u.birthday
    return (u, ts)

def interactive(show_msec, timescale, interval, reset_user, reverse_time):
    print "MorbidMeter will output your calculated date and time"
    print "assuming your life is compressed to a single", timescale + "."
    print "MorbidMeter will update every", interval, "msec."
    print "Press 'q' and then 'RETURN' to stop."
    (u, ts) = get_user_timescale(timescale, reset_user)
    if u is None:
        print "Can't set up user."
        return
    if ts is None:
        print "Unsupported timescale."
        return
    # continuously update console
    global terminate_it
    thread.start_new_thread(stop_it, ())
    while terminate_it == 0:
        if ts.name == "age":
            proportional_time = ts.proportional_time(u.percent_alive()) - u.birthday
        else:
            proportional_time = ts.proportional_time(u.percent_alive())
        if reverse_time:
            proportional_time = ts.reverse_proportional_time(u.percent_alive())
        if ts.name in ["universe", "percent", "age"] or reverse_time:
            print proportional_time
        else:
            print proportional_time.strftime(ts.format_string), \
                proportional_time.microsecond / 1000, "msec"
        sleep(interval / 1000)

def gui(show_msec, timescale, interval, reset_user, reverse_time, use_sound):    
    print "MorbidMeter will show the calculated date and/or time"
    print "assuming your life is compressed to a single", timescale + "."
    print "MorbidMeter will appear in a small window."
    
    (u, ts) = get_user_timescale(timescale, reset_user)
    if u is None:
        print "Can't set up user."
        return
    if ts is None:
        print "Unsupported timescale."
        return
    root = Tk()
    root.bell()
    window = SimpleWindow(parent=root, 
                          user=u, ts=ts,
                          show_msec=show_msec, update_interval=interval,
                          reverse_time=reverse_time, use_sound=use_sound)
    window.pack(expand=YES, fill=BOTH)
    window.mainloop()
    

if __name__ == "__main__":
    main()
