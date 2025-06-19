from curve_extraction import extract_curve
from modern_quadtree import Quadtree
from modern_lower_bound import compute_8d_features
from modern_positive_filter import greedy_frechet_upper_bound
from modern_negative_filter import neg_filter
from modern_Frechet_distance import frechet_distance_recursive
from classic_Frechet_distance import frechet_distance
import sys
import time



# RUN ALL FILTRES AND RECURSIVE VS CLASSIC APPROACH. CHANGE DATABASE PATH, RANGE INDEX, QUERY CURVE AND DELTA


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python full_pipeline.py <curve_file> <num_curves> <query_file> <query_index> <delta>")
        sys.exit(1)

    curve_file = sys.argv[1]
    num_curves = int(sys.argv[2])
    query_file = sys.argv[3]
    query_index = int(sys.argv[4])
    delta = float(sys.argv[5])

    # Check file length
    with open(curve_file, 'r') as f:
        total_lines = len(f.readlines()) - 1
    if num_curves > total_lines:
        print(f"Error: You requested {num_curves} curves, but file contains only {total_lines}.")
        sys.exit(1)

    print("")
    print(f"From file {curve_file} you chose {num_curves} curves.")
    print(f"From query file you chose curve {query_index}.")
    print(f"Using delta value: {delta}")
    print("")

    # 0. Build Quadtree
    dataset = []
    for idx in range(num_curves):
        curve = extract_curve(curve_file, idx)
        features = compute_8d_features(curve)
        dataset.append((features, idx))

    start = time.perf_counter()
    tree = Quadtree(dataset, max_elements=4)
    end = time.perf_counter()
    print(f"Total time to create quad tree: {end - start:.7f} seconds")

    k = extract_curve(query_file, query_index)
    k_features = compute_8d_features(k)

    start = time.perf_counter()
    candidates = tree.query(k_features, delta * 2)  # delta treated as radius, so use 2*delta
    end = time.perf_counter()
    print(f"Total time to find candidates: {end - start:.7f} seconds")
    print("Total number of candidates:", len(candidates))
    print("Candidate indexes:", candidates)

    # 1. Positive Filter
    pos_total = 0
    exact_distance_needed = []
    curves_below_delta = []

    candidate_curves = [extract_curve(curve_file, idx) for idx in candidates]
    for i, idx in enumerate(candidates):
        curve = candidate_curves[i]
        start = time.perf_counter()
        upper_bound = greedy_frechet_upper_bound(k, curve)
        end = time.perf_counter()
        pos_total += (end - start)

        if upper_bound <= delta:
            curves_below_delta.append(idx)
        else:
            exact_distance_needed.append(idx)

    print(f"Total time for positive filter: {pos_total:.7f} seconds")

    # 2. Negative Filter
    neg_total = 0
    accepted_idxs = []
    rejected_idxs = []
    for idx in exact_distance_needed:
        candidate_curve = extract_curve(curve_file, idx)
        start = time.perf_counter()
        boolean = neg_filter(k, candidate_curve, delta)
        end = time.perf_counter()
        neg_total += (end - start)

        if boolean:
            rejected_idxs.append(idx)
        else:
            accepted_idxs.append(idx)

    print(f"Total time for negative filter: {neg_total:.7f} seconds")

    # 3. Recursive Check
    recursive_total = 0
    for i in accepted_idxs:
        print(f"Working on curve {i}.", flush=True)
        P = extract_curve(curve_file, i)
        start = time.process_time()
        distance = frechet_distance_recursive(k, P)
        end = time.process_time()
        recursive_total += (end - start)
        if distance <= delta:
            curves_below_delta.append(i)

    print(f"Total time for recursive algorithm: {recursive_total:.7f} seconds")
    print("Curves below delta:", curves_below_delta)

    print("-" * 60)

    # 4. Classic Algorithm
    classic_total = 0
    curves_below_delta_classic = []
    print(f"Now running classic algorithm.", flush=True)
    for i in range(num_curves):
        print(f"Working on curve {i}.", flush=True)
        P = extract_curve(curve_file, i)
        start = time.process_time()
        frechet = frechet_distance(k, P)  
        end = time.process_time()
        classic_total += (end - start)
        if frechet <= delta:
            curves_below_delta_classic.append(i)

    print(f"Total time for classic algorithm: {classic_total:.7f} seconds")
    print("Curves below delta (classic):", curves_below_delta_classic)

    recursive_set = set(curves_below_delta)
    classic_set = set(curves_below_delta_classic)

    if recursive_set == classic_set:
        print("Both algorithms returned the same curves.")
    else:
        only_in_recursive = sorted(list(recursive_set - classic_set))
        only_in_classic = sorted(list(classic_set - recursive_set))

        if only_in_recursive:
            print("Curves returned by the recursive method but not by classic:")
            print(only_in_recursive)
        if only_in_classic:
            print("Curves returned by the classic method but not by recursive:")
            print(only_in_classic)


# LETS SAVE OUR RESULTS SO WE VISUALIZE THEM LATER

    def save_results_to_file(filename, params, curves_below_delta, curves_below_delta_classic):
        with open(filename, 'w') as f:
            f.write("# PARAMETERS\n")
            for key, value in params.items():
                f.write(f"{key}: {value}\n")

            f.write("\n# RESULTS\n")
            f.write(f"curves_below_delta: {curves_below_delta}\n")
            f.write(f"curves_below_delta_classic: {curves_below_delta_classic}\n")


    params = {
        "curve_file": curve_file,
        "num_curves": num_curves,
        "query_file": query_file,
        "query_index": query_index,
        "delta": delta
    }
    save_results_to_file("results.txt", params, curves_below_delta, curves_below_delta_classic)

# Run Example:  python modern_vs_classic.py generated_curves_10_30.csv 100 query_dataset.csv 0 0.01
