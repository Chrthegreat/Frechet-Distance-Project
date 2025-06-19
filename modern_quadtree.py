import numpy as np

###########################################################################################################################################

# THIS FILE CREATES THE QUATREE AND ITS METHODS

class QuadtreeNode:
    def __init__(self, min_coords, max_coords, max_elements=4):
        self.min_coords = np.array(min_coords) # Bounding box limits 
        self.max_coords = np.array(max_coords)
        self.max_elements = max_elements # Max contained elements
        self.elements = []  # list of tuples (point, data)
        self.children = None

    def insert(self, point, data):
        point = np.array(point) 
        # If we have children, delegate insertion to appropriate child
        if self.children is not None:
            child = self._get_child(point) 
            child.insert(point, data)
            return

        # Otherwise, store element here
        self.elements.append((point, data))

        # Split if needed
        if len(self.elements) > self.max_elements:
            self._split()

    def _split(self):
        mid = (self.min_coords + self.max_coords) / 2 # Midpoint
        dims = len(self.min_coords) # Dimension. 8 in our case

        # Create children nodes (2^dims)
        self.children = []
        for i in range(2 ** dims):
            # The starting coordinates of each child are the fathers
            min_c = self.min_coords.copy()
            max_c = self.max_coords.copy()
            for d in range(dims):
                if (i >> d) & 1: # Binary right shift and bitwise AND
                    min_c[d] = mid[d]
                else:
                    max_c[d] = mid[d]
            self.children.append(QuadtreeNode(min_c, max_c, self.max_elements))

        # Move elements to children
        for point, data in self.elements:
            child = self._get_child(point)
            child.insert(point, data)

        # Clear current node's elements
        self.elements = []

    def _get_child(self, point):
        # Mid point in each direction
        mid = (self.min_coords + self.max_coords) / 2
        index = 0
        for d in range(len(point)): # Check all dimensions
            if point[d] >= mid[d]:  # Whether the point is on top half or bottom half
                index |= (1 << d)   # If top half d bit is 1, otherwise 0
        return self.children[index] # Index of the child it belongs to

    def query(self, center, radius):
        results = []
        self._query_recursive(np.array(center), radius, results)
        return results

    def _query_recursive(self, center, radius, results):
        # Check if bounding box intersects the hypersphere
        if np.any(self.min_coords > center + radius) or np.any(self.max_coords < center - radius):
            return

        # Leaf node: check all elements
        if self.children is None:
            for point, data in self.elements:
                if np.linalg.norm(point - center) <= radius:
                    results.append(data)
            return

        # Otherwise recurse into children
        for child in self.children:
            child._query_recursive(center, radius, results)

class Quadtree:
    def __init__(self, points, max_elements=4):
        
        if not points:
            raise ValueError("Points list is empty!")

        # Calculate global min/max coords over all points
        all_points = np.array([p for p, _ in points])
        min_coords = np.min(all_points, axis=0)
        max_coords = np.max(all_points, axis=0)

        # Expand slightly so points on edges fit properly
        eps = 1e-8
        min_coords -= eps
        max_coords += eps

        self.root = QuadtreeNode(min_coords, max_coords, max_elements)
        for point, data in points:
            self.root.insert(point, data)

    def insert(self, point, data):
        self.root.insert(point, data)

    def query(self, center, radius):
        return self.root.query(center, radius)