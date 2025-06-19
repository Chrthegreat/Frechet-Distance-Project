import numpy as np
from classic_Frechet_criticalPoints import compute_critical_epsilons
from modern_get_intervals import * 
from curve_extraction import extract_curve
import sys
import time


def get_last_reachable_point_from_start(P, Q, d):
    j = 0  # Start from the 1st point of Q
    # With P[0] fixed, swipe through all points of Q
    # and find the last one that is within d distance
    while j < len(Q) - 2 and dist(P[0], Q[j + 1]) <= d:
        j += 1
    # Find the free space on the border of the cell that 
    # corresponds to P[0] and the Q[j]. 
    return get_reachable_horizontal_border(0, j, P, Q, d)[1]

def get_dist_to_point_sqr(curve, pt):
    return max(dist_sqr(p, pt) for p in curve)

def is_frechet_distance_at_most(P, Q, d):
    # Check the distance between starting and ending points
    if dist(P[0], Q[0]) > d or dist(P[-1], Q[-1]) > d:
        return False
    # Check if either curve comprises of only one point
    if len(P) == 1 and len(Q) == 1:
        return True
    elif len(P) == 1:
        return get_dist_to_point_sqr(Q, P[0]) <= sqr(d)
    elif len(Q) == 1:
        return get_dist_to_point_sqr(P, Q[0]) <= sqr(d)

    rP = [[0, get_last_reachable_point_from_start(P, Q, d)]]
    rQ = [[0, get_last_reachable_point_from_start(Q, P, d)]]
    rP_out, rQ_out = [], []

    get_reachable_intervals(0, len(P) - 1, 0, len(Q) - 1, P, Q, d, rQ, rP, rQ_out, rP_out)

    return rP_out and rP_out[-1][1] >= len(P) - 1.5


def frechet_distance_recursive(P, Q):
    critical_epsilons = compute_critical_epsilons(P, Q)
    left = 0
    right = len(critical_epsilons) - 1
    result = critical_epsilons[-1]

    while left <= right:
        mid = (left + right) // 2
        eps = critical_epsilons[mid]
        if is_frechet_distance_at_most(P, Q, eps):
            result = eps
            right = mid - 1
        else:
            left = mid + 1

    return result

#############################################################################################################
# THESE LINES BELOW WILL CHECK RECURSIVE ALGORITHM

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python recursive_check.py <curve_file> <num_curves> <query_file> <query_index>")
        sys.exit(1)

    curve_file = sys.argv[1]
    num_curves = int(sys.argv[2])
    query_file = sys.argv[3]
    query_index = int(sys.argv[4])

    with open(curve_file, 'r') as f:
        total_lines = len(f.readlines()) - 1

    if num_curves > total_lines:
        print(f"Error: You requested {num_curves} curves, but the file only contains {total_lines} curves.")
        sys.exit(1)

    print("")
    print(f"From file {curve_file} you chose {num_curves} curves.")
    print(f"From query file you chose curve {query_index}.")
    print("")

    k = extract_curve(query_file, query_index)

    recursive_total = 0.0

    for i in range(num_curves):
        print(f"Working on curve {i+1}.", flush=True)
        P = extract_curve(curve_file, i)

        start = time.process_time()
        distance = frechet_distance_recursive(k, P)
        end = time.process_time()

        print(f"Frechet distance between query and curve {i+1}: {distance:.8f}")
        print("-" * 40)

        recursive_total += (end - start)

    print("-" * 60)
    print(f"Total time for recursive: {recursive_total:.7f} seconds")
    avg_time = recursive_total / num_curves if num_curves else 0
    print(f"Average time for recursive: {avg_time:.7f} seconds")

# Run Example:  python modern_Frechet_distance.py generated_curves_10_30.csv 100 query_dataset.csv 0 