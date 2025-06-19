import numpy as np
from curve_extraction import extract_curve
import time
import sys

################################################################################################################################################################

# NEGATIVE FILTER. FIND CURVES WITH TOO LARGE FRECHE DISTANCE AND EXCLUDE THEM


def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def curve_length(c, i, j):
    #Compute the sum of Euclidean distances between c[i] to c[j] (exclusive).
    c = np.array(c)
    return np.sum(np.linalg.norm(c[i+1:j+1] - c[i:j], axis=1))

def next_close_point(c, i, p, d):
    #Greedily find the first point on curve c (starting at i) within distance d of p.
    c = np.array(c)
    delta_step = 1
    k = i

    while True:
        # Check if we are at the end
        if k == len(c) - 1:
            return k if euclidean(c[k], p) <= d else len(c)
        else:
            # Make sure we dont go over the end when jumping delta
            delta_step = min(delta_step, len(c) - 1 - k)
            # Find shortest distance thap p could be from any point in k , k+step
            if euclidean(p, c[k]) - curve_length(c, k, k + delta_step) > d:
                # Modify k with varying step
                k += delta_step
                delta_step *= 2
            elif delta_step > 1:
                delta_step //= 2
            else:
                return k

def neg_filter(c1, c2, d):
    #Negative filter: returns True if curves can be rejected.
    c1 = np.array(c1)
    c2 = np.array(c2)

    delta_step = max(len(c1), len(c2)) - 1
    while delta_step >= 1:
        i = 0
        for j in range(0, len(c2), delta_step):
            i = next_close_point(c1, i, c2[j], d)
            if i >= len(c1):
                return True  # Rejected

        j = 0
        for i_ in range(0, len(c1), delta_step):
            j = next_close_point(c2, j, c1[i_], d)
            if j >= len(c2):
                return True  # Rejected

        delta_step //= 2

    return False  # Not rejected

############################################################################################################################
# THESE LINES BELOW WILL CHECK NEGATIVE FILTER

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python negative_filter.py <curve_file> <num_curves> <query_file> <query_index> <delta>")
        sys.exit(1)

    curve_file = sys.argv[1]
    num_curves = int(sys.argv[2])
    query_file = sys.argv[3]
    query_index = int(sys.argv[4])
    delta = float(sys.argv[5])

    with open(curve_file, 'r') as f:
        total_lines = len(f.readlines()) - 1

    if num_curves > total_lines:
        print(f"Error: You requested {num_curves} curves, but the file only contains {total_lines} curves.")
        sys.exit(1)

    print("")
    print(f"From file {curve_file} you chose {num_curves} curves.")
    print(f"From query file you chose curve {query_index}.")
    print(f"Using delta value: {delta}")
    print("")

    k = extract_curve(query_file, query_index)

    reject = 0
    accept = 0
    idxs = []  # Rejected
    accepted_idxs = []  # Accepted
    neg_total = 0.0

    for i in range(num_curves):
        
        candidate_curve = extract_curve(curve_file, i)

        start = time.perf_counter()
        boolean = neg_filter(k, candidate_curve, delta)
        end = time.perf_counter()
        neg_total += (end - start)

        if boolean:
            idxs.append(i)
            reject += 1
        else:
            accept += 1
            accepted_idxs.append(i)

    print("Curves rejected by negative filter (too far from query):", idxs)
    print(f"Total time to run negative filter: {neg_total:.7f} seconds")
    print("Number of curves too far apart from query:", reject)
    print("Number of curves close to query:", accept)

# Run Example:  python modern_negative_filter.py generated_curves_10_30.csv 100 query_dataset.csv 0 0.01