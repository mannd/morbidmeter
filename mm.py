#!/usr/bin/env python
# mm - morbidmeter
# Copyright (c) 2009 EP Studios, Inc.
# license - GPL v 3 or later

from optparse import OptionParser
import ConfigParser
import os
from datetime import date
from datetime import timedelta
import datetime

def parse_options():
    program_name = "morbidmeter"
    short_program_name = "mm"
    version = "0.1"
    if (os.name == 'nt'):
        usage = "usage: python " + short_program_name + ".py [options]"
    else:
        usage = "usage: " + short_program_name + " [options]"
    parser = OptionParser(usage=usage, version=program_name + " version 0.1")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=True,
                      help="generate verbose output [default]")
    parser.add_option("--example",
                      action="store_true", dest="example", default=False,
                      help="show an example of how morbidmeter works")
    (options, args) = parser.parse_args()
    if (options.example):
        example()
    else:
        print "Right now morbidmeter does nothing, but"
        print "rerun as ./mm --example to see what it will do."


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
    
def example():
    days = days_alive(datetime.date(1950,1,1),date.today())
    year = timedelta(days=365)
    totaldays = year.days * 80
    percentlife = float(days) / float(totaldays)
    proportionalyeardays = percentlife * 365
    proportionaldate = date.fromordinal(int(proportionalyeardays))
    proportionaldate = proportionaldate.replace(year=2000)

    print "Here is an example of how morbidmeter works."
    print "Assume your birthday is Jan 1, 1950."
    print "Further assume your predicted life span is 80 years."
    print "If your life took place over just one year,"
    print "Today would be " + (proportionaldate).strftime("%b %d")
    
if __name__ == "__main__":
    main()

