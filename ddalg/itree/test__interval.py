import unittest

from ._interval import Interval


class TestInterval(unittest.TestCase):

    def setUp(self) -> None:
        self.one = SimpleInterval(1, 3)

    def test_comparison(self):
        self.assertEqual(SimpleInterval(1, 3), self.one)

        self.assertLess(SimpleInterval(0, 3), self.one)
        self.assertGreater(SimpleInterval(2, 3), self.one)

        self.assertLess(SimpleInterval(1, 2), self.one)
        self.assertGreater(SimpleInterval(1, 4), self.one)

    def test_hash(self):
        self.assertEqual(hash(SimpleInterval(1, 3)), hash(self.one))
        self.assertNotEqual(hash(SimpleInterval(2, 3)), hash(self.one))

    def test_len(self):
        self.assertEqual(2, len(self.one))
        self.assertEqual(5, len(SimpleInterval(10, 15)))

    def test_intersection(self):
        intersection = self.one.intersection(SimpleInterval(0, 1))
        self.assertEqual(0, intersection)

        intersection = self.one.intersection(SimpleInterval(0, 2))
        self.assertEqual(1, intersection)

        intersection = self.one.intersection(SimpleInterval(0, 5))
        self.assertEqual(2, intersection)

        intersection = self.one.intersection(SimpleInterval(2, 3))
        self.assertEqual(1, intersection)

        intersection = self.one.intersection(SimpleInterval(3, 4))
        self.assertEqual(0, intersection)


class SimpleInterval(Interval):

    def __init__(self, begin: int, end: int):
        self._begin = begin
        self._end = end

    @property
    def begin(self):
        return self._begin

    @property
    def end(self):
        return self._end


def make_intervals(begin, end, n, step=1):
    # intervals=[(0,3), (1,4), ..., (8, 11)]
    intervals = []
    i = 0
    a, b = begin, end
    while i < n:
        intervals.append(SimpleInterval(a, b))
        a += step
        b += step
        i += 1
    return intervals
