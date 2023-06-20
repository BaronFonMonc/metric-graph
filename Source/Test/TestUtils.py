import unittest

import sympy

import Data.Utils


# Basic example https://docs.python.org/3/library/unittest.html
class TestUtils(unittest.TestCase):

    def test_latex_to_int(self):
        s = '$1234567$'
        int_s = 1234567
        #self.assertEqual(Data.Utils.latex_to_int(s), int_s)

    def test_calc_pos(self):
        x = [0, 0]
        y = [1, 2]
        dist = 10
        length = 100
        self.assertEqual(Data.Utils.calc_pos(x, y, length, dist), (0.1, 0.2))

    def test_concat_intervals_single(self):
        intervals = [[1,2]]
        intervals_2 = [[]]

        self.assertEqual(Data.Utils.concat_intervals(intervals), intervals)
        self.assertEqual(Data.Utils.concat_intervals(intervals_2), intervals_2)

    def test_concat_intervals(self):
        intervals = [[1,2], [1,3], [3,5], [6,8]] #-> [[1,5], [6,8]]
        second_intervals = [[1,2], [2,8], [2,3]] #-> [[1,8]]

        ans1 = Data.Utils.concat_intervals(intervals)
        ans2 = Data.Utils.concat_intervals(second_intervals)

        self.assertEqual([[1,5], [6,8]], ans1)
        self.assertEqual([[1,8]], ans2)

    def test_concat_intervals_sympy(self):
        intervals = [[sympy.simplify((float(0))), sympy.simplify((float(2)))],
                     [sympy.simplify((float(1))), sympy.simplify((float(3)))],
                     [sympy.simplify((float(3))), sympy.simplify((float(5)))],
                     [sympy.simplify((float(6))), sympy.simplify((float(8)))]]

        ans1 = Data.Utils.concat_intervals(intervals)

        self.assertEqual([[sympy.simplify((float(0))),sympy.simplify((float(5)))],
                          [sympy.simplify((float(6))), sympy.simplify((float(8)))]], ans1)

        #a,b,c = sympy.sqrt(sympy.Rational(170,10)), sympy.sqrt(sympy.Rational(17,1)), sympy.latex(sympy.sqrt(sympy.Float(17)))
        #print(a,b,c)

    def test_intervalInersection(self):
        intervals = [[1,5], [6,8]]
        second_intervals = [[1,8]]

        self.assertEqual(Data.Utils.intervalIntersection(intervals, second_intervals), [[1,5], [6,8]])

        firstList = [[0, 2], [5, 10], [13, 23], [24, 25]]
        secondList = [[1, 5], [8, 12], [15, 24], [25, 26]]

        res = [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]

        self.assertEqual(Data.Utils.intervalIntersection(firstList,secondList), res)

    def test_intersection(self):
        list = [[[0, 2], [5, 10], [13, 23], [24, 25]],
                [[1, 5], [8, 12], [15, 24], [25, 26]],
                [[1,5], [6,8]]]

        self.assertEqual(Data.Utils.get_intersections(list), [[1,2], [5,5], [8,8]])

        list2 = [[[0,2]],[[4,5]]]
        self.assertEqual(Data.Utils.get_intersections(list2), [[]])

    def test_parseLatex(self):
        s1 = "$\sqrt{2}{2}$"
        s2 = "$$"
        s3 = "$"
        s4 = "123"
        s5 = "adva"
        s6 = "sqrt(2)"
        s7 = "sqrt[2]"
        s8 = "9/2"
        s9 = "frac(2)(2)"
        s10 = "vpowpok31pfk-031"
        s11 = "sqrt(3/2)"
        s12 = "sqrt(2)/sqrt(3)"
        s13 = "sqrt(sqrt(15/2))"

        print(Data.Utils.parseStrToLatex(s1))
        print(Data.Utils.parseStrToLatex(s2))
        print(Data.Utils.parseStrToLatex(s3))
        print(Data.Utils.parseStrToLatex(s4))
        print(Data.Utils.parseStrToLatex(s5))
        print(Data.Utils.parseStrToLatex(s6))
        print(Data.Utils.parseStrToLatex(s7))
        print(Data.Utils.parseStrToLatex(s8))
        print(Data.Utils.parseStrToLatex(s9))
        print(Data.Utils.parseStrToLatex(s10))
        print(Data.Utils.parseStrToLatex(s11))
        print(Data.Utils.parseStrToLatex(s12))
        print(Data.Utils.parseStrToLatex(s13))

if __name__ == '__main__':
    unittest.main()