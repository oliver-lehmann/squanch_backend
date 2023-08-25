import unittest
from sync.utils import mm_ss_to_seconds

class TestUtils(unittest.TestCase):
    def test_mm_ss_to_seconds(self):
        self.assertEqual(mm_ss_to_seconds('00:00'), 0)
        self.assertEqual(mm_ss_to_seconds('00:01'), 1)
        self.assertEqual(mm_ss_to_seconds('01:01'), 61)
        self.assertEqual(mm_ss_to_seconds('10:11'), 611)
        self.assertEqual(mm_ss_to_seconds('59:59'), 3599)
        self.assertEqual(mm_ss_to_seconds('119:59'), 7199)
