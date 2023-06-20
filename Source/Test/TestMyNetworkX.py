import unittest

import networkx

from Data.MetricGraph import MyNetworkX


def _before() -> MyNetworkX:
    network = MyNetworkX()
    edges = [(0, 1), (1, 2), (0, 3), (3, 4), (1, 4)]
    weights = ["1", "1", "1", "5", "2"]
    #weights = [1.1, 1.2, 1.5, 5, 2]
    #edges = [(0, 1), (1, 2), (0, 3), (3, 4), (1, 4)]
    #weights = [1.1, 1.2, 1.5, 5, 2]
    network.update(edges, weights)
    return network


class TestMyNetworkX(unittest.TestCase):


    def test_add_edges(self):
        network = MyNetworkX()
        nodes = [0, 1, 2, 3, 4]
        edges = [(0, 1), (1, 2), (0, 3), (3, 4), (1, 4)]
        weights = [1.1, 1.2, 1.5, 5, 2]
        network.update(edges, weights)

        for edge in edges:
            self.assertIn(edge, network.graph.edges)
        for node in nodes:
            self.assertIn(node, network.graph.nodes)
        self.assertEqual(network.min_weight, 1.1)

        nodes.append(5)
        edges.append((2, 5))
        weights = [1.1, 1.2, 1.5, 5, 2, 0.5]  # You can't store weights you need to recalculate them from canvas

        network.update(edges, weights)
        for edge in edges:
            self.assertIn(edge, network.graph.edges)
        for node in nodes:
            self.assertIn(node, network.graph.nodes)

        self.assertEqual(network.min_weight, 0.5)

    # Example https://stackoverflow.com/questions/33078907/get-all-edges-linked-to-a-given-node-in-a-networkx-graph
    def test_find_adjacent_edges(self):
        network = _before()

        for node in network.graph.nodes:
            adj_edges = network.graph.edges(0)
            print(adj_edges, node, network.graph.edges, network.graph.nodes)

    def test_move_points_silly(self):
        network = _before()

        network.set_moving_point(list(network.graph.nodes)[0])
        print(network.moving_points)

        for i in range(200):
            network.move_points_silly(0.5)
            print(len(network.moving_points), len(set(network.moving_points)))#, network.moving_points)

        #for i in network.moving_points:
        #    print(i)

        print('-'*30)

        #for i in set(network.moving_points):
        #    print(i)

    def test_move_points_approx(self):
        network = _before()

        network.set_moving_point(list(network.graph.nodes)[0])
        print(network.moving_points)

        for i in range(200):
            network.move_points_approx(0.5)
            print(len(network.moving_points))#, network.moving_points)
            for j in network.moving_points:
                print(j)

        for i in network.moving_points:
            print(i)

    def test_moving_points_calc_precise(self):
        network = _before()

    def test_shortest_path(self):
        network = _before()

        self.assertEqual(networkx.shortest_path_length(network.graph, 0, 1, 'weight'), 1.1)
        self.assertEqual(networkx.shortest_path_length(network.graph, 0, 0, 'weight'), 0)


    def test_get_interval_coverage(self):
        network = _before()

        d, o = [1, 15, 30], [2, 10, 11]
        eps = 3

        self.assertEqual(network.get_interval_coverage(d, eps), [[-2, 4], [12, 18], [27, 33]])
        self.assertEqual(network.get_interval_coverage(o, eps), [[-1, 5], [7, 14]])

    def test_move_interval(self):
        network = _before()

        a = [[1,2], [5,10], [12, 20], [21, 22]]
        t = 5

        self.assertEqual(network.move_interval(a, t), [[-4,-3], [0,5], [7,15], [16,17]])


    def test_strange_merge(self):
        network = _before()

        d, o = [1, 5, 15], [2, 10, 11]
        eps = 3
        weight = 10

        a = network.get_interval_coverage(d, eps)
        b = network.get_interval_coverage(o, eps)
        #print(a, b)

        self.assertEqual(network._strange_merge(a, b, weight), True)
        #self.assertEqual(network._check_if_gap_is_covered(0, weight, [[-2, 18]]), True)

    def test_actual_times_gap_coverage(self):
        network = _before()

        direction = "LEFT"
        gap1 = [-5, -3]
        gap2 = [-2, 0]
        gap3 = [-1, 1]
        gap4 = [0, 2]
        gap5 = [1, 3]
        arr1 = [[4,10]]
        weight, time_limit = 10, 10
        ########################################## Left 0 ####################################################
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap1, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap2, arr1, direction, weight, time_limit))
        self.assertEqual([[1, 10]], network.get_gap_coverage_times(gap3, arr1, direction, weight, time_limit))
        self.assertEqual([[2, 10]], network.get_gap_coverage_times(gap4, arr1, direction, weight, time_limit))
        self.assertEqual([[3, 10]], network.get_gap_coverage_times(gap5, arr1, direction, weight, time_limit))

        arr2 = [[-5, -4]]
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap1, arr2, direction, weight, time_limit))
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap2, arr2, direction, weight, time_limit))
        self.assertEqual([[1, 10]], network.get_gap_coverage_times(gap3, arr2, direction, weight, time_limit))
        self.assertEqual([[2, 10]], network.get_gap_coverage_times(gap4, arr2, direction, weight, time_limit))
        self.assertEqual([[3, 10]], network.get_gap_coverage_times(gap5, arr2, direction, weight, time_limit))

        arr3 = [[-1, 0]]
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap1, arr3, direction, weight, time_limit))
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap2, arr3, direction, weight, time_limit))
        self.assertEqual([[0.5, 10]], network.get_gap_coverage_times(gap3, arr3, direction, weight, time_limit))
        self.assertEqual([[1, 1], [2, 10]], network.get_gap_coverage_times(gap4, arr3, direction, weight, time_limit))
        self.assertEqual([[3, 10]], network.get_gap_coverage_times(gap5, arr3, direction, weight, time_limit))

        arr4 = [[-1, 1]]
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap1, arr4, direction, weight, time_limit))
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap2, arr4, direction, weight, time_limit))
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap3, arr4, direction, weight, time_limit))
        self.assertEqual([[0.5, 1], [2, 10]], network.get_gap_coverage_times(gap4, arr4, direction, weight, time_limit))
        self.assertEqual([[1, 1], [3, 10]], network.get_gap_coverage_times(gap5, arr4, direction, weight, time_limit))

        arr5 = [[-1.5, 1]]
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap1, arr5, direction, weight, time_limit))
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap2, arr5, direction, weight, time_limit))
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap3, arr5, direction, weight, time_limit))
        self.assertEqual([[0.5, 1.5], [2, 10]], network.get_gap_coverage_times(gap4, arr5, direction, weight, time_limit))
        self.assertEqual([[1, 1.5], [3, 10]], network.get_gap_coverage_times(gap5, arr5, direction, weight, time_limit))

        ########################################## Left w ####################################################
        gap6, gap7, gap8, gap9, gap10 = [20, 25], [13, 15], [10, 12], [9, 11], [8, 10]
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap6, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 4.5]], network.get_gap_coverage_times(gap7, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 3]], network.get_gap_coverage_times(gap8, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 2.5]], network.get_gap_coverage_times(gap9, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 2], [10, 10]], network.get_gap_coverage_times(gap10, arr1, direction, weight, time_limit))

        arr6 = [[26, 30]]
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap6, arr6, direction, weight, time_limit))
        self.assertEqual([[0, 3]], network.get_gap_coverage_times(gap7, arr6, direction, weight, time_limit))
        self.assertEqual([[0, 0]], network.get_gap_coverage_times(gap8, arr6, direction, weight, time_limit))
        self.assertEqual([[]], network.get_gap_coverage_times(gap9, arr6, direction, weight, time_limit))
        self.assertEqual([[10, 10]], network.get_gap_coverage_times(gap10, arr6, direction, weight, time_limit))

        arr7 = [[8, 10]]
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap6, arr7, direction, weight, time_limit))
        self.assertEqual([[0, 3]], network.get_gap_coverage_times(gap7, arr7, direction, weight, time_limit))
        self.assertEqual([[0, 1]], network.get_gap_coverage_times(gap8, arr7, direction, weight, time_limit))
        self.assertEqual([[0, 0.5]], network.get_gap_coverage_times(gap9, arr7, direction, weight, time_limit))
        self.assertEqual([[0, 0], [10, 10]], network.get_gap_coverage_times(gap10, arr7, direction, weight, time_limit))

        arr7 = [[7.5, 10]]
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap6, arr7, direction, weight, time_limit))
        self.assertEqual([[0, 3]], network.get_gap_coverage_times(gap7, arr7, direction, weight, time_limit))
        self.assertEqual([[0, 1.25]], network.get_gap_coverage_times(gap8, arr7, direction, weight, time_limit))
        self.assertEqual([[0, 0.75]], network.get_gap_coverage_times(gap9, arr7, direction, weight, time_limit))
        self.assertEqual([[0, 0.25], [10, 10]], network.get_gap_coverage_times(gap10, arr7, direction, weight, time_limit))

        arr7 = [[7, 9]]
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap6, arr7, direction, weight, time_limit))
        self.assertEqual([[0, 3]], network.get_gap_coverage_times(gap7, arr7, direction, weight, time_limit))
        self.assertEqual([[0, 0], [1, 1.5]], network.get_gap_coverage_times(gap8, arr7, direction, weight, time_limit))
        self.assertEqual([[1, 1]], network.get_gap_coverage_times(gap9, arr7, direction, weight, time_limit))
        self.assertEqual([[0.5, 0.5], [10, 10]], network.get_gap_coverage_times(gap10, arr7, direction, weight, time_limit))

        ########################################## Right 0 ####################################################
        direction = "Right"
        gap6, gap7, gap8, gap9, gap10 = [20, 25], [13, 15], [10, 12], [9, 11], [8, 10]
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap6, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap7, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap8, arr1, direction, weight, time_limit))
        self.assertEqual([[1, 10]], network.get_gap_coverage_times(gap9, arr1, direction, weight, time_limit))
        self.assertEqual([[2, 10]], network.get_gap_coverage_times(gap10, arr1, direction, weight, time_limit))

        gap1, gap2, gap3, gap4, gap5 = [-5, -3], [-2, 0], [-1, 1], [0, 2], [1, 3]
        self.assertEqual([[0, 3], [4, 6.5]], network.get_gap_coverage_times(gap1, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 0], [3, 5]], network.get_gap_coverage_times(gap2, arr1, direction, weight, time_limit))
        self.assertEqual([[2.5, 4.5]], network.get_gap_coverage_times(gap3, arr1, direction, weight, time_limit))
        self.assertEqual([[2, 4], [10, 10]], network.get_gap_coverage_times(gap4, arr1, direction, weight, time_limit))
        self.assertEqual([[1.5, 3.5], [9, 10]], network.get_gap_coverage_times(gap5, arr1, direction, weight, time_limit))

        gap1, gap2, gap3, gap4, gap5 = [-5, -3], [-2, 0], [-1, 1], [0, 2], [1, 3]
        arr1 = [[0, 2]]
        self.assertEqual([[0, 3]], network.get_gap_coverage_times(gap1, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 1]], network.get_gap_coverage_times(gap2, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 0.5]], network.get_gap_coverage_times(gap3, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 0], [10, 10]], network.get_gap_coverage_times(gap4, arr1, direction, weight, time_limit))
        self.assertEqual([[9, 10]], network.get_gap_coverage_times(gap5, arr1, direction, weight, time_limit))

        gap1, gap2, gap3, gap4, gap5 = [-5, -3], [-2, 0], [-1, 1], [0, 2], [1, 3]
        arr1 = [[0.5, 2.5]]
        self.assertEqual([[0, 3]], network.get_gap_coverage_times(gap1, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 0], [0.5, 1.25]], network.get_gap_coverage_times(gap2, arr1, direction, weight, time_limit))
        self.assertEqual([[0.5, 0.75]], network.get_gap_coverage_times(gap3, arr1, direction, weight, time_limit))
        self.assertEqual([[0.25, 0.25], [10, 10]], network.get_gap_coverage_times(gap4, arr1, direction, weight, time_limit))
        self.assertEqual([[9, 10]], network.get_gap_coverage_times(gap5, arr1, direction, weight, time_limit))

        gap1, gap2, gap3, gap4, gap5 = [-5, -3], [-2, 0], [-1, 1], [0, 2], [1, 3]
        arr1 = [[0.5, 2]]
        self.assertEqual([[0, 3]], network.get_gap_coverage_times(gap1, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 0], [0.5, 1]], network.get_gap_coverage_times(gap2, arr1, direction, weight, time_limit))
        self.assertEqual([[0.5, 0.5]], network.get_gap_coverage_times(gap3, arr1, direction, weight, time_limit))
        self.assertEqual([[10, 10]], network.get_gap_coverage_times(gap4, arr1, direction, weight, time_limit))
        self.assertEqual([[9, 10]], network.get_gap_coverage_times(gap5, arr1, direction, weight, time_limit))

        ########################################## Right w ####################################################
        gap6, gap7, gap8, gap9, gap10 = [13, 15], [10, 12], [9, 11], [8, 10], [7, 9]
        arr1 = [[5, 8]]
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap6, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap7, arr1, direction, weight, time_limit))
        self.assertEqual([[1, 10]], network.get_gap_coverage_times(gap8, arr1, direction, weight, time_limit))
        self.assertEqual([[2, 10]], network.get_gap_coverage_times(gap9, arr1, direction, weight, time_limit))
        self.assertEqual([[3, 10]], network.get_gap_coverage_times(gap10, arr1, direction, weight, time_limit))

        gap6, gap7, gap8, gap9, gap10 = [13, 15], [10, 12], [9, 11], [8, 10], [7, 9]
        arr1 = [[11, 13]]
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap6, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap7, arr1, direction, weight, time_limit))
        self.assertEqual([[1, 10]], network.get_gap_coverage_times(gap8, arr1, direction, weight, time_limit))
        self.assertEqual([[1.5, 10]], network.get_gap_coverage_times(gap9, arr1, direction, weight, time_limit))
        self.assertEqual([[2, 10]], network.get_gap_coverage_times(gap10, arr1, direction, weight, time_limit))

        gap6, gap7, gap8, gap9, gap10 = [13, 15], [10, 12], [9, 11], [8, 10], [7, 9]
        arr1 = [[10, 12]]
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap6, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap7, arr1, direction, weight, time_limit))
        self.assertEqual([[0.5, 10]], network.get_gap_coverage_times(gap8, arr1, direction, weight, time_limit))
        self.assertEqual([[1, 10]], network.get_gap_coverage_times(gap9, arr1, direction, weight, time_limit))
        self.assertEqual([[1.5, 2], [3, 10]], network.get_gap_coverage_times(gap10, arr1, direction, weight, time_limit))

        gap6, gap7, gap8, gap9, gap10 = [13, 15], [10, 12], [9, 11], [8, 10], [7, 9]
        arr1 = [[9, 11]]
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap6, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap7, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap8, arr1, direction, weight, time_limit))
        self.assertEqual([[0.5, 1], [2, 10]], network.get_gap_coverage_times(gap9, arr1, direction, weight, time_limit))
        self.assertEqual([[1, 1], [3, 10]], network.get_gap_coverage_times(gap10, arr1, direction, weight, time_limit))

        gap6, gap7, gap8, gap9, gap10 = [13, 15], [10, 12], [9, 11], [8, 10], [7, 9]
        arr1 = [[10, 11]]
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap6, arr1, direction, weight, time_limit))
        self.assertEqual([[0, 10]], network.get_gap_coverage_times(gap7, arr1, direction, weight, time_limit))
        self.assertEqual([[0.5, 10]], network.get_gap_coverage_times(gap8, arr1, direction, weight, time_limit))
        self.assertEqual([[1, 1], [2, 10]], network.get_gap_coverage_times(gap9, arr1, direction, weight, time_limit))
        self.assertEqual([[3, 10]], network.get_gap_coverage_times(gap10, arr1, direction, weight, time_limit))

    def test_get_times_of_coverage(self):
        network = _before()

        arr = [[-5, -3], [-2.5, 2], [3, 9], [10, 11], [15, 19]]
        gap = [12, 13]
        weight = 11.5
        direction = "LEFT"
        time_limit = 10

        ans = network.get_gap_coverage_times(gap, arr, direction, weight, time_limit)
        print(ans)

        arr = [[15, 20]]
        ans = network.get_gap_coverage_times(gap, arr, direction, weight, time_limit)
        print(ans)

        arr = [[10.5, 11]]
        ans = network.get_gap_coverage_times(gap, arr, direction, weight, time_limit)
        print(ans)

        gap = [1,2]
        arr = [[-1,-0.5]]
        ans = network.get_gap_coverage_times(gap, arr, direction, weight, time_limit)
        print(ans)

if __name__ == '__main__':
    unittest.main()