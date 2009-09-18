#!/usr/bin/env python
import unittest
from mm import *

class MmTestExample(unittest.TestCase):
      def test_proportional_date(self):
          days = days_alive(datetime.date(1950,1,1),datetime.date(2009,9,17))
          self.assertEqual(proportional_date(days, 80), 
                           datetime.date(2000,9,29))

      def test_proportional_time(self):
          days = days_alive(datetime.date(1950,1,1),datetime.date(2009,9,17))
          self.assertEqual(proportional_time(days, 80).hour, 17)
          self.assertEqual(proportional_time(days, 80).minute, 55)
          self.assertEqual(proportional_time(days, 80).second, 30)
          
          
if __name__ == '__main__':
    unittest.main()

