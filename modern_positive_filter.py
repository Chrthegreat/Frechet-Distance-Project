import numpy as np
from curve_extraction import extract_curve
import time

# UPPER BOUND FILTER (POSITIVE FILTER). IF UPPER BOUND LOWER THAN TARGET WE ACCEPT CURVE WITHOUT EXACT CALCULATION

def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def greedy_frechet_upper_bound(P, Q):
    pos_a = 0
    pos_b = 0
    distance = euclidean(P[-1], Q[-1])  # Start from end-point distance

    # Loop until we reach the end points
    while pos_a + pos_b < len(P) + len(Q) - 2:
        distance = max(distance, euclidean(P[pos_a], Q[pos_b]))

        # If pos_a reach the end, only increase pos_b and via versa
        if pos_a == len(P) - 1: 
            pos_b += 1
        elif pos_b == len(Q) - 1:
            pos_a += 1

        # If we are not at the end, find minimal distance
        else:
            # Compute possible future distances (squared for efficiency)
            dist_a = np.sum((np.array(P[pos_a + 1]) - np.array(Q[pos_b])) ** 2)
            dist_b = np.sum((np.array(P[pos_a]) - np.array(Q[pos_b + 1])) ** 2)
            dist_both = np.sum((np.array(P[pos_a + 1]) - np.array(Q[pos_b + 1])) ** 2)

            # Take the step that minimizes the distance
            if dist_a < dist_b and dist_a < dist_both:
                pos_a += 1
            elif dist_b < dist_both:
                pos_b += 1
            else:
                pos_a += 1
                pos_b += 1

    return distance

############################################################################################################################
# THESE LINES WILL CHECK THE POSITIVE FILTER 

import sys

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python positive_filter.py <curve_file> <num_curves> <query_file> <query_index> <delta>")
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

    pos_total = 0.0
    exact_distance_needed = []

    for i in range(num_curves):
       
        curve = extract_curve(curve_file, i)

        start = time.perf_counter()
        upper_bound = greedy_frechet_upper_bound(k, curve)
        end = time.perf_counter()
        pos_total += (end - start)

        if upper_bound > delta:
            exact_distance_needed.append(i)

    print("After greedy check, curves remaining:")
    print("Curves left to find exact distance:", exact_distance_needed)
    print("Total number left after greedy:", len(exact_distance_needed))
    print(f"Total time to run positive filter: {pos_total:.7f} seconds")

# Run Example:  python modern_positive_filter.py generated_curves_10_30.csv 100 query_dataset.csv 0 0.01