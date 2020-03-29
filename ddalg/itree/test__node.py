import unittest

from ddalg.model.test__interval import make_intervals
from ._node import IntervalNode, get_coordinates
from ._tree import SimpleInterval


class TestIntervalNode(unittest.TestCase):

    def setUp(self) -> None:
        self.node = IntervalNode(make_intervals(0, 3, 9))

    def test_equality(self):
        self.assertEqual(IntervalNode(make_intervals(0, 3, 9)), self.node)

    def test_minimum(self):
        intervals = sorted(list(self.node.minimum().intervals.keys()))
        self.assertEqual([SimpleInterval.of(0, 3), SimpleInterval.of(1, 4), SimpleInterval.of(2, 5)], intervals)
        empty = IntervalNode([])
        self.assertEqual(empty.minimum(), empty)

    def test_maximum(self):
        intervals = sorted(list(self.node.maximum().intervals.keys()))
        self.assertEqual([SimpleInterval.of(6, 9), SimpleInterval.of(7, 10), SimpleInterval.of(8, 11)], intervals)
        empty = IntervalNode([])
        self.assertEqual(empty.maximum(), empty)

    def test_min_value(self):
        self.assertEqual(SimpleInterval.of(3, 6), self.node.min_value())
        self.assertEqual(SimpleInterval.of(0, 3), self.node.left.min_value())

    def test_max_value(self):
        self.assertEqual(SimpleInterval.of(5, 8), self.node.max_value())
        self.assertEqual(SimpleInterval.of(8, 11), self.node.right.max_value())

    # def test_iterate(self):
    #     nodes = list(self.node)
    #     self.assertEqual(IntervalNode([SimpleInterval(0, 3), SimpleInterval(1, 4)]), nodes[0])
    #     self.assertEqual(IntervalNode([SimpleInterval(8, 11)]), nodes[-1])
    #
    #     # iterate through an empty node
    #     nodes = list(IntervalNode([]))
    #     self.assertListEqual([], nodes)

    def test_get_coordinates(self):
        self.assertSetEqual({1, 2, 3, 4}, get_coordinates([SimpleInterval(1, 2), SimpleInterval(3, 4)]))
        self.assertSetEqual({1, 2, 3, 4, 5}, get_coordinates([SimpleInterval(1, 2),
                                                              SimpleInterval(3, 4),
                                                              SimpleInterval(4, 5)]))
        self.assertSetEqual(set(), get_coordinates([]))
