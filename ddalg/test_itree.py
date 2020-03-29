import unittest

from ddalg.itree import IntervalTree
from ddalg.model import Interval


class TestItree(unittest.TestCase):
    """Integration tests"""

    def setUp(self):
        self.intervals = [
            IntervalImpl.of(0, 40), IntervalImpl.of(-20, -10),
            IntervalImpl.of(0, 10), IntervalImpl.of(5, 15),
            IntervalImpl.of(10, 20), IntervalImpl.of(15, 25),
            IntervalImpl.of(20, 30), IntervalImpl.of(25, 35)
        ]
        self.tree = IntervalTree(self.intervals)

    def test_get_overlaps(self):
        overlaps = self.tree.get_overlaps(15, 20)
        self.assertEqual(3, len(overlaps))
        self.assertListEqual([IntervalImpl.of(0, 40), IntervalImpl.of(10, 20), IntervalImpl.of(15, 25)], overlaps)

    def test_search(self):
        overlaps = self.tree.search(35)
        self.assertEqual(2, len(overlaps))
        self.assertListEqual([IntervalImpl.of(0, 40), IntervalImpl.of(25, 35)], overlaps)

    def test_insert(self):
        overlaps = self.tree.search(40)
        self.assertEqual(1, len(overlaps))
        self.assertListEqual([IntervalImpl.of(0, 40)], overlaps)

        # act
        self.tree.insert(IntervalImpl.of(35, 45))
        overlaps = self.tree.search(40)
        self.assertEqual(2, len(overlaps))
        self.assertListEqual([IntervalImpl.of(0, 40), IntervalImpl.of(35, 45)], overlaps)


class IntervalImpl(Interval):

    @classmethod
    def of(cls, begin, end):
        return cls(begin, end)

    def __init__(self, begin, end):
        self._begin = begin
        self._end = end

    @property
    def begin(self):
        return self._begin

    @property
    def end(self):
        return self._end
