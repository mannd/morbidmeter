#!/usr/bin/env python
# user - Class for user objects in MorbidMeter
# Copyright (c) 2009 EP Studios, Inc.
# license - GPL v 3 or later

from datetime import *

def datetime_in_secs(date_time):
    days = date_time.days
    secs = date_time.seconds
    return (days * 24 * 60 * 60 + secs)

class User:
    """The user object."""
    def __init__(self, name):
        self.name = name
    birthday = datetime.now()
    longevity = 80.0
    def time_alive(self):
        return datetime.now() - self.birthday
    def deathday(self):
        daysalive = int(self.longevity * 365)
        return self.birthday + timedelta(daysalive)
    def lifepercent(self):
        seconds_alive = datetime_in_secs(datetime.now() - self.birthday)
        return float(seconds_alive) / float(self.longevity * 365 * 24 * 60 * 60)

