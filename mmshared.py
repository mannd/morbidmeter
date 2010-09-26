#!/usr/bin/env python
# mmshared - Shared methods for MorbidMeter
# Copyright (c) 2010 EP Studios, Inc.
# license - GPL v 3 or later

import sys, os

def os_is_windows():
    return sys.platform[:3]  == 'win'

def play_sound():
    if not os_is_windows():
        os.system("cvlc Bells.wav --play-and-exit &")
