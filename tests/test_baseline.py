import unittest
from retry_policy import constant_delay

class Baseline(unittest.TestCase):
    def test_constant_delay(self):
        self.assertEqual(constant_delay(), 1)
