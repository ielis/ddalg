import unittest

from ._node import IntervalNode, get_center
from .test__interval import SimpleInterval, make_intervals


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


class TestUtils(unittest.TestCase):

    def test_get_center(self):
        self.assertEqual(2, get_center([SimpleInterval(1, 2), SimpleInterval(3, 4)]))
        self.assertEqual(3, get_center([SimpleInterval(1, 2),
                                        SimpleInterval(3, 4),
                                        SimpleInterval(4, 5)]))
