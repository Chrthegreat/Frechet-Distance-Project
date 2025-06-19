import numpy as np

# FIND CRITICAL EPSILONS

def point_segment_distance(p, seg):
    #Compute the shortest distance from point p to segment (s0, s1).
    s0, s1 = np.array(seg[0]), np.array(seg[1]) # Segment
    p = np.array(p)  # Single Point
    d = s1 - s0  # d = p0 - p1
    l2 = np.dot(d, d) # ||d|| ^ 2
    if l2 == 0:   # Check if segment is just a point
        return np.linalg.norm(p - s0)
    t = np.dot(p - s0, d) / l2  # Find the projection
    t = np.clip(t, 0, 1)   # Clip it in [0,1]
    projection = s0 + t * d  # Find the point in the segment
    return np.linalg.norm(p - projection) # Return the distance

def compute_critical_epsilons(P, Q):
    # Defie this as set to avoid duplicates
    epsilons = set()

    # Vertex-vertex distances
    for p in P:
        for q in Q:
            # Find the distances of all the points of the curves
            eps = np.linalg.norm(np.array(p) - np.array(q))
            epsilons.add(eps)

    # Vertex-to-segment distances: P vertex to Q segment
    for p in P:
        for i in range(len(Q) - 1):
            q_seg = (Q[i], Q[i + 1]) # Segment
            eps = point_segment_distance(p, q_seg) # Use function
            epsilons.add(eps)

    # Vertex-to-segment distances: Q vertex to P segment
    for q in Q:
        for i in range(len(P) - 1):
            p_seg = (P[i], P[i + 1]) # Segment
            eps = point_segment_distance(q, p_seg) # Use function
            epsilons.add(eps)

    # Return sorted list of unique critical values
    return sorted(epsilons)
