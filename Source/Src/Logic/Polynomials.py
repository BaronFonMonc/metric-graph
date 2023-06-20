import itertools

import networkx as nx
from collections import deque
import sympy
import numpy as np
from numpy import linalg
from sympy import poly, Poly

import Random.todd
from Data.Utils import getOtherPoint, norm_edge
#from networkx.algorithms.polynomials import tutte_polynomial

#Call this method If edge is bridge. If it multyedge return true.
def is_bridge_but_multi(G,v1,v2):
    count = 0
    for i in G.edges:
        if i[0] == v1 and i[1] == v2:
            count += 1
            if count > 1:
                return True
    return False

def tutte_polynomial(G):
    #var('x,y')
    x = sympy.Symbol("x")
    y = sympy.Symbol("y")
    stack = deque()
    stack.append(nx.MultiGraph(G))
    #stack.append(nx.Graph(G))

    polynomial = 0
    while stack:
        G = stack.pop()
        #print(Polynomial, G.edges, nx.Graph(G).edges
        #print(polynomial,G.edges,set(nx.bridges(G)),list(nx.selfloop_edges(G, keys=True)))
        #print(nx.has_bridges(G))
        #for i in nx.bridges(G):
        #    print(i)

        bridges = set(nx.bridges(nx.Graph(G)))

        e = None
        for i in G.edges:
            if (((i[0], i[1]) not in bridges) and (i[0] != i[1])) or ((i[0], i[1]) in bridges and is_bridge_but_multi(G,i[0],i[1])):
                e = i
                break
        if not e:
            loops = list(nx.selfloop_edges(G, keys=True))
            polynomial += x ** len(bridges) * y ** len(loops)
        else:
            # deletion-contraction
            C = nx.contracted_edge(G, e, self_loops=True)
            C.remove_edge(e[0], e[0])
            G.remove_edge(*e)
            stack.append(G)
            stack.append(C)

    return sympy.expand(polynomial)

def critical_configuration_polynomial(G):
    x = sympy.Symbol("x")
    y = sympy.Symbol("y")
    pol = tutte_polynomial(G)
    res_pol = pol.subs(x,1)
    return res_pol

def zonotope_polynomial(G):
    x = sympy.Symbol("x")
    y = sympy.Symbol("y")
    t = sympy.Symbol("t")
    pol = tutte_polynomial(G)

    D = np.zeros(shape=(len(G.nodes),len(G.edges)))
    mapping_n = dict(zip(G, range(0, len(G.nodes))))
    G = nx.relabel_nodes(G, mapping_n)

    i = 0
    for edge in G.edges:
        D[int(edge[0])][i] = 1
        D[int(edge[1])][i] = 1
        i += 1
    #print(D)
    #print(linalg.matrix_rank(D))

    res_pol = pol.subs(x,1+1/t)
    res_pol = res_pol.subs(y,1)
    res_pol = res_pol * (t**linalg.matrix_rank(D))

    return sympy.expand(res_pol)


#C = nx.cycle_graph(5)
#print(tutte_polynomial(C))

#import sympy
#x = sympy.Symbol("x")
#G = nx.complete_graph(4)
#A = nx.adjacency_matrix(G)
#M = sympy.SparseMatrix(A.todense())
#print(M.charpoly(x).as_expr())

# Return set of connected subgraphs that contain s
# s - source
def getSubGraphs(graph, s):

    subGraphs = []

    for n in range(1, len(graph.edges)):
        for SG in (graph.edge_subgraph(i) for i in itertools.combinations(graph.edges, n)):
            if nx.is_connected(SG) and (s in SG.nodes):
                subGraphs.append(SG)
                #print(SG, SG.nodes, SG.edges)
    return subGraphs

    #print(ans)

# TODO: Redundunt
def getPointNumber(network, T, s):
    N1, N2 = 0, 0

    for H in getSubGraphs(network.graph, s):
        bridges = [norm_edge(e) for e in nx.bridges(H)]
        #print(bridges, "!!!!")
        paths = getAllPaths(H, s)

        for v in H.nodes():
            pGv1, pGv2 = len(list(network.graph.neighbors(v))), len(list(H.neighbors(v)))
            path_count = 0

            for path in paths[v]:
                keys = dict()
                j = 0
                for e in path:
                    keys[j] = e
                    j += 1
                division = [0]*j

                currently_moving = len(division)-1
                while currently_moving>=0:
                    sum = 0
                    for i in range(len(division)):
                        sum += (2*division[i] + (2 - path[keys[i]] % 2)) * network.get_weight(keys[i])
                    #print(division, sum, path_count)
                    if sum<=T:
                        path_count+=1
                        division[currently_moving]+=1
                        for i in range(currently_moving+1, len(division)):
                            division[i] = 0
                        currently_moving = len(division)-1
                    else:
                        currently_moving -= 1
                        if currently_moving>0 and division[currently_moving+1]!=0:
                            division[currently_moving] += 1
                            for i in range(currently_moving + 1, len(division)):
                                division[i] = 0
                            currently_moving = len(division) - 1

            N1 += (pGv1-pGv2) * path_count
            path_count = 0

            for e in H.edges(v):
                if norm_edge(e) in bridges:
                    temp = nx.shortest_path(network.graph, s, v)
                    #print(temp, v, s)
                    if len(temp)>=2:
                        edge = norm_edge([temp[-1], temp[-2]])
                        if edge == norm_edge(e) and len(list(H.neighbors(edge[0]))) != 1 and len(list(H.neighbors(edge[1]))) != 0:

                            edge_weigth = network.get_weight(edge)
                            #print("YEEEESS!!!!")

                            for path in paths[v]:
                                keys = dict()
                                j = 0
                                for e1 in path:
                                    keys[j] = e1
                                    j += 1
                                division = [0] * j

                                currently_moving = len(division) - 1
                                while currently_moving >= 0:
                                    if norm_edge(keys[currently_moving]) == norm_edge(edge):
                                        currently_moving -= 1
                                        continue
                                    sum = 0
                                    for i in range(len(division)):
                                        if norm_edge(keys[i]) != norm_edge(e):
                                            sum += (2 * division[i] + (2 - path[keys[i]] % 2)) * network.get_weight(keys[i])
                                    if sum <= T - edge_weigth:
                                        path_count += 1
                                        division[currently_moving] += 1
                                        for i in range(currently_moving + 1, len(division)):
                                            division[i] = 0
                                        currently_moving = len(division) - 1
                                    else:
                                        currently_moving -= 1
                                        if currently_moving > 0 and division[currently_moving + 1] != 0 \
                                                and norm_edge(keys[currently_moving]) != norm_edge(edge):
                                            division[currently_moving] += 1
                                            for i in range(currently_moving + 1, len(division)):
                                                division[i] = 0
                                            currently_moving = len(division) - 1
            N2 += path_count

            #print(N1, N2, (pGv1-pGv2))
    return N1+N2


def getPointNumber_Todd(network, t_sub, s):
    N1, N2 = 0, 0
    T = sympy.Symbol("T")
    if len(t_sub)==0:
        t_sub = "T"

    a = getSubGraphs(network.graph, s)

    for H in getSubGraphs(network.graph, s):
        bridges = [norm_edge(e) for e in nx.bridges(H)]
        #print(bridges, "!!!!")
        paths = getAllPaths(H, s)

        for v in H.nodes():
            pGv1, pGv2 = len(list(network.graph.neighbors(v))), len(list(H.neighbors(v)))
            path_count = 0

            for path in paths[v]:
                keys = dict()
                j = 0
                for e in path:
                    keys[j] = e
                    j += 1
                ti = [0]*j
                sum = 0
                for i in range(len(ti)):
                    sum += (2-(path[keys[i]] % 2)) * network.get_weight(keys[i])
                    #sum += (path[keys[i]] % 2) * network.get_weight(keys[i])
                    ti[i] = 2 * network.get_weight(keys[i])

                #path_count += Random.todd.build_rk(len(H.edges), T + sum, ti)
                path_count += Random.todd.build_rk(len(H.edges), T - sum, ti)

            N1 += (pGv1-pGv2) * path_count
            path_count = 0

            if pGv2>1:
                for e in H.edges(v):
                    if norm_edge(e) in bridges:
                        temp = nx.shortest_path(network.graph, s, v)
                        #print(temp, v, s)
                        if len(temp)>=2:
                            edge = norm_edge([temp[-1], temp[-2]])
                            if edge == norm_edge(e) and len(list(H.neighbors(edge[0]))) != 1 and len(list(H.neighbors(edge[1]))) != 0:

                                edge_weigth = network.get_weight(edge)
                                #print("YEEEESS!!!!")

                                for path in paths[v]:
                                    keys = dict()
                                    j = 0
                                    for e in path:
                                        keys[j] = e
                                        j += 1
                                    ti = [0] * (j - 1)
                                    sum = 0
                                    j = 0
                                    for i in range(len(ti)):
                                        if norm_edge(keys[i]) != norm_edge(e):
                                            sum += (2-(path[keys[i]] % 2)) * network.get_weight(keys[i])
                                            ti[j] = 2 * network.get_weight(keys[i])
                                            j += 1
                                    path_count += Random.todd.build_rk(len(H.edges) - 1, T - sum - edge_weigth, ti)

            N2 += path_count

            #print(N1, N2, (pGv1-pGv2))
    #print(N1+N2)
    #print(Poly(N1+N2))
    #return sympy.expand(N1).subs(T, t_sub)
    #return sympy.simplify(Poly(N1+N2).subs(T, t_sub))
    N1 += len(list(network.graph.neighbors(s)))
    print(N1,N2, sep='\n')
    print(sympy.simplify(sympy.Poly(N1, T)).as_expr())
    print(sympy.simplify(sympy.Poly(N2, T)).as_expr())
    return sympy.simplify(sympy.Poly(N1, T) + sympy.Poly(N2, T)).as_expr()

def getAllPaths(SG, s):
    paths = dict()
    for n in SG.nodes:
        paths[n] = []
    visited = dict()
    for e in SG.edges:
        visited[norm_edge(e)] = 0
    __recursionPaths(SG, s, visited, paths)

    for e in paths:
        for v in paths[e]:
            for c in v:
                v[c] = 2 - v[c] % 2
        #        print(e, c, v)
        paths[e] = list({str(i):i for i in paths[e]}.values())
        #paths[e] = set(list(paths[e]))
        #print(paths[e])

    return paths


def __recursionPaths(SG, point, visited, paths):
    for e in SG.edges(point):
        edge = norm_edge(e)
        if visited[edge]<2:
            visited_copy = visited.copy()
            visited_copy[edge] += 1
            paths[getOtherPoint(edge, point)].append(visited_copy)
            __recursionPaths(SG, getOtherPoint(edge, point), visited_copy, paths)
