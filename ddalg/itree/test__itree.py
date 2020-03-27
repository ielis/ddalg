import unittest

from ddalg.itree import Interval, IntervalTree
from ._itree import get_center, IntervalNode


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


class TestIntervalNode(unittest.TestCase):

    def setUp(self) -> None:
        self.node = IntervalNode(make_intervals(0, 3, 9))

    def test_equality(self):
        self.assertEqual(IntervalNode(make_intervals(0, 3, 9)), self.node)

    def test_minimum(self):
        self.assertEqual(IntervalNode([SimpleInterval(0, 3), SimpleInterval(1, 4)]),
                         self.node.minimum())
        empty = IntervalNode([])
        self.assertEqual(empty.minimum(), empty)

    def test_maximum(self):
        self.assertEqual(IntervalNode([SimpleInterval(8, 11)]),
                         self.node.maximum())
        empty = IntervalNode([])
        self.assertEqual(empty.maximum(), empty)

    def test_min_value(self):
        self.assertEqual(SimpleInterval(2, 5), self.node.min_value())
        self.assertEqual(SimpleInterval(0, 3), self.node.left.min_value())

    def test_max_value(self):
        self.assertEqual(SimpleInterval(4, 7), self.node.max_value())
        self.assertEqual(SimpleInterval(7, 10), self.node.right.max_value())

    def test_iterate(self):
        nodes = list(self.node)
        self.assertEqual(IntervalNode([SimpleInterval(0, 3), SimpleInterval(1, 4)]), nodes[0])
        self.assertEqual(IntervalNode([SimpleInterval(8, 11)]), nodes[-1])

        # iterate through an empty node
        nodes = list(IntervalNode([]))
        self.assertListEqual([], nodes)


class TestIntervalTree(unittest.TestCase):

    def setUp(self) -> None:
        intervals = make_intervals(0, 3, 9)
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

        # test error input
        self.assertRaises(ValueError, self.tree.search, 'BlaBla')

    def test_get_overlaps(self):
        self.assertEqual(0, len(self.tree.get_overlaps(-1, 0)))

        result = self.tree.get_overlaps(0, 1)
        self.assertEqual(1, len(result))
        self.assertListEqual([SimpleInterval(0, 3)], result)

        result = self.tree.get_overlaps(4, 6)
        self.assertEqual(4, len(result))
        self.assertListEqual(
            [SimpleInterval(2, 5), SimpleInterval(3, 6), SimpleInterval(4, 7), SimpleInterval(5, 8)],
            result)

        result = self.tree.get_overlaps(10, 11)
        self.assertEqual(1, len(list(result)))
        self.assertListEqual([SimpleInterval(8, 11)], result)

        self.assertEqual(0, len(self.tree.get_overlaps(11, 12)))

    def test_len(self):
        self.assertEqual(0, len(IntervalTree([])))
        self.assertEqual(9, len(self.tree))

    def test_insert(self):
        self.assertEqual(0, len(self.tree.search(12)))

        self.tree.insert(SimpleInterval(9, 12))

        results = self.tree.search(12)
        self.assertEqual(1, len(results))
        self.assertListEqual([SimpleInterval(9, 12)], results)

    def test_fuzzy_query(self):
        intervals = make_intervals(-5, 95, 11)
        tree = IntervalTree(intervals)

        # by default required coverage is 1.
        self.assertListEqual([SimpleInterval(0, 100)], tree.fuzzy_query(0, 100))

        # try .98, this should add intervals within +-1 to the results
        self.assertListEqual([SimpleInterval(-1, 99),
                              SimpleInterval(0, 100),
                              SimpleInterval(1, 101)],
                             tree.fuzzy_query(0, 100, coverage=.98))
        # try .95, this should add intervals within +-2.5 to the results
        self.assertListEqual([SimpleInterval(-2, 98),
                              SimpleInterval(-1, 99),
                              SimpleInterval(0, 100),
                              SimpleInterval(1, 101),
                              SimpleInterval(2, 102)],
                             tree.fuzzy_query(0, 100, coverage=.95))

        # test error input
        self.assertRaises(ValueError, tree.fuzzy_query, 0, 100, 1.5)

    def test_bool(self):
        self.assertTrue(self.tree)  # tree with at least one element is true
        self.assertFalse(IntervalTree([]))  # empty tree is False


class TestUtils(unittest.TestCase):

    def test_get_center(self):
        self.assertEqual(2, get_center([SimpleInterval(1, 2), SimpleInterval(3, 4)]))
        self.assertEqual(3, get_center([SimpleInterval(1, 2),
                                        SimpleInterval(3, 4),
                                        SimpleInterval(4, 5)]))


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


def make_intervals(begin, end, n):
    # intervals=[(0,3), (1,4), ..., (8, 11)]
    intervals = []
    i = 0
    a, b = begin, end
    while i < n:
        intervals.append(SimpleInterval(a, b))
        a += 1
        b += 1
        i += 1
    return intervals
