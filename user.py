#!/usr/bin/env python
# user - Class for user objects in MorbidMeter
# Copyright (c) 2009 EP Studios, Inc.
# license - GPL v 3 or later

from datetime import *

def duration_in_secs(duration):
    days = duration.days
    secs = duration.seconds
    return days * 24 * 60 * 60 + secs

class User:
    """The user object."""
    def __init__(self, name, birthday=datetime.now(),
                 longevity=80.0,):
        self.name = name
        self.birthday=birthday
        self.longevity=longevity

    seconds_per_year = 365 * 24 * 60 * 60
    min_age = 1
    max_age = 130

    def time_alive(self):
        return datetime.now() - self.birthday

    def seconds_alive(self):
        return duration_in_secs(self.time_alive())

    def seconds_longevity(self):
        return self.longevity * self.seconds_per_year

    def deathday(self):
        daysalive = int(self.longevity * 365)
        return self.birthday + timedelta(daysalive)

    def percent_alive(self):
        return float(self.seconds_alive()) / float(self.seconds_longevity())

    def get_birthday(self, get_time=False):
        y = int(raw_input("Enter year of birth: "))
        m = int(raw_input("Enter month of birth [1-12]: "))
        d = int(raw_input("Day of birth [1-31]: "))
        if get_time:
            h = int(raw_input("Enter hour of birth: "))
            M = int(raw_input("Enter minute of birth: "))
            s = int(raw_input("Enter second of birth: "))
        else:
            # assume born at MN
            h = 0
            M = 0
            s = 0
        if (m not in range(1,13) or d not in range(1,32)
            or h not in range(0,25) or M not in range(0,61) or
            s not in range(0,61)):
            return False
        self.birthday = datetime(y,m,d,h,M,s)
        return True

    def get_longevity(self):
        self.longevity = float(raw_input("Enter expected longevity in years "))
        return self.longevity >= self.min_age and \
            self.longevity <= self.max_age

    def get_data(self):
        if not self.get_birthday():
            print "Not a real date."
            return False
        if not self.get_longevity():
            print("Not currently a realistic human life span.")
            return False
        return True

