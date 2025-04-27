from abc import ABC, abstractmethod
from typing import Any, List, Union

class SearchProblem(ABC):
    """Abstract base class for search problems."""
    
    @abstractmethod
    def get_neighbors(self, state: Any) -> List[Any]:
        """
        Returns valid neighboring states.
        
        Args:
            state: Current state
            
        Returns:
            list: List of valid neighbor states
        """
        pass
    
    @abstractmethod
    def heuristic(self, state: Any, goal_state: Any) -> float:
        """
        Estimates cost from current state to goal state.
        Must be admissible for optimal path finding.
        
        Args:
            state: Current state
            goal_state: Goal state
            
        Returns:
            float: Estimated cost to goal
        """
        pass

    @abstractmethod
    def get_cost(self, current_state: Any, next_state: Any) -> float:
        """
        Returns the actual cost of moving from current_state to next_state.
        
        Args:
            current_state: Starting state
            next_state: Target neighbor state
            
        Returns:
            float: Actual cost between states
        """
        pass