from curve_extraction import extract_curve
from classic_Frechet_criticalPoints import compute_critical_epsilons
from classic_Frechet_decision import decision
import sys
import time

# CALCULATE CLASSIC FRECHET DISTANCE USING BINARY SEARCH

def frechet_distance(P, Q):
    critical_epsilons = compute_critical_epsilons(P, Q) # The critical epsilons
    left = 0   # Start with the middle element of the array
    right = len(critical_epsilons) - 1
    result = critical_epsilons[-1]

    while left <= right:
        mid = (left + right) // 2   
        eps = critical_epsilons[mid]
        if decision(P, Q, eps):  # Call the decision function
            result = eps         # Keep the lowest element that ansers YES
            right = mid - 1
        else:
            left = mid + 1
            
    return result

################################################################################################################################################################

# RUN CLASSIC ALGORITHM


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python classic_Frechet_distance.py <curve_file> <num_curves> <query_file> <query_index>")
        sys.exit(1)

    curve_file = sys.argv[1]
    num_curves = int(sys.argv[2])
    query_file = sys.argv[3]
    query_index = int(sys.argv[4])

    

    print("")
    print(f"From file {curve_file} you chose {num_curves} curves.")
    print(f"From query file you chose curve {query_index}.")
    print("")

    with open(curve_file, 'r') as f:
        total_lines = len(f.readlines()) - 1  # Header that says x y or anything is excluded

    if num_curves > total_lines:
        print(f"Error: You requested {num_curves} curves, but the file only contains {total_lines} curves.")
        sys.exit(1)

    query_curve = extract_curve(query_file, query_index)

    classic_total = 0.0

    for i in range(num_curves):
        print(f"Working on curve {i+1}.", flush=True)
        current_curve = extract_curve(curve_file, i)
        # print("Current curve (P) =", current_curve)

        critical_eps = compute_critical_epsilons(query_curve, current_curve)
        # print("Critical epsilon values:")
        # for eps in critical_eps:
        #     print(f"{eps:.6f}")
        
        start = time.process_time()
        frechet = frechet_distance(query_curve, current_curve)
        end = time.process_time()

        classic_total += (end - start)

        print(f"Frechet distance between query and curve {i+1}: {frechet:.8f}")
        print("-" * 40)
    
    print("-" * 60)
    print(f"Total time for recursive: {classic_total:.7f} seconds")
    avg_time = classic_total / num_curves if num_curves else 0
    print(f"Average time for recursive: {avg_time:.7f} seconds")


# Run Example:  python classic_Frechet_distance.py generated_curves_10_30.csv 100 query_dataset.csv 0