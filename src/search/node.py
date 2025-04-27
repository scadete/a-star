class Node:
    """
    Represents a node in the A* search algorithm.

    Attributes:
        position: Current state/position in the search space
        parent (Node): The parent node, used to reconstruct the path.
        g (float): Cost from the start node to this node.
        h (float): Heuristic cost estimate to the goal node.
        f (float): Total cost (g + h).
    """
    def __init__(self, position, parent=None):
        """
        Initializes a Node object.

        Args:
            position (tuple): The (x, y) coordinates of the node.
            parent (Node, optional): The parent node. Defaults to None.
        """
        self.position = position
        self.parent = parent
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic cost to goal
        self.f = 0  # Total cost (g + h)

    def __lt__(self, other):
        """
        Compares two nodes based on their total cost (f).

        Args:
            other (Node): Another node to compare with.

        Returns:
            bool: True if this node's f cost is less than the other node's f cost.
        """
        return self.f < other.f