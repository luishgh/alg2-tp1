class KDTreeNode:
    def __init__(self, point, l, r):
        """
        left: points with axis values <= point[axis]
        right: points with axis values >= point[axis]
        point: point at this node
        l: minimum value of the axis at this node
        r: maximum value of the axis at this node
        """
        self.left = None
        self.right = None
        self.point = point
        self.l = l
        self.r = r

class KDTree:
    def __init__(self, points, k=2):
        """
        K dimensional tree (KD-Tree) for efficient range queries.
        points: list of points, each point is a list of coordinates
        k: number of dimensions (default is 2)
        """
        self.k = k
        if points:
            self.root = self.build(points, depth=0)
        else:
            raise ValueError("KDTree cannot be built with an empty list of points")

    def build(self, points, depth):
        """
        Builds the KD-Tree recursively.
        points: current list of points
        depth: current depth in the tree, used to determine the axis
        """
        if not points:
            return None

        axis = depth % self.k

        # Sort points by the current axis and choose the median as the pivot
        points.sort(key=lambda x: x[axis])
        median_index = len(points) // 2

        node = KDTreeNode(point=points[median_index], l = points[0][axis], r = points[-1][axis])
        node.left = self.build(points[:median_index], depth + 1)
        node.right = self.build(points[median_index + 1:], depth + 1)

        return node
    
    def _query(self, node, ranges, depth, results):
        if node is None:
            return

        axis = depth % self.k

        l = ranges[axis][0]
        r = ranges[axis][1]

        #print(f"Querying node: {node.point}, axis: {axis}, range: {l} to {r}")

        # Check if current node intersects with the range
        if l > node.r or r < node.l:
            return
        
        # Check if the point is within all range
        if all(ll <= node.point[i] <= rr for i, (ll, rr) in enumerate(ranges)):
            results.append(node.point)

        # Traverse left or right subtree based on the current axis
        if node.left and l <= node.point[axis]:
            self._query(node.left, ranges, depth + 1, results)
        if node.right and r >= node.point[axis]:
            self._query(node.right, ranges, depth + 1, results)
        
            
    
    def query(self, ranges):
        """
        ranges: list of tuples, each tuple of the form (l, r) for each dimension
        Returns list of points that fall within the specified ranges in each dimension.
        """
        if not self.root:
            return []
        
        # Validate ranges
        if len(ranges) != self.k or any(len(r) != 2 for r in ranges):
            raise ValueError("Ranges must be a list of tuples with two elements each, one for each dimension.")
        
        for i, (l, r) in enumerate(ranges):
            if l > r:
                raise ValueError(f"Each range must be a tuple (l, r) where l <= r, got {l} > {r} at axis {i}")

        results = []
        self._query(self.root, ranges, 0, results)
        return results