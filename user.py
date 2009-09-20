#!/usr/bin/env python
# user - Class for user objects in MorbidMeter
# Copyright (c) 2009 EP Studios, Inc.
# license - GPL v 3 or later

from datetime import *

class User:
    """The user object."""
    def __init__(self, name):
        self.name = name
    dob = datetime.now()
