import numpy as np
from curve_extraction import extract_curve
import time
from modern_quadtree import Quadtree
import sys

# FIND LOWER BOUND OF FRECHET DISTANCE BASED ON MIN MAX COORDIANTES ON X AND Y AND STARTING AND ENDNG POINTS

def find_lower_bound(P, Q):
    P = np.array(P)
    Q = np.array(Q)

    # Start and end point distances
    d_start = np.linalg.norm(P[0] - Q[0])
    d_end = np.linalg.norm(P[-1] - Q[-1])

    # Min/max differences in x and y. Numpy makes things simple here.
    min_x_diff = abs(np.min(P[:, 0]) - np.min(Q[:, 0]))
    max_x_diff = abs(np.max(P[:, 0]) - np.max(Q[:, 0]))
    min_y_diff = abs(np.min(P[:, 1]) - np.min(Q[:, 1]))
    max_y_diff = abs(np.max(P[:, 1]) - np.max(Q[:, 1]))

    # Return the max values of all the possible boundaries
    return max(d_start, d_end, min_x_diff, max_x_diff, min_y_diff, max_y_diff)

def compute_8d_features(curve):
    curve = np.array(curve)
    return np.array([
        curve[0][0],       # start x
        curve[0][1],       # start y
        curve[-1][0],      # end x
        curve[-1][1],      # end y
        np.min(curve[:, 0]),  # min x
        np.max(curve[:, 0]),  # max x
        np.min(curve[:, 1]),  # min y
        np.max(curve[:, 1])   # max y
    ])


################################################################################################################################################################
# FIND CANDIDATES WITH LOWER BOUND FOR FRECHET DISTANCE LOWER THAN EPSILON USING A QUATREE

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python modern_lower_bound.py <curve_file> <num_curves> <query_file> <query_index> <delta>")
        sys.exit(1)

    curve_file = sys.argv[1]
    num_curves = int(sys.argv[2])
    query_file = sys.argv[3]
    query_index = int(sys.argv[4])
    delta = float(sys.argv[5])

    print("")
    print(f"From file {curve_file} you chose {num_curves} curves.")
    print(f"From query file you chose curve {query_index}.")
    print(f"Using delta value: {delta}")
    print("")

    with open(curve_file, 'r') as f:
        total_lines = len(f.readlines()) - 1  # Header that says x y or anything is excluded

    if num_curves > total_lines:
        print(f"Error: You requested {num_curves} curves, but the file only contains {total_lines} curves.")
        sys.exit(1)

    dataset = []
    for idx in range(num_curves):
    
        curve = extract_curve(curve_file, idx)
        features = compute_8d_features(curve)
        dataset.append((features, idx))

    start = time.perf_counter()
    tree = Quadtree(dataset, max_elements=4)
    end = time.perf_counter()
    create_tree_time = end - start
    print(f"Total time to create quad tree: {create_tree_time:.7f} seconds")

    k = extract_curve(query_file, query_index)
    k_features = compute_8d_features(k)

    delta = delta * 2  # Treated like diameter

    start = time.perf_counter()
    candidates = tree.query(k_features, delta)
    end = time.perf_counter()
    find_candidates_time = end - start
    print(f"Total time to find candidates: {find_candidates_time:.7f} seconds")

    print("Total number of candidates:", len(candidates))
    print("Candidates:", candidates)

# Run Example:  python modern_lower_bound.py generated_curves_10_30.csv 100 query_dataset.csv 0 0.01