import sys
import matplotlib.pyplot as plt
import numpy as np

def parse_csv_curves(filename, max_curves=5):
    curves = []
    with open(filename, 'r') as f:
        lines = f.readlines()[1:]  # Skip header
        if max_curves > len(lines):
            raise ValueError(f"Requested {max_curves} curves but only {len(lines)} available in {filename}")
        for line in lines[:max_curves]:
            line = line.strip()
            if not line:
                continue
            points = []
            for pair in line.split('|'):
                x, y = map(float, pair.strip().split())
                points.append((x, y))
            curves.append(points)
    return curves

def extract_curve_by_index(filename, curve_index):
    with open(filename, 'r') as f:
        lines = f.readlines()[1:]  # Skip header line

        if curve_index < 0 or curve_index >= len(lines):
            raise IndexError("Curve index out of range.")

        line = lines[curve_index].strip()
        if not line:
            raise ValueError("Selected curve line is empty.")

        curve = [
            tuple(map(float, pair.strip().split()))
            for pair in line.split('|')
        ]
        return curve

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python visualize_curves.py <curve_file> <num_curves> <query_file> <query_index>")
        sys.exit(1)

    curve_file = sys.argv[1]
    num_curves = int(sys.argv[2])
    query_file = sys.argv[3]
    query_index = int(sys.argv[4])

    print(f"From file '{curve_file}' you chose {num_curves} curves.")
    print(f"From query file '{query_file}' you chose curve {query_index}.")

    # Load dataset and query curve
    curves = parse_csv_curves(curve_file, max_curves=num_curves)
    k = extract_curve_by_index(query_file, query_index)

    # Plotting
    plt.figure(figsize=(10, 8))
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'magenta', 'grey', 'black']

    for i, curve in enumerate(curves):
        xs, ys = zip(*curve)
        plt.plot(ys, xs, marker='o', label="", color=colors[i % len(colors)], alpha=0.25)

    k_xs, k_ys = zip(*k)
    plt.plot(k_ys, k_xs, marker='x', linestyle='--', color='black', linewidth=3, label='Query Curve k')

    plt.title(f"First {num_curves} curves + Query curve")
    plt.xlim(104, 143)  # Longitude
    plt.ylim(22, 43)    # Latitude
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.legend()
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

    # Run Example: python visualize_dataset.py geolife_trajectories_under_5km.csv 100 query_dataset.csv 1
