import matplotlib.pyplot as plt
import numpy as np

################################################################################################################################################################

# READ CURVES FROM DATABASE

def parse_csv_curves(filename, max_curves=5):
    curves = []
    with open(filename, 'r') as f:
        lines = f.readlines()[1:]  # Skip header
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

################################################################################################################################################################

# THE LINES BELOW WILL PLOT THE RESULTS FOR THE CLASSIC AND THE MODERN ALGORITHM

def parse_results_file(path):
    results = {
        "params": {},
        "classic_candidates": [],
        "modern_candidates": []
    }

    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("curve_file:"):
                results["params"]["curve_file"] = line.split(":", 1)[1].strip()
            elif line.startswith("query_file:"):
                results["params"]["query_file"] = line.split(":", 1)[1].strip()
            elif line.startswith("num_curves:"):
                results["params"]["num_curves"] = int(line.split(":", 1)[1].strip())
            elif line.startswith("query_index:"):
                results["params"]["query_index"] = int(line.split(":", 1)[1].strip())
            elif line.startswith("delta:"):
                results["params"]["delta"] = float(line.split(":", 1)[1].strip())
            elif line.startswith("curves_below_delta:"):
                results["modern_candidates"] = eval(line.split(":", 1)[1].strip())
            elif line.startswith("curves_below_delta_classic:"):
                results["classic_candidates"] = eval(line.split(":", 1)[1].strip())
    return results

# Load from results.txt
results = parse_results_file("results.txt")

# Load curves and query
curves = parse_csv_curves(results["params"]["curve_file"], max_curves=results["params"]["num_curves"])
query_curve = extract_curve_by_index(results["params"]["query_file"], results["params"]["query_index"])
delta = results["params"]["delta"]

# Plotting
fig, axes = plt.subplots(1, 2, figsize=(18, 8))

methods = {
    "Classic Method": results["classic_candidates"],
    "Modern Method": results["modern_candidates"]
}

for ax, (title, candidates) in zip(axes, methods.items()):
    candidates_set = set(candidates)

    rejected_label_plotted = False
    accepted_label_plotted = False

    for idx, curve in enumerate(curves):
        xs, ys = zip(*curve)
        if idx in candidates_set:
            label = "Near query curves" if not accepted_label_plotted else ""
            ax.plot(ys, xs, color='blue', alpha=0.6, label=label)
            accepted_label_plotted = True
        else:
            label = "Far away curves" if not rejected_label_plotted else ""
            ax.plot(ys, xs, color='red', alpha=0.3, label=label)
            rejected_label_plotted = True

    # Plot query curve
    k_xs, k_ys = zip(*query_curve)
    ax.plot(k_ys, k_xs, marker='x', linestyle='--', color='black', linewidth=3, label='Query Curve k')

    ax.text(0.01, 0.99, fr'$\delta = {delta}$', transform=ax.transAxes,
            fontsize=12, verticalalignment='top', horizontalalignment='left',
            bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3'))

    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(True)
    ax.axis('equal')
    ax.legend()

plt.tight_layout()
plt.show()