#!/usr/bin/env python
# timescale - Class for timescale objects in MorbidMeter
# Copyright (c) 2009 EP Studios, Inc.
# license - GPL v 3 or later

from datetime import *
from user import duration_in_secs

class TimeScale:
    """Time scale of measure used to calibrate MorbidMeter"""
    def __init__(self, name, minimum=0, maximum=100):
        self.name = name
        self.minimum = minimum
        self.maximum = maximum

    def duration(self):
        return self.maximum - self.minimum

    def proportional_time(self, percent):
        return self.minimum + percent * self.duration()
    
class DateTimeScale(TimeScale):
    """Time scale that uses DateTime"""
    def duration(self):
        return duration_in_secs(TimeScale.duration(self))

    def proportional_time(self, percent):
        return self.minimum + timedelta(seconds=
                                        (percent * self.duration()))


