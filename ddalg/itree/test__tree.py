import unittest

from ._node import IntervalNode
from ._tree import IntervalTree
from .test__interval import SimpleInterval, make_intervals


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

    def test_iteration(self):
        nodes = list(self.tree)
        self.assertEqual(IntervalNode([SimpleInterval(0, 3), SimpleInterval(1, 4)]), nodes[0])
        self.assertEqual(IntervalNode([SimpleInterval(8, 11)]), nodes[-1])
