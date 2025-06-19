import numpy as np

# SOLVE QUADRATIC INEQUATION TO FIND CELL FREE SPACE

def point_on_segment(p0, p1, t):
    return (1 - t) * np.array(p0) + t * np.array(p1)

def interval_within_epsilon(seg, point, epsilon):
    p0, p1 = seg
    q = np.array(point)
    d = np.array(p1) - np.array(p0)
    a = np.dot(d, d)
    b = 2 * np.dot(d, np.array(p0) - q)
    c = np.dot(np.array(p0) - q, np.array(p0) - q) - epsilon**2
    disc = b**2 - 4*a*c
    if disc < 0:
        return None
    sqrt_disc = np.sqrt(disc)

    if a == 0:
        # Check if segment is a single point
        dist = np.linalg.norm(np.array(p0) - q)
        if dist <= epsilon:
            # Entire segment is just that point, so interval is [0, 1]
            return (0.0, 1.0)
        else:
            # Outside epsilon radius
            return None
        
    t1 = (-b - sqrt_disc) / (2*a)
    t2 = (-b + sqrt_disc) / (2*a)
    start = max(0.0, t1)
    end = min(1.0, t2)
    if start > end:
        return None
    return (start, end)

def cell_free_space(p_seg, q_seg, epsilon):
    bottom = interval_within_epsilon(p_seg, q_seg[0], epsilon)
    top = interval_within_epsilon(p_seg, q_seg[1], epsilon)
    left = interval_within_epsilon(q_seg, p_seg[0], epsilon)
    right = interval_within_epsilon(q_seg, p_seg[1], epsilon)
    return {"bottom": bottom, "top": top, "left": left, "right": right}

################################################################################################################################################

# DECIDE FOR CLASSIC CASE IF PATH EXISTS. LOOP EVERY CELL

def decision(P, Q, epsilon):
    P_segments = [(P[i], P[i+1]) for i in range(len(P)-1)]
    Q_segments = [(Q[i], Q[i+1]) for i in range(len(Q)-1)]

    #print(f"decision called with epsilon={epsilon}")
    #print(f"P segments: {len(P_segments)}, Q segments: {len(Q_segments)}")

    m, n = len(P_segments), len(Q_segments)

    # Compute free space intervals
    free_space = [[None for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            p_seg = P_segments[i]
            q_seg = Q_segments[j]
            free_space[i][j] = cell_free_space(p_seg, q_seg, epsilon)
    # Reachability matrix
    reachable = [[False for _ in range(n)] for _ in range(m)]

    # Step 1: Initialize bottom-left cell (0, 0)
    start_cell = free_space[0][0]
    if start_cell["bottom"] and start_cell["left"]:
        if start_cell["bottom"][0] <= 0.0 and start_cell["left"][0] <= 0.0:
            reachable[0][0] = True

    # Step 2: Propagate reachability
    for i in range(m):
        for j in range(n):
            if not reachable[i][j]:
                continue
            cell = free_space[i][j]

            # Right neighbor
            if j + 1 < n and cell["right"] and free_space[i][j+1]["left"]:
                reachable[i][j+1] = True

            # Top neighbor
            if i + 1 < m and cell["top"] and free_space[i+1][j]["bottom"]:
                reachable[i+1][j] = True

            # Diagonal neighbor (optional, for monotonicity across both)
            if i + 1 < m and j + 1 < n:
                if cell["top"] and cell["right"]:
                    if cell["top"][1] == 1.0 and cell["right"][1] == 1.0:
                        reachable[i+1][j+1] = True

    # Step 3: Check final cell (top-right)
    final_cell = free_space[m-1][n-1]
    if reachable[m-1][n-1] and final_cell["top"] and final_cell["right"]:
        if final_cell["top"][1] >= 1.0 and final_cell["right"][1] >= 1.0:
            return True
    return False