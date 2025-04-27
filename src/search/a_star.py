import heapq
from .node import Node
from .search_problem import SearchProblem

class AStar:
    """A* pathfinding algorithm implementation."""
    
    def __init__(self, problem: SearchProblem):
        """
        Initialize the A* pathfinder.
        
        Args:
            problem (SearchProblem): Problem instance defining the search space
        """
        self.problem = problem
        self.open_list = []
        self.closed_set = set()
    
    def search(self, start, goal):
        """
        Find the shortest path from start to goal.
        
        Args:
            start: Starting state
            goal: Goal state
            
        Returns:
            list: List of states forming the path, or None if no path found
        """
        self.open_list = []
        self.closed_set = set()
        
        start_node = Node(start)
        goal_node = Node(goal)
        
        heapq.heappush(self.open_list, start_node)
        
        while self.open_list:
            current_node = heapq.heappop(self.open_list)
            self.closed_set.add(current_node.position)
            
            if self.problem.is_goal(current_node.position, goal_node.position):
                return self._reconstruct_path(current_node)
            
            self._evaluate_neighbors(current_node, goal_node)
        
        return None
    
    def _evaluate_neighbors(self, current_node, goal_node):
        """Evaluate all valid neighboring nodes."""
        for neighbor_pos in self.problem.get_neighbors(current_node.position):
            if neighbor_pos in self.closed_set:
                continue
            
            neighbor_node = Node(neighbor_pos, current_node)
            
            edge_cost = self.problem.get_cost(current_node.position, neighbor_pos)
            neighbor_node.g = current_node.g + edge_cost
            neighbor_node.h = self.problem.heuristic(
                neighbor_node.position, 
                goal_node.position
            )
            neighbor_node.f = neighbor_node.g + neighbor_node.h
            
            if self._should_add_to_open_list(neighbor_node):
                heapq.heappush(self.open_list, neighbor_node)

    def _should_add_to_open_list(self, neighbor_node):
        """
        Check if a neighbor node should be added to the open list.
        
        Args:
            neighbor_node (Node): The node to potentially add
            
        Returns:
            bool: True if the node should be added
        """
        for node in self.open_list:
            if neighbor_node.position == node.position and neighbor_node.g >= node.g:
                return False
        return True

    def _reconstruct_path(self, node):
        """
        Reconstruct the path from start to goal.
        
        Args:
            node (Node): The goal node with parent references
            
        Returns:
            list: List of positions from start to goal
        """
        path = []
        while node:
            path.append(node.position)
            node = node.parent
        return path[::-1]