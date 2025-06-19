# EXTRACT CURVE FROM FILE AS POINTS

def extract_curve(filename, curve_index):
    with open(filename, 'r') as f:
        lines = f.readlines()[1:]  # Skip header line

        if curve_index < 0 or curve_index >= len(lines):
            print("Curve index that failed" , curve_index)
            raise IndexError("Curve index out of range.")

        line = lines[curve_index].strip()
        if not line:
            raise ValueError("Selected curve line is empty.")

        curve = [
            tuple(map(float, pair.strip().split()))
            for pair in line.split('|')
        ]
        return curve

