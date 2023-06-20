import unittest

import sympy
from sympy import continued_fraction_iterator, Rational, sqrt

import Data.Utils

from Windows.Tabs.ChartTab import ChartTab


# Basic example https://docs.python.org/3/library/unittest.html
class TestChartTab(unittest.TestCase):

    def test_is_commensurable_number(self):
        chart = ChartTab()
        a = sympy.sqrt(2)
        b = sympy.sqrt(2) * 2
        self.assertTrue(chart.isCommensurableNumber(a, b))
        self.assertTrue(chart.isCommensurableNumber(b, a))
        self.assertTrue(chart.isCommensurableNumber(a, a))
        self.assertTrue(chart.isCommensurableNumber(b, b))
        self.assertTrue(chart.isCommensurableNumber(7 * a, b))
        self.assertTrue(chart.isCommensurableNumber(a, 7 * b))
        self.assertFalse(chart.isCommensurableNumber(a, 2))
        self.assertFalse(chart.isCommensurableNumber(a, sympy.sqrt(3)))

    def test_(self):
        weight, epsilon = 5 , Rational(1, 2)
        qt, qt_1 = 0, 1
        l = sqrt(3)
        #w = 0
        for i, a in enumerate(continued_fraction_iterator(l/weight)):
            if i > 10:
                break
            qt, qt_1 = a * qt + qt_1, qt
            print(i, qt, qt_1, a)


if __name__ == '__main__':
    unittest.main()
