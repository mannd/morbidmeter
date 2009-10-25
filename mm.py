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

def os_is_windows():
    return os.name == 'nt'

def parse_options():
    program_name = "MorbidMeter"
    short_program_name = "mm"
    version = "0.1"
    if os_is_windows():
        program_invocation = "python " + short_program_name + ".py"
    else:
        program_invocation = "./mm"
    usage = "usage: " + program_invocation + " [options]"
    parser = OptionParser(usage=usage, version=program_name + " version 0.1")
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
    parser.add_option("-i", "--interval", action="store",
                      type="int", dest="interval", default=1000,
                      help="set update time interval in msec")
    parser.add_option("-u", "--user", action="store",
                      type="string", dest="user",
                      help="select user, new if blank")
    parser.add_option("-z", "--zen", action="store_true",
                      dest="zen", default=False)
    (options, args) = parser.parse_args()
    # check available timescales
    if (options.timescale not in ["year", "day", "hour"]):
        print options.timescale, "not supported."
        return
    if (options.example):
        example()
    elif (options.interactive):
        interactive(options.show_msec, options.timescale, options.interval)
    elif (options.gui):
        gui(options.show_msec, options.timescale, options.interval)
    elif (options.zen):
        zen()
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

def main():
    parse_options()
    create_config()
    read_config()

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
    else:
        return None
    
    
def interactive(show_msec, timescale, interval):
    print "MorbidMeter will output your calculated date and time"
    print "assuming your life is compressed to a single", timescale + "."
    print "MorbidMeter will update every", interval, "msec."
    print "Press Control-C to stop."
    u = User("default")
    if not u.get_data():
        return
    ts = get_timescale(timescale)
    if ts is None:
        print "Unsupported timescale."
        return
    # continuously update console
    while True:
        proportional_time = ts.proportional_time(u.percent_alive())
        print proportional_time.strftime(ts.format_string), \
             proportional_time.microsecond / 1000, "msec"
        sleep(interval / 1000)

def gui(show_msec, timescale, interval):    
    print "MorbidMeter will show the calculated date and/or time"
    print "assuming your life is compressed to a single", timescale + "."
    print "MorbidMeter will appear in a small window."

    u = User("default")
    if not u.get_data():
        return
    ts = get_timescale(timescale)
    if ts is None:
        print "Unsupported timescale."
        return
    root = Tk()
    window = SimpleWindow(parent=root, 
                          user=u, ts=ts, 
                          show_msec=show_msec, update_interval=interval)
    window.pack()
    window.mainloop()
    

if __name__ == "__main__":
    main()
