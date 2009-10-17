#!/usr/bin/env python
import unittest
from mm import *
from user import User
from timescale import DateTimeScale

class MmTestExample(unittest.TestCase):
      def test_get_proportional_time(self):
            ts = DateTimeScale("year", datetime(2000,1,1), datetime(2001,1,1))
            u = User("test")
            # User.birthday defaults to now()
            self.assertEqual(get_proportional_time(ts, u), ts.minimum)
            print get_proportional_time(ts, u)
          
if __name__ == '__main__':
    unittest.main()

