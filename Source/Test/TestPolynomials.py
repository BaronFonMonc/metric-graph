import unittest

import networkx as nx
import sympy

import itertools

from sympy import Poly, sqrt

import Data.Utils
import Random.todd
from Logic.Polynomials import getSubGraphs, getPointNumber, getAllPaths


# Basic example https://docs.python.org/3/library/unittest.html
from Data.MetricGraph import MyNetworkX
from Random.graph_utils import *
from Random.pc_polynomial import build
from Random.todd import build_rk


class TestPolynomials(unittest.TestCase):

    def test_graph(self):
        #g = get_triangle()
        #g = get_star(4)
        g = get_triangle()
        print(build(g[0],g[1],g[2]).as_expr())
        #g = get_star(5)
        #print(build(g[0],g[1],g[2]).as_expr())
        #g = get_star(6)
        #print(build(g[0],g[1],g[2]).as_expr())

    def test_td(self):
        print()
        a = [sympy.symbols('a'), sympy.symbols('b'), sympy.symbols('c'), sympy.symbols('d'), sympy.symbols('e')]
        for s in range(len(a)):
            sum = 0
            for i in range(len(a)):
                b = a.copy()
                b.remove(b[i])
                print(a[i] * Random.todd.td(s, b))
                sum+=a[i] * Random.todd.td(s, b)
            print(sympy.simplify(sum))
            print('-'*10)

    def test_getSubGraphs(self):
        network = MyNetworkX()
        edges = [(0, 1), (1, 2), (0, 3), (3, 4), (1, 4)]
        weights = ["1", "1", "1", "5", "2"]
        # edges = [(0, 1), (1, 2), (0, 3), (3, 4), (1, 4)]
        # weights = [1.1, 1.2, 1.5, 5, 2]
        network.update(edges, weights)

        getSubGraphs(network.graph, 0)

    def test_getPointNumber(self):
        network = MyNetworkX()
        edges = [(0, 1), (1, 2), (0, 3), (3, 4), (1, 4)]
        weights = ["1", "1", "1", "5", "2"]
        # edges = [(0, 1), (1, 2), (0, 3), (3, 4), (1, 4)]
        # weights = [1.1, 1.2, 1.5, 5, 2]
        network.update(edges, weights)

        getPointNumber(network, 10, 0)

    def test_getAllPaths(self):
        network = MyNetworkX()
        edges = [(0, 1), (1, 2), (0, 3), (3, 4), (1, 4)]
        weights = ["1", "1", "1", "5", "2"]
        # edges = [(0, 1), (1, 2), (0, 3), (3, 4), (1, 4)]
        # weights = [1.1, 1.2, 1.5, 5, 2]
        network.update(edges, weights)

        paths = getAllPaths(network.graph, 0)

    def test_rk(self):
        weights = [2*sympy.sqrt(2), 2*sympy.sqrt(3)]
        T = sympy.symbols("T")

        print(build_rk(2, T, weights))
        w = [2*sympy.sqrt(2)]

        print(build_rk(1, T, w))

    def test_Poly(self):
        x = sympy.symbols("x")
        a = Poly(sqrt(3)*x**2 + x**3 + 2*x)
        print(a)

if __name__ == '__main__':
    unittest.main()