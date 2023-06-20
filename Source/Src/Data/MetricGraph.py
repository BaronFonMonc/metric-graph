import networkx as nx
import sympy
from sympy import Rational

import Data.Utils
from Data.MovingPoint import MovingPoint
from Data.Utils import norm_edge, getOtherPoint
from latex2sympy2 import latex2sympy, latex2latex


class MyNetworkX:

    def __init__(self):
        self.graph = nx.Graph()
        self.moving_points = []
        self.min_weight = None
        self.node_positions = dict()

    def get_adjacent(self, node):
        return self.graph.edges(node)

    def __get_destination_point(self, edge, node):
        if edge[0] == node:
            return edge[1]
        else:
            return edge[0]

    # Move points by delta. Each edge can have only one point.
    # TODO: Redundant. Can be deleted
    def move_points_approx(self, delta):

        add_later = dict()
        occupied_later = []
        # remove_later = []

        for point in self.moving_points:
            point.dist = point.dist + delta
            if point.dist >= point.length:
                for edge in self.get_adjacent(point.dir):
                    if not (edge in self.occupied_edges or self.__reverse_edge(edge) in self.occupied_edges):
                        norm_edge = (min(edge[0], edge[1]), max(edge[0], edge[1]))
                        if norm_edge not in add_later:
                            add_later[norm_edge] = []
                            occupied_later.append(norm_edge)
                        add_later[norm_edge].append(MovingPoint(edge,
                                                                self.get_weight(edge),
                                                                self.__get_destination_point(edge, point.dir),
                                                                point.dist - point.length))
                point.dist = point.dist - point.length
                point.dir = self.__get_destination_point(point.edge, point.dir)
                point.edge = self.__reverse_edge(point.edge)

        for edge in add_later:
            fastest = add_later[edge][0]
            for i in add_later[edge]:
                if i.dist > fastest.dist:
                    fastest = i
            self.moving_points.append(fastest)

        self.occupied_edges.extend(occupied_later)

    # Move points by delta. Each edge can have multiple points.
    def move_points_silly(self, delta):

        add_later = []
        remove_later = []

        for point in self.moving_points:
            point.dist = point.dist + delta
            if point.dist >= point.length:
                remove_later.append(point)
                for edge in self.get_adjacent(point.dir):
                    add_later.append(MovingPoint(edge,
                                                 self.get_weight(edge),
                                                 self.__get_destination_point(edge, point.dir),
                                                 point.dist - point.length))
                # point.old_pos = point.pos
                # point.mid_pos =
        self.moving_points = [i for i in self.moving_points if i not in remove_later]
        self.moving_points.extend(add_later)
        self.moving_points = [i for i in set(self.moving_points)]

    # Returns next moment when some point hit its vertice.
    def get_points_next_moment(self):
        fastest_time = self.moving_points[0].length - self.moving_points[0].dist
        for i in self.moving_points:
            if i.length - i.dist < fastest_time:
                fastest_time = i.length - i.dist

        return fastest_time

    # Move points to next moment when some point hit its vertice.
    def move_points_to_next_moment(self):
        moment = self.get_points_next_moment()
        self.move_points_silly(moment)
        return moment

    # Check if in current position points form an e-net
    # For each point check which part of edge its covering
    #   need to calculate distance from point to other edges
    #   For both vertices of edge calculate distance to other vertices
    # For each edge for each point save interval of coverage (Epsilon-distance)
    def check_saturation(self, epsilon):

        coverage = dict()
        for edge in self.graph.edges:
            norm_edge = self.__norm_edge(edge)
            coverage[norm_edge] = [0] * len(self.moving_points)
            for i in range(len(self.moving_points)):
                coverage[norm_edge][i] = []

        mp_index = 0
        for mp in self.moving_points:
            norm = self.__norm_edge(mp.edge)
            coverage[norm][mp_index].append([max(0, mp.dist - epsilon), min(mp.length, mp.dist + epsilon)])

            dir_node = mp.dir
            other_node = self.__get_destination_point(mp.edge, mp.dir)
            dir_dist = mp.length - mp.dist
            other_dist = mp.dist

            for node in self.graph.nodes:
                # if node not in (dir_node, other_node):
                path_dir = nx.shortest_path_length(self.graph, dir_node, node,
                                                   'weight') + dir_dist  # Change later to BFS
                path_other = nx.shortest_path_length(self.graph, other_node, node, 'weight') + other_dist
                best_path = min(path_dir, path_other)
                if best_path < epsilon:
                    for edge in self.get_adjacent(node):
                        norm_edge = self.__norm_edge(edge)
                        if (edge[0] == norm_edge[0]) and (edge[1] == norm_edge[1]):
                            if edge[0] == node:
                                coverage[norm_edge][mp_index].append(
                                    [0, min(epsilon - best_path, self.get_weight(edge))])
                            else:
                                coverage[norm_edge][mp_index].append(
                                    [max(0, self.get_weight(edge) + best_path - epsilon), self.get_weight(edge)])
                        else:
                            if edge[1] == node:
                                coverage[norm_edge][mp_index].append(
                                    [0, min(epsilon - best_path, self.get_weight(edge))])
                            else:
                                coverage[norm_edge][mp_index].append(
                                    [max(0, self.get_weight(edge) + best_path - epsilon), self.get_weight(edge)])
            mp_index += 1
        flag = True
        Res = dict()
        for edge in coverage:
            cov = []
            for i in range(mp_index):
                for j in coverage[edge][i]:
                    cov.append(j)
            res = Data.Utils.concat_intervals(cov)
            if res == []:
                flag = False
            elif res[0] == []:
                flag = False
            elif not (res[0][0] == 0 and res[0][1] == self.get_weight(edge)):
                flag = False
            Res[edge] = res
        return (Res, flag)  # What part of edges is covered, IsCovered?

    # Check if moving points can form an e-net starting from now, till corresponding moment (when some point hits it vertice).
    # This moment should be calulated by get_points_next_moment() method
    def check_saturation_between_moments_redundant(self, moment, epsilon):

        t_coverage = []  # contains moments when edge is covered (during specific t which is smaller than moment)

        for edge in self.graph.edges:
            empty = True
            MP = None
            for mp in self.moving_points:
                if (mp.edge in (edge, self.__reverse_edge(edge))):
                    empty = False
                    MP = mp
            if empty:
                # if 2 points close enough in normal edge
                # if edge is hanging, check the epsilon smaller than weight. Check there is close enough point.
                res = []
                length = self.get_weight(edge)
                dir_node = edge[0]
                other_node = edge[1]

                if length > 2 * epsilon:
                    t_coverage.append([])
                else:

                    path_d_d = []
                    path_d_o = []
                    path_o_d = []
                    path_o_o = []

                    for mp in self.moving_points:
                        dir_node_mp = mp.dir
                        other_node_mp = self.__get_destination_point(mp.edge, mp.dir)
                        dir_dist_mp = mp.length - mp.dist  # - t
                        other_dist_mp = mp.dist  # + t

                        path_d_d.append(
                            nx.shortest_path_length(self.graph, dir_node_mp, dir_node, 'weight') + dir_dist_mp)  # - t
                        path_d_o.append(nx.shortest_path_length(self.graph, other_node_mp, dir_node,
                                                                'weight') + other_dist_mp)  # + t
                        path_o_d.append(
                            nx.shortest_path_length(self.graph, dir_node_mp, other_node, 'weight') + dir_dist_mp)  # - t
                        path_o_o.append(nx.shortest_path_length(self.graph, other_node_mp, other_node,
                                                                'weight') + other_dist_mp)  # + t

                    shortest_path_d_d = min(path_d_d)  # - t
                    shortest_path_d_o = min(path_d_o)  # + t
                    shortest_path_o_d = min(path_o_d)  # - t
                    shortest_path_o_o = min(path_o_o)  # + t

                    if len(self.get_adjacent(dir_node)) == 0:  # dir is hanging
                        if shortest_path_d_d - moment <= epsilon:
                            res.append([max(0, shortest_path_d_d - epsilon), moment])
                        if shortest_path_d_o <= epsilon:
                            res.append([0, min(moment, shortest_path_d_o - epsilon)])
                    elif len(self.get_adjacent(other_node)) == 0:  # other is hanging
                        if shortest_path_o_d - moment <= epsilon:
                            res.append([max(0, shortest_path_o_d - epsilon), moment])
                        if shortest_path_o_o <= epsilon:
                            res.append([0, min(moment, shortest_path_o_o - epsilon)])
                    else:  # nothing is hanging
                        if shortest_path_d_d + shortest_path_o_d - 2 * moment < 2 * epsilon - length:  # - 2t
                            res.append(
                                [max(0, shortest_path_d_d + shortest_path_o_d - 2 * epsilon + length) / 2, moment])
                        if shortest_path_d_d + shortest_path_o_o < 2 * epsilon - length:  # 0
                            res.append([0, moment])
                        if shortest_path_d_o + shortest_path_o_d < 2 * epsilon - length:  # 0
                            res.append([0, moment])
                        if shortest_path_d_o + shortest_path_o_o < 2 * epsilon - length:  # + 2t
                            res.append(
                                [0, min(moment, (shortest_path_d_o + shortest_path_o_o - 2 * epsilon + length) / 2)])
                    res = Data.Utils.concat_intervals(res)
                    t_coverage.append(res)
            else:
                dir, other = [], []
                dir_node = MP.dir
                other_node = self.__get_destination_point(MP.edge, MP.dir)
                dir_dist = MP.length - MP.dist  # - t
                other_dist = MP.dist  # + t

                if dir_dist - moment <= epsilon:
                    dir.append([max(0, dir_dist - epsilon), moment])
                if other_dist <= epsilon:
                    other.append([0, min(epsilon - other_dist, moment)])

                for mp in self.moving_points:
                    if mp != MP:
                        dir_node_mp = mp.dir
                        other_node_mp = self.__get_destination_point(mp.edge, mp.dir)
                        dir_dist_mp = mp.length - mp.dist  # - t
                        other_dist_mp = mp.dist  # + t

                        path_d_d = nx.shortest_path_length(self.graph, dir_node_mp, dir_node, 'weight')
                        path_d_o = nx.shortest_path_length(self.graph, other_node_mp, dir_node, 'weight')
                        path_o_d = nx.shortest_path_length(self.graph, dir_node_mp, other_node, 'weight')
                        path_o_o = nx.shortest_path_length(self.graph, other_node_mp, other_node, 'weight')

                        # dir - dir # dir+dir_mp+path-2t < 2Epsilon
                        if path_d_d + dir_dist + dir_dist_mp - 2 * moment <= 2 * epsilon:  # -2t
                            dir.append([max(0, path_d_d + dir_dist + dir_dist_mp - 2 * epsilon) / 2, moment])

                        # dir - oth # dir+oth_mp+path < 2Epsilon
                        if path_d_o + dir_dist + other_dist_mp <= 2 * epsilon:  # 0
                            dir.append([0, moment])

                        # oth - dir # oth+dir_mp+b+path < 2Epsilon
                        if path_o_d + other_dist + dir_dist_mp <= 2 * epsilon:  # 0
                            other.append([0, moment])

                        # oth - oth # oth+oth_mp+path+2t < 2Epsilon
                        if path_o_o + other_dist + other_dist_mp <= 2 * epsilon:  # +2t
                            other.append([0, min(moment, (2 * epsilon - path_o_o - other_dist - other_dist_mp) / 2)])

                other = Data.Utils.concat_intervals(other)
                dir = Data.Utils.concat_intervals(dir)
                res = Data.Utils.get_intersections([other, dir])
                t_coverage.append(res)

        # based on coverage need to give result
        res_t = Data.Utils.get_intersections(t_coverage)

        print(t_coverage)  # TODO: Delete this
        return (res_t, res_t != [])

    # Actual method.
    # Divide points on edge into 2 groups
    # Move them towards each other
    # check
    def check_saturation_between_moments(self, moment, epsilon):
        t_coverage = [[0, moment]]
        point_to_edges = dict()
        for e in self.graph.edges:
            point_to_edges[norm_edge(e)] = []
        for mp in self.moving_points:
            point_to_edges[norm_edge(mp.edge)].append(mp)

        for e in self.graph.edges:
            edge = norm_edge(e)
            dn, on = edge[0], edge[1]
            dir, other = [], [] #red, blue

            for mp in point_to_edges[edge]:
                if mp.dir == dn:
                    dir.append(mp.dist)
                else:
                    other.append(mp.dist)


            # add to dir the closest one from left
            # add to other the closest one from right
            # for each mp: find the shortest path to edge[0] and edge[1]:
            # from mp.edge[0] and mp.edge[1]: add to those path dir and edge.weight-dir

            d_d, d_o, o_d, o_o = 10000000, 10000000, 10000000, 10000000

            for mp in self.moving_points:
                if norm_edge(mp.edge)==edge:
                    continue
                dir_node, other_node = mp.dir, self.__get_destination_point(mp.edge, mp.dir)
                dir_dist_mp, other_dist_mp = mp.length - mp.dist, mp.dist


                d_d = min(d_d, nx.shortest_path_length(self.graph, dn, dir_node, 'weight') + dir_dist_mp) # blue
                d_o = min(d_o, nx.shortest_path_length(self.graph, on, dir_node, 'weight') + dir_dist_mp) # red
                o_d = min(o_d, nx.shortest_path_length(self.graph, dn, other_node, 'weight') + other_dist_mp) # red
                o_o = min(o_o, nx.shortest_path_length(self.graph, on, other_node, 'weight') + other_dist_mp)  # blue
            other.append(d_d + self.get_weight(edge))
            other.insert(0, -o_o)
            dir.append(o_d + self.get_weight(edge))
            dir.insert(0, -d_o)

            # after dir and other complete: calculate how much they cover: +- epsilon intervals: merge them
            # then for dir find first (from right to left) not closed gap: find the closest to the right non-gap in other
            # other move: calculate gaps: if none find how long it will last (find closest gap in other to another gap in dir): else repeat

            dir = self.get_interval_coverage(dir, epsilon)
            other = self.get_interval_coverage(other, epsilon)

            gaps = [[0, moment]]
            for i in range(len(dir)-1):
                gap = self._get_gap(dir, i)
                ans = self.get_gap_coverage_times(gap, other, "RIGHT", self.get_weight(edge), moment)
                print(ans)
                gaps = Data.Utils.intervalIntersection(ans, gaps)
            if dir[0][0]>0:
                gap = [0, dir[0][0]]
                ans = self.get_gap_coverage_times(gap, other, "RIGHT", self.get_weight(edge), moment)
                print(ans)
                gaps = Data.Utils.intervalIntersection(ans, gaps)
            if dir[-1][1]<self.get_weight(edge):
                gap = [dir[-1][1], self.get_weight(edge)]
                ans = self.get_gap_coverage_times(gap, other, "RIGHT", self.get_weight(edge), moment)
                print(ans)
                gaps = Data.Utils.intervalIntersection(ans, gaps)

            for i in range(len(other)-1):
                gap = self._get_gap(other, i)
                ans = self.get_gap_coverage_times(gap, dir, "LEFT", self.get_weight(edge), moment)
                print(ans)
                gaps = Data.Utils.intervalIntersection(ans, gaps)
            if other[0][0] > 0:
                gap = [0, other[0][0]]
                ans = self.get_gap_coverage_times(gap, dir, "LEFT", self.get_weight(edge), moment)
                print(ans)
                gaps = Data.Utils.intervalIntersection(ans, gaps)
            if other[-1][1] < self.get_weight(edge):
                gap = [other[-1][1], self.get_weight(edge)]
                ans = self.get_gap_coverage_times(gap, dir, "LEFT", self.get_weight(edge), moment)
                print(ans)
                gaps = Data.Utils.intervalIntersection(ans, gaps)
            print("Gaps are:", gaps)
            t_coverage = Data.Utils.intervalIntersection(t_coverage, gaps)
            print("T_coverage is:",t_coverage)
            if t_coverage==[]:
                return (t_coverage!=[], t_coverage)

        return (t_coverage!=[], t_coverage)


    def get_interval_coverage(self, centers, epsilon):
        centers = sorted(centers)
        ans = [0]*len(centers)

        for i in range(len(centers)):
            ans[i] = [centers[i]-epsilon, centers[i]+epsilon]
        return Data.Utils.concat_intervals(ans)


    # arr = [[1,2], [3,4], [5,6], [7,8]]
    # i = 0 -> ans = [2,3]
    # i = 1 -> ans = [4,5]
    # i = 2 -> ans = [6,7]
    def _get_gap(self, arr, i):
        return [arr[i][1], arr[i+1][0]]


    # gap = [1,2]
    # arr = [[1,3], [2,5], [6,7]] # opposing array (dir or other)
    # direction -> which way interval moves (LEFT, RIGHT)
    def get_gap_coverage_times(self, gap, arr, direction, weight, time_limit):
        time = []
        gap_len = self._interval_len(gap)
        if direction == "LEFT":
            if gap[0] < 0:
                gap[0] = 0
            if gap[0] >= weight:
                time.append([0, gap[0]-weight])
            if gap[1] <= 0:
                time.append([0, time_limit])
            elif gap[1] <= time_limit:
                time.append([gap[1], time_limit])
            for interval in arr:
                if self._interval_len(interval) >= gap_len:
                    if interval[0] <= gap[0]:
                        time.append([max(0, gap[1] - interval[1]) / 2, (gap[0] - interval[0]) / 2])
                        if (gap[0] - interval[0]) / 2 > time_limit:
                            break
                if interval[0] < 0: # 0
                    if interval[1] <= gap[1]:
                        t = (gap[1] - interval[1])/2
                        if - interval[0] >= max(t, gap[0]):
                            time.append([ max(t, gap[0]), - interval[0]])
                if gap[1] > weight: # weight
                    if interval[0] <= gap[0]:
                        t = (gap[0] - interval[0]) / 2
                        t2 = max(0, weight - interval[1])
                        t3 = max(0, gap[0] - weight)
                        if max(t2, t3) <= t:
                            time.append([max(t2, t3), t])
        else:
            if gap[0] >= weight:
                time.append([0, time_limit])
            elif time_limit >= weight - gap[0]:
                time.append([weight - gap[0], time_limit])
            if gap[1] <= 0:
                time.append([0, -gap[1]])
            for interval in arr:
                if self._interval_len(interval) >= gap_len:
                    if interval[1] > gap[1]:
                        time.append([max(0, interval[0] - gap[0]) / 2, (interval[1] - gap[1]) / 2])
                        if (interval[1] - gap[1]) / 2 > time_limit:
                            break

                if interval[1] > weight:
                    if interval[0] >= gap[0]:
                        t = max((interval[0] - gap[0]) / 2, weight - gap[1])
                        t2 = max(0, weight - gap[0])
                        t3 = max(0, interval[1] - weight)
                        if min(t2,t3) >= t:
                            time.append([ t, min(t2,t3)])
                if gap[0] <= 0:
                    if gap[1] <= interval[1]:
                        t = (interval[1] - gap[1]) / 2
                        t2 = max(0, -gap[0])
                        t3 = max(0, interval[0])
                        t4 = max(0, -gap[1])
                        if max(t3, t4) <= min(t, t2):
                            time.append([max(t3, t4), min(t,t2)])
        time = Data.Utils.intervalIntersection(Data.Utils.concat_intervals(time), [[0, weight]])
        if time!=[]:
            return time
        return [[]]



    # dir [[-2, 4], [12, 18], [27, 33]] # +1
    # oth [[-1, 5], [7, 14]] # -1
    # dir +; oth -;
    # weight - edge len
    # Probably non relevant
    def get_times_of_coverage(self, dir, other, weight, time_limit):
        print("DIR:OTHER:", dir, other)
        ans = []
        t = 0
        dir_gap = len(other)-2 # The number of gap in dir that is "righter" than rigth node.
        other_gap = 0 # The number of gap in other that is "lefter" than left node.
        #cur_dir_gap = 0
        #cur_other_gap = len(other)-2

        #while cur_dir_gap < len(dir)-1 and cur_other_gap >= 0 and t <= time_limit:
        #    print("Current dir_gap:", cur_dir_gap, self._get_gap(dir, cur_dir_gap),
        #          "Current other_gap:", cur_other_gap, self._get_gap(other, cur_other_gap))

            #while cur_dir_gap < dir_gap and t <= time_limit:
            #    dg = self._get_gap(dir, cur_dir_gap)
            #    print(dg)
            #    covered = False
            #    while cur_other_gap <= len(other)-1 and not covered:
            #        if self._interval_len(other[cur_other_gap])>=self._interval_len(dg):
            #            if dg[1]<other[cur_other_gap][1]:
            #                covered = True
            #    if not covered:
            #        print("This gap can never be covered", dg)
            #        return ans
        i,j = 0,0
        while t <= time_limit and (dir_gap>=0 or other_gap<=len(other)-2):
            # need to check when whole dir is covered
            while i <= dir_gap and t<=time_limit:
                # check when i will be covered
                covered = False
                moved = False

                dg = self._get_gap(dir, i)
                if dg[0] > weight:
                    dir_gap = i-1
                    break
                for J in range(other_gap, len(other)):
                    if self._interval_len(dg) < self._interval_len(other[J]):
                        if dg[1] <= other[J][1]:
                            if other[J][0] > dg[0]:
                                d = (other[J][0]-dg[0])/2
                                t += d
                                dir, other = self.move_interval(dir, d), self.move_interval(other, d)
                                moved = True
                            covered = True
                            break
                if not covered:
                    print("This gap can never be covered", dg)
                    return ans
                if covered and moved:
                    i,j = 0, other_gap
                else:
                    i += 1

            moved_j = False
            # now need to check other
            while j <= len(other)-2 and t<=time_limit:
                # check when j will be covered
                covered = False
                moved = False
                og = self._get_gap(other, j)
                if og[1] < 0:
                    other_gap = j + 1
                    j += 1
                else:
                    for I in range(0, dir_gap):
                        if self._interval_len(og) < self._interval_len(dir[I]):
                            if dir[I][0] <= og[0]:
                                if dir[I][1] < og[1]:
                                    d = (og[1] - dir[I][1]) / 2
                                    t += d
                                    dir, other = self.move_interval(dir, d), self.move_interval(other, d)
                                    moved = True
                                    moved_j = True
                                covered = True
                                break
                    if not covered:
                        print("This gap can never be covered", og)
                        return ans
                    if covered and moved:
                        i,j = 0,other_gap
                    else:
                        j += 1
            # both now covered. Need to check how long it will last.
            if not moved_j:
                if not self._strange_merge(dir, other, weight):
                    print("WHAT!!!!!???? WHY!??? It is not covered?!?!?!?!?")

                min_t = 10000000000000

                for i in range(dir_gap+1):
                    dg = self._get_gap(i)
                    for j in range(other_gap, len(other)):
                        if dg[0] <= other[j][0] and dg[1] <= other[j][1]:
                            min_t = min(min_t, (other[j][1] - dg[1]) / 2)
                            break
                for j in range(other_gap, len(other)-1):
                    og = self._get_gap(j)
                    for i in range(dir_gap+1):
                        if og[0] <= dir[i][0] and og[1] <= dir[i][1]:
                            min_t = min(min_t, (og[0] - dir[i][0]) / 2)
                            break
                ans.append([t,t+min_t])
                t += min_t + Rational(1, 1000)
                dir, other = self.move_interval(dir, min_t), self.move_interval(other, min_t + Rational(1, 1000))

        return ans


    def _interval_len(self, a):
        return a[1]-a[0]

    # Check if edge is covered
    # weight = len of edge
    def _strange_merge(self, dir, other, weight):
        ans = dir
        for i in other:
            ans.append(i)
        ans = Data.Utils.concat_intervals(ans)
        #print(ans)
        for i in ans:
            if i[0] <= 0 and i[1] >= weight:
                return True
        return False


    # interval: [[1,2], [3,6], [9,10]] -> [[1-t,2-t], [3-t,6-t], [9-t,10-t]]
    def move_interval(self, interval, t):
        for i in range(len(interval)):
            interval[i] = [interval[i][0] - t, interval[i][1] - t]
        return interval

    # We need to prohibit set delta t bigger than smallest edge (so we won't need to calculate 3 edges)
    # We can say this is because of irrationality

    def __norm_edge(self, edge):
        return (min(edge[0], edge[1]), max(edge[0], edge[1]))

    def get_weight(self, edge):
        return self.graph.edges[edge]['weight']

    # Just reverse an edge. If edge is (1,2) reversed one is (2,1)
    def __reverse_edge(self, edge):
        return (edge[1], edge[0])

    # Set initial position of moving points
    def set_moving_point(self, node):
        self.moving_points = []
        self.occupied_edges = []
        for edge in self.get_adjacent(node):
            self.moving_points.append(
                MovingPoint(edge, self.get_weight(edge), self.__get_destination_point(edge, node), 0))
            self.occupied_edges.append(edge)



    # Remove all edges and nodes, and add a new one
    # Weights should be float or sympy
    def update(self, edges, weights, source):
        if len(weights) != len(edges):
            print("WEIGHTS AND EDGES OF DIFFERENT DIMENSIONS!")
            #weights = [-1] * len(edges)
            return 1

        self.graph = nx.Graph()

        weighted_edges = []

        for i in range(len(edges)):
            print(weights[i], latex2sympy(weights[i]))
            weights[i] = latex2sympy(weights[i])

            #tex = r"\frac{d}{dx}(x^{2}+x)"
            # Or you can use '\mathrm{d}' to replace 'd'
            #latex2sympy(tex)
            # => "Derivative(x**2 + x, x)"
            #latex2latex(tex)

            #if weights[i][0] == '/':
            #    weights[i] = sympy.sqrt(int(weights[i][1:]))
            #else:
            #    weights[i] = sympy.symbols(weights[i])
                #weights[i] = sympy.simplify(
                #    int(weights[i]))  # TODO FLOATS. As frac. a/b where b is 10^k k- number of symbols after ,

            weighted_edges.append((edges[i][0], edges[i][1], sympy.simplify(weights[i])))
            if not weighted_edges[-1][2].is_number:
                return 2

        #self.min_weight = min(weights)

        print(weights)

        self.graph.add_weighted_edges_from(weighted_edges)

        print(source)
        if len(source)>0:
            self.set_moving_point(list(self.graph.nodes)[source[0]])
        else:
            self.set_moving_point(list(self.graph.nodes)[0])  # self.graph.nodes[0] not working
        return 0
