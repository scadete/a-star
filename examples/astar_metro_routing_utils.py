from typing import Dict, List
import networkx as nx
import matplotlib.pyplot as plt
from src.search import SearchProblem

def create_fixed_layout(complete_graph: Dict[str, Dict[str, float]]) -> Dict[str, tuple]:
    """
    Create a fixed layout for all nodes combining distance and heuristic graphs.
    
    Args:
        combined_graph: Dictionary containing all nodes and their connections
        
    Returns:
        Dictionary mapping node names to (x, y) positions
    """
    # Create graph
    G = nx.Graph()
    
    # Add edges with weights
    for city1, neighbors in complete_graph.items():
        for city2, distance in neighbors.items():
            G.add_edge(city1, city2, weight=distance)
    
    # Add all nodes from the graph
    for node in complete_graph.keys():
        G.add_node(node)
    
    # Generate layout once
    return nx.spring_layout(G, k=1.5, iterations=50, seed=42)
def plot_graph(distances: Dict[str, Dict[str, float]], 
              path: List[str] = None,
              show_distances: bool = True,
              figsize: tuple = (12, 8),
              pos: Dict[str, tuple] = None,
              line_config: Dict[str, Dict[str, any]] = None):
    """
    Plot the graph with metro lines, optional path highlighting and distances.
    
    Args:
        distances: Dictionary of distances between nodes
        path: Optional list of nodes representing the route
        show_distances: Whether to show distance labels on edges
        figsize: Figure size as (width, height) tuple
        pos: Fixed positions for nodes
        line_config: Optional dictionary containing line configurations with colors
    """
    # Create graph
    G = nx.Graph()
    
    # Add edges with weights
    for city1, neighbors in distances.items():
        for city2, distance in neighbors.items():
            G.add_edge(city1, city2, weight=distance)
    
    # Set up the plot
    plt.figure(figsize=figsize)
    
    # Use provided positions or generate new ones
    if pos is None:
        pos = nx.spring_layout(G, k=1.5, iterations=50)

    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.3, width=1)
        
    # Draw metro lines if configuration is provided
    if line_config:
        line_colors = {'R': 'red', 'G': 'green', 'B': 'blue', 'Y': 'yellow'}
        
        # For each edge in distances, check if it belongs to a metro line
        for station1, neighbors in distances.items():
            for station2 in neighbors:
                # Find which line (if any) this connection belongs to
                for line_id, config in line_config.items():
                    stations = config['stations']
                    # Check if both stations are in this line and consecutive
                    if station1 in stations and station2 in stations:
                        color = line_colors.get(line_id, 'black')
                        nx.draw_networkx_edges(G, pos,
                                                edgelist=[(station1, station2)],
                                                edge_color=color,
                                                width=2,
                                                alpha=0.7)
    else:
        # Draw regular edges if no line configuration
        nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5)
    
    # Draw edge labels if requested
    if show_distances:
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, 
                          node_color='lightblue',
                          node_size=700,
                          alpha=0.7)
    
    # Draw station labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    # If path is provided, highlight it
    if path and len(path) > 1 and line_config:
        path_edges = list(zip(path[:-1], path[1:]))
        line_colors = {'R': 'red', 'G': 'green', 'B': 'blue', 'Y': 'yellow'}
        
        for station1, station2 in path_edges:
            # Find which line this edge belongs to
            for line_id, config in line_config.items():
                stations = config['stations']
                if station1 in stations and station2 in stations:
                    idx1, idx2 = stations.index(station1), stations.index(station2)
                    if abs(idx1 - idx2) == 1:  # stations are consecutive in the line
                        color = line_colors.get(line_id, 'red')
                        # Draw highlighted edge with line's color
                        nx.draw_networkx_edges(G, pos,
                                            edgelist=[(station1, station2)],
                                            edge_color=color,
                                            width=4,  # thicker for highlighting
                                            alpha=1.0)  # full opacity for highlight
        
        # Highlight stations in path
        nx.draw_networkx_nodes(G, pos,
                             nodelist=path,
                             node_color='lightgreen',
                             node_size=700,
                             alpha=0.7)
    
    plt.title("Metro Network", pad=20, fontsize=14)
    plt.axis('off') 
    plt.tight_layout()
    plt.show()