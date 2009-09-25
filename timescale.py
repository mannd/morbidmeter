#!/usr/bin/env python
# timescale - Class for timescale objects in MorbidMeter
# Copyright (c) 2009 EP Studios, Inc.
# license - GPL v 3 or later

from datetime import *

class TimeScale:
    """Time scale of measure used to calibrate MorbidMeter"""
    def __init__(self, name):
        self.name = name

    minimum = 0
    maximum = 100               # arbitrary min and max
    
    def duration(self):
        return self.maximum - self.minimum



class DateTimeScale(TimeScale):
    pass

