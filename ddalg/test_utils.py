import unittest

from ddalg.utils import jaccard_coefficient, get_boundary_margin
from .itree.test__tree import SimpleInterval


class TestUtil(unittest.TestCase):

    def setUp(self) -> None:
        self.one = SimpleInterval(0, 3)
        self.two = SimpleInterval(1, 4)
        self.three = SimpleInterval(3, 5)

    def test_jaccard_coefficient(self):
        self.assertEqual(.5, jaccard_coefficient(self.one, self.two))
        self.assertEqual(0, jaccard_coefficient(self.one, self.three))
        self.assertEqual(1., jaccard_coefficient(self.one, self.one))

    def test_get_boundary_margin(self):
        self.assertAlmostEqual(5., get_boundary_margin(0, 100, .9), delta=.1e-5)
        self.assertAlmostEqual(5., get_boundary_margin(-50, 50, .9), delta=.1e-5)
        self.assertAlmostEqual(2.5, get_boundary_margin(0, 50, .9), delta=.1e-5)

        # by default `coverage=1.`
        self.assertAlmostEqual(0., get_boundary_margin(0, 100), delta=1e-5)

        self.assertRaises(ValueError, get_boundary_margin, 0, 100, 10)
