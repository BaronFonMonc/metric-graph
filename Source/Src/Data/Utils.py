import sympy
from sympy import latex


# Calculate the position of points based on dir
# Coordinates pos1 = edge[0]; pos2 = edge[1]
def calc_pos_dir(pos1, pos2, length, dist, dir, edge):
    if edge[1] == dir:
        return calc_pos(pos1, pos2, length, dist)
    else:
        return calc_pos(pos2, pos1, length, dist)


# Calculate the position of points
# on edge (pos1, pos2)
# that is located on distance dist from pos1.
def calc_pos(pos1, pos2, length, dist):
    if dist>length:
        print("Distance should not be bigger than length of edge")
        pass
    x1, y1 = pos1[0], pos1[1]
    x2, y2 = pos2[0], pos2[1]
    ratio = dist/length

    x, y = x1 + (x2 - x1) * ratio, y1 + (y2 - y1) * ratio
    return x, y


# https://learncodingfast.com/merge-intervals/
# Concatenate intervals
# for example [[1,2], [1,3], [3,5], [6,8]] -> [[1,5], [6,8]]
# and         [[1,2], [2,8], [2,3]] -> [[1,8]]
def concat_intervals(intervals):
    if len(intervals) == 0 or len(intervals) == 1:
        return intervals
    intervals.sort(key=lambda x:x[0])
    result = [intervals[0]]
    for interval in intervals[1:]:
        if interval[0] <= result[-1][1]:
            result[-1][1] = max(result[-1][1], interval[1])
        else:
            result.append(interval)
    return result


# Get intersection of list of intervals
# for example [[[1,8], [9,10]], [[1,5]]] -> [[1,5]]
def get_intersections(intervals):
    ans = intervalIntersection(intervals[0], intervals[1])
    for i in range(1, len(intervals)):
        ans = intervalIntersection(ans, intervals[i])

    return ans


# Get intersection of two intervals
# [[1,2], [3,5]] and [[3,4]] -> [[3,4]]
def intervalIntersection(A, B):
    if A==[] or B==[] or A==[[]] or B==[[]]:
        return []
    ans = []
    i = j = 0

    while i < len(A) and j < len(B):
        # Let's check if A[i] intersects B[j].
        # lo - the startpoint of the intersection
        # hi - the endpoint of the intersection
        lo = max(A[i][0], B[j][0])
        hi = min(A[i][1], B[j][1])
        if lo <= hi:
            ans.append([lo, hi])

        # Remove the interval with the smallest endpoint
        if A[i][1] < B[j][1]:
            i += 1
        else:
            j += 1

    return ans


def norm_edge(edge):
    return (min(edge[0], edge[1]), max(edge[0], edge[1]))


def getOtherPoint(edge, node):
    if edge[0] == node:
        return edge[1]
    else:
        return edge[0]


# If string is started with $ and ended with $: return unchanged string.
# If string is sympy format return sympy(s) transformed to raw latex.
def parseStrToLatex(s: str) -> str:
    if len(s)>2:
        if s[0]=='$' and s[-1]=='$':
            return s
    try:
        s = sympy.parse_expr(s)
    except:
        return False
    return "$" + str(latex(s)) + "$"
