#!/usr/bin/env python
# mmc - morbidmeter command line program
# Copyright (c) 2009 EP Studios, Inc.
# license - GPL v 3 or later

from optparse import OptionParser
import ConfigParser
import os
from datetime import date
from datetime import timedelta
import datetime

def parse_options():
    program_name = "morbidmeter commandline"
    short_program_name = "mmc"
    version = "0.1"
    usage = "usage: " + short_program_name + " [options]"
    parser = OptionParser(usage=usage, version=program_name + " version 0.1")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=True,
                      help="generate verbose output [default]")
    (options, args) = parser.parse_args()

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
    print user

def main():
    parse_options()
    create_config()
    read_config()
    birthday = datetime.date(1951, 11, 1)
    today = date.today()
    year = timedelta(days=365)
    daysalive = (today - birthday).days
    totaldays = year.days * 80
    percentlife = float(daysalive) / float(totaldays)
    proportionalyeardays = percentlife * 365
    proportionaldate = date.fromordinal(proportionalyeardays)
    print proportionaldate


if __name__ == "__main__":
    main()

