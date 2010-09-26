#!/usr/bin/env python
import unittest
from mm import *
from user import User
from user import duration_in_secs
from timescale import DateTimeScale

class MmTestExample(unittest.TestCase):
      def test_get_proportional_time(self):
            ts = DateTimeScale("year", datetime(2000,1,1), datetime(2001,1,1))
            u = User("test")
            # User.birthday defaults to now()
            self.assertEqual(ts.proportional_time(0), ts.minimum)
      def test_user_get_birthday(self):
            u = User("test")
            self.assertEqual(u.test_birthday(1,1,1), True)
            self.assertEqual(u.test_birthday(1,1,0), True)
            self.assertEqual(u.test_birthday(1,0,0), False)
            self.assertEqual(u.test_birthday(12,1), True)
            self.assertEqual(u.test_birthday(1,1,23), True)
            self.assertEqual(u.test_birthday(13,1,0), False)
            self.assertEqual(u.test_birthday(12,31,23,59,59), True)
            self.assertEqual(u.test_birthday(1,1,1,1,60), False)
      def test_duration_in_secs(self):
            self.assertEqual(duration_in_secs(datetime(2000,1,2) - 
                                              datetime(2000,1,1)), 24 * 60 * 60)

class MmTestUser(unittest.TestCase):
      def test_seconds_longevity(self):
            user = User("test")
            self.assertEqual(user.seconds_longevity(), user.longevity 
                             * user.seconds_per_year)
            self.assertEqual(user.longevity, 80.0)
            self.assertEqual(user.seconds_per_year, 365 * 24 * 60 * 60)

if __name__ == '__main__':
    unittest.main()



