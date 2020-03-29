import unittest

from ddalg.itree.test__tree import SimpleInterval
from ddalg.metrics.interval import jaccard_coefficient, get_boundary_margin, reciprocal_overlap

DELTA = 1e-5


class TestInterval(unittest.TestCase):

    def setUp(self):
        self.one = SimpleInterval.of(0, 100)
        self.two = SimpleInterval.of(50, 150)
        self.three = SimpleInterval.of(100, 200)
        self.four = SimpleInterval.of(0, 10)

    def test_jaccard_coefficient(self):
        self.assertAlmostEqual(1 / 3, jaccard_coefficient(self.one, self.two), delta=DELTA)
        self.assertAlmostEqual(0., jaccard_coefficient(self.one, self.three), delta=DELTA)
        self.assertAlmostEqual(1., jaccard_coefficient(self.one, self.one), delta=DELTA)

    def test_get_boundary_margin(self):
        self.assertAlmostEqual(5., get_boundary_margin(0, 100, .9), delta=DELTA)
        self.assertAlmostEqual(5., get_boundary_margin(-50, 50, .9), delta=DELTA)
        self.assertAlmostEqual(2.5, get_boundary_margin(0, 50, .9), delta=DELTA)

        # by default `coverage=1.`
        self.assertAlmostEqual(0., get_boundary_margin(0, 100), delta=DELTA)

        self.assertRaises(ValueError, get_boundary_margin, 0, 100, 10)

    def test_reciprocal_overlap(self):
        self.assertAlmostEqual(.5, reciprocal_overlap(self.one, self.two), delta=DELTA)
        self.assertAlmostEqual(.1, reciprocal_overlap(self.one, self.four), delta=DELTA)

        # self-overlap
        self.assertAlmostEqual(1., reciprocal_overlap(self.one, self.one), delta=DELTA)

        # disjoint intervals
        self.assertAlmostEqual(0., reciprocal_overlap(self.one, self.three), delta=DELTA)
