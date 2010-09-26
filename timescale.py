#!/usr/bin/env python
# timescale - Class for timescale objects in MorbidMeter
# Copyright (c) 2009, 2010 EP Studios, Inc.
# license - GPL v 3 or later

from datetime import *
from user import duration_in_secs

class TimeScale:
    """Time scale of measure used to calibrate MorbidMeter"""
    def __init__(self, name, minimum=0, maximum=100, format_string=""):
        self.name = name
        self.minimum = minimum
        self.maximum = maximum
        self.format_string = format_string

    def duration(self):
        return self.maximum - self.minimum

    def proportional_time(self, percent):
        return self.minimum + percent * self.duration()

    def reverse_proportional_time(self, percent):
        return self.maximum - self.proportional_time(percent)
    
class DateTimeScale(TimeScale):
    """Time scale that uses DateTime"""
    def duration(self):
        return duration_in_secs(TimeScale.duration(self))

    def proportional_time(self, percent):
        return self.minimum + timedelta(seconds=
                                        (percent * self.duration()))

    def reverse_proportional_time(self, percent):
        return self.maximum - self.proportional_time(percent)


