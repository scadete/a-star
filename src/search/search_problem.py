from abc import ABC
from typing import Any, List, Callable, Dict

class SearchProblem:
    """Base class for search problems with configurable functions."""
    
    def __init__(self, 
                 get_neighbors_fn: Callable[[Any], List[Any]],
                 heuristic_fn: Callable[[Any, Any], float],
                 get_cost_fn: Callable[[Any, Any], float],
                 is_goal_fn: Callable[[Any, Any], bool] = None,
                 **kwargs: Dict[str, Any]):
        """
        Initialize problem with required functions.
        
        Args:
            get_neighbors_fn: Function that returns valid neighbor states
            heuristic_fn: Function that estimates cost to goal
            get_cost_fn: Function that returns actual cost between states
            kwargs: Additional problem-specific parameters
        """
        self._get_neighbors_fn = get_neighbors_fn
        self._heuristic_fn = heuristic_fn
        self._get_cost_fn = get_cost_fn
        self._is_goal_fn = is_goal_fn or (lambda state, goal: state == goal)
        self.params = kwargs
    
    def get_neighbors(self, state: Any) -> List[Any]:
        """Returns valid neighboring states."""
        return self._get_neighbors_fn(state)
    
    def heuristic(self, state: Any, goal_state: Any) -> float:
        """Estimates cost from current state to goal state."""
        return self._heuristic_fn(state, goal_state)
    
    def get_cost(self, current_state: Any, next_state: Any) -> float:
        """Returns actual cost between states."""
        return self._get_cost_fn(current_state, next_state)
    
    def is_goal(self, state: Any, goal_state: Any) -> bool:
        """Tests if current state is the goal state."""
        return self._is_goal_fn(state, goal_state)
    
    def get_path_details(self, path: List[Any]) -> List[Dict[str, Any]]:
        """
        Get basic information about each step in the path.
        This method should be overridden by specific problem implementations
        to provide domain-specific details.
        
        Args:
            path: List of states forming the path
            
        Returns:
            List of dictionaries containing basic step information:
            - from_state: Source state
            - to_state: Destination state
            - cost: Cost between states
        """
        if not path or len(path) < 2:
            return []
            
        details = []
        for i in range(len(path) - 1):
            from_state = path[i]
            to_state = path[i + 1]
            
            step = {
                'from_state': from_state,
                'to_state': to_state,
                'cost': self.get_cost(from_state, to_state)
            }
            details.append(step)
            
        return details