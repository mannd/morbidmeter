#!/usr/bin/env python
# mm - MorbidMeter
# Copyright (c) 2009 EP Studios, Inc.
# license - GPL v 3 or later

from optparse import OptionParser
import ConfigParser
import os
from datetime import *
from user import User
from user import duration_in_secs
from timescale import TimeScale
from time import sleep

def os_is_windows():
    return os.name == 'nt'

def parse_options():
    program_name = "MorbidMeter"
    short_program_name = "mm"
    version = "0.1"
    if os_is_windows():
        usage = "usage: python " + short_program_name + ".py [options]"
    else:
        usage = "usage: " + short_program_name + " [options]"
    parser = OptionParser(usage=usage, version=program_name + " version 0.1")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=True,
                      help="generate verbose output [default]")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose",
                      default=False,
                      help="generate quiet output")
    parser.add_option("--example",
                      action="store_true", dest="example", default=False,
                      help="show an example of how morbidmeter works")
    parser.add_option("-i", "--interactive",
                      action="store_true", dest="interactive",
                      default = False,
                      help="run morbidmeter in interactive mode")
    (options, args) = parser.parse_args()
    if (options.example):
        example()
    elif (options.interactive):
        interactive()
    else:
        if os_is_windows():
            program_invocation = "python mm.py"
        else:
            program_invocation = "./mm"
        print "Right now morbidmeter doesn't do much, but rerun as: "
        print program_invocation + " --example"
        print "or as "
        print program_invocation + " --interactive"
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

def days_alive(birthday, now):
    """ returns number of days alive """
    return (now - birthday).days

def time_alive(birthday):
    """ returns time alive assumes born at MN on birthday """
    birthdaytime = datetime.combine(birthday, time(0,0,0))
    rightnow = datetime.now()
    diff = rightnow - birthdaytime
    return diff

def datetime_in_secs(date_time):
    days = date_time.days
    secs = date_time.seconds
    return (days * 24 * 60 * 60 + secs)

def percent_life(days, ageofdeath):
    totaldays = 365 * ageofdeath
    return float(days) / float(totaldays)

def hires_percent_life(seconds, ageofdeath):
    totalsecs = timedelta(365).seconds * ageofdeath
    return float(seconds) / float(totalsecs)

def proportional_date(days, ageofdeath):
    percentlife = percent_life(days, ageofdeath)
    proportionalyeardays = percentlife * 365
    proportionaldate = date.fromordinal(int(proportionalyeardays))
    proportionaldate = proportionaldate.replace(year=2000)
    return proportionaldate

def proportional_time(days, ageofdeath):
    secs_in_day = 24 * 60 * 60
    proportionalsecs = percent_life(days, ageofdeath) * secs_in_day
    startdatetime = datetime.datetime(2000, 1, 1, 0, 0, 0)
    return startdatetime + timedelta(seconds=proportionalsecs)

def hires_proportional_date(seconds, ageofdeath):
    hirespercentlife = hires_percent_life(seconds, ageofdeath)
    proportionalsecs = hirespercentlife * timedelta(365).seconds
    proportionaldate = (datetime(2000,1,1,0,0,0) + 
                        timedelta(seconds=proportionalsecs))
    return proportionaldate

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
    
def interactive():
    print "MorbidMeter will output your calculated date and time"
    print "assuming your life was compressed to a single year and"
    print "that you will live to be 80."
    print "MorbidMeter will update every 2 seconds."
    print "Press Control-C to stop."
    u = User("david")
    y = int(raw_input("Enter year of birth: "))
    m = int(raw_input("Enter month of birth [1-12]: "))
    d = int(raw_input("Day of birth [1-31]: "))
    # assume born at MN
    h = 0
    M = 0
    s = 0
    u.birthday = datetime(y,m,d,h,M,s)
    ts = TimeScale("year")
    ts.minimum = datetime(2000, 1, 1)
    ts.maximum = datetime(2000, 12, 31)
    while 1:
        proportional_secs = u.percent_alive() * duration_in_secs(ts.duration())
        proportional_time = (datetime(2000,1,1) + 
                             timedelta(seconds=proportional_secs))
        print proportional_time.strftime("%b %d %I:%M:%S %p"), \
            proportional_time.microsecond / 1000, "msec"
        sleep(2)

if __name__ == "__main__":
    main()
