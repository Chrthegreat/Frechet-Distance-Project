import numpy as np
from classic_Frechet_decision import interval_within_epsilon

# RECURSIVE ALGORITHM. FIND FREE SPACE


def dist(p, q):
    return np.linalg.norm(np.array(p) - np.array(q))

def dist_sqr(p, q):
    return np.sum((np.array(p) - np.array(q)) ** 2)

def sqr(x):
    return x * x

def is_empty_interval(interval):
    return interval[0] > interval[1]

def merge_intervals(intervals, new_interval, eps=1e-9):
    if is_empty_interval(new_interval):
        return
    if intervals and new_interval[0] - eps <= intervals[-1][1]:
        intervals[-1][1] = max(intervals[-1][1], new_interval[1])
    else:
        intervals.append(list(new_interval))

def intersection_interval(p, d, q0, q1):
    result = interval_within_epsilon((q0, q1), p, d)
    if result is None:
        return (1, 0)  
    return result

def get_reachable_horizontal_border(i, j, a, b, d):
    if j + 1 >= len(b): # Care not to overflow
        return [1, 0]  
    #if i >= len(a):
    #    i = len(a) - 1  # clamp i to last valid index
    start, end = intersection_interval(a[i], d, b[j], b[j + 1])
    return [start + j, end + j]

def get_reachable_vertical_border(i, j, a, b, d):
    if j + 1 >= len(a):
        return [1, 0]  
    if i >= len(b):
        return [15,15]
    start, end = intersection_interval(b[i], d, a[j], a[j + 1])
    return [start + j, end + j]


def overlap(intervals, i0, i1):
        for i in intervals:
            if i[0] <= i1 and i[1] >= i0:
                return i
        return None

def curve_length(c, i, j):
    #Compute the sum of Euclidean distances between c[i] to c[j] (exclusive).
    c = np.array(c)
    return np.sum(np.linalg.norm(c[i+1:j+1] - c[i:j], axis=1))

def get_reachable_intervals(i_min, i_max, j_min, j_max, P, Q, d, rQ, rP, rQ_out, rP_out):
    
    tQ = overlap(rQ, j_min, j_max)
    tP = overlap(rP, i_min, i_max)

    if tQ is None and tP is None:
        return

    if tQ and tP:
        i_mid = (i_min + 1 + i_max) // 2
        j_mid = (j_min + 1 + j_max) // 2
        d_est = dist(P[i_mid], Q[j_mid]) + max(
            curve_length(P, i_min + 1, i_mid),
            curve_length(P, i_mid, i_max)
        ) + max(
            curve_length(Q, j_min + 1, j_mid),
          curve_length(Q, j_mid, j_max)
        )
        if d_est <= d:
            merge_intervals(rQ_out, [j_min, j_max])
            merge_intervals(rP_out, [i_min, i_max])
            return

    #print(f"Recurse: i=({i_min},{i_max}), j=({j_min},{j_max})")
    if i_max <= i_min or j_max <= j_min:
        return  # clamp: can't split further
    if i_max == i_min + 1 and j_max == j_min + 1:

        aa = get_reachable_horizontal_border(i_max, j_min, P, Q, d)
        bb = get_reachable_vertical_border(i_min, j_max, P, Q, d)

        if tP is None and tQ:
            aa[0] = max(aa[0], tQ[0])
        elif tQ is None and tP:
            bb[0] = max(bb[0], tP[0])

        merge_intervals(rQ_out, aa)
        merge_intervals(rP_out, bb)
        return

    if (j_max - j_min) > (i_max - i_min):
        j_split = (j_min + j_max) // 2
        ra_middle = []
        get_reachable_intervals(i_min, i_max, j_min, j_split, P, Q, d, rQ, rP, rQ_out, ra_middle)
        get_reachable_intervals(i_min, i_max, j_split, j_max, P, Q, d, rQ, ra_middle, rQ_out, rP_out)
    else:
        i_split = (i_min + i_max) // 2
        rb_middle = []
        get_reachable_intervals(i_min, i_split, j_min, j_max, P, Q, d, rQ, rP, rb_middle, rP_out)
        get_reachable_intervals(i_split, i_max, j_min, j_max, P, Q, d, rb_middle, rP, rQ_out, rP_out)