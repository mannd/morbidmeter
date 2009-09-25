#!/usr/bin/env python
# user - Class for user objects in MorbidMeter
# Copyright (c) 2009 EP Studios, Inc.
# license - GPL v 3 or later

from datetime import *

def duration_in_secs(duration):
    days = duration.days
    secs = duration.seconds
    return (days * 24 * 60 * 60 + secs)

class User:
    """The user object."""
    def __init__(self, name):
        self.name = name

    birthday = datetime.now()
    longevity = 80.0
    seconds_per_year = 365 * 24 * 60 * 60

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

