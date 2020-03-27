import unittest

from ddalg.itree import Interval, IntervalTree
from ._itree import get_center


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

    def test_get_center(self):
        self.assertEqual(2, get_center([SimpleInterval(1, 2), SimpleInterval(3, 4)]))
        self.assertEqual(3, get_center([SimpleInterval(1, 2),
                                        SimpleInterval(3, 4),
                                        SimpleInterval(4, 5)]))


class TestIntervalTree(unittest.TestCase):

    def setUp(self) -> None:
        intervals = []
        i = 0
        a, b = 0, 3
        while i <= 8:
            intervals.append(SimpleInterval(a, b))
            a += 1
            b += 1
            i += 1
        # intervals=[(0,3), (1,4), ..., (8, 11)]

        self.tree = IntervalTree(intervals)

    def test_search(self):
        self.assertEqual(0, len(self.tree.search(0)))

        result = self.tree.search(1)
        self.assertEqual(1, len(result))
        self.assertListEqual([SimpleInterval(0, 3)], result)

        result = self.tree.search(6)
        self.assertEqual(3, len(result))
        self.assertListEqual([SimpleInterval(3, 6), SimpleInterval(4, 7), SimpleInterval(5, 8)], result)

        result = self.tree.search(11)
        self.assertEqual(1, len(result))
        self.assertEqual([SimpleInterval(8, 11)], result)

        self.assertEqual(0, len(self.tree.search(12)))

    def test_query(self):
        self.assertEqual(0, len(self.tree.query(-1, 0)))

        result = self.tree.query(0, 1)
        self.assertEqual(1, len(result))
        self.assertListEqual([SimpleInterval(0, 3)], result)

        result = self.tree.query(4, 6)
        self.assertEqual(4, len(result))
        self.assertListEqual(
            [SimpleInterval(2, 5), SimpleInterval(3, 6), SimpleInterval(4, 7), SimpleInterval(5, 8)],
            result)

        result = self.tree.query(10, 11)
        self.assertEqual(1, len(result))
        self.assertListEqual([SimpleInterval(8, 11)], result)

        self.assertEqual(0, len(self.tree.query(11, 12)))

    def test_len(self):
        self.assertEqual(9, len(self.tree))

    def test_insert(self):
        self.assertEqual(0, len(self.tree.search(12)))

        self.tree.insert(SimpleInterval(9, 12))

        results = self.tree.search(12)
        self.assertEqual(1, len(results))
        self.assertListEqual([SimpleInterval(9, 12)], results)


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
