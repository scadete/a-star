from typing import Dict, List
import networkx as nx
import matplotlib.pyplot as plt

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
              pos: Dict[str, tuple] = None):
    """
    Plot the graph with optional path highlighting.
    
    Args:
        distances: Dictionary of distances between nodes
        path: Optional list of nodes representing the route
        show_distances: Whether to show distance labels on edges
        figsize: Figure size as (width, height) tuple
        pos: Fixed positions for nodes
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
    
    # Draw edges first (background)
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
    
    # Draw city labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    # If path is provided, highlight it
    if path and len(path) > 1:
        # Create edges pairs from path
        path_edges = list(zip(path[:-1], path[1:]))
        
        # Highlight the path edges
        nx.draw_networkx_edges(G, pos,
                             edgelist=path_edges,
                             edge_color='red',
                             width=2)
        
        # Highlight path nodes
        nx.draw_networkx_nodes(G, pos,
                             nodelist=path,
                             node_color='lightgreen',
                             node_size=700,
                             alpha=0.7)
    
    plt.title("Graph", pad=20, fontsize=14)
    plt.axis('off') 
    plt.tight_layout()
    plt.show()

def plot_lines_with_colors(line_config: Dict[str, Dict[str, any]], pos: Dict[str, tuple]):
    """
    Plot the lines with their respective colors based on the line configuration.
    
    Args:
        line_config: Dictionary containing line configurations with colors
        pos: Fixed positions for nodes
    """
    # Map line IDs to colors
    line_colors = {'R': 'red', 'G': 'green', 'B': 'blue', 'Y': 'yellow'}
    
    # Create a graph
    G = nx.Graph()
    
    # Add nodes and edges based on line configuration
    for line_id, config in line_config.items():
        color = line_colors.get(line_id, 'black')  # Default to black if color not found
        stations = config['stations']
        for i in range(len(stations) - 1):
            G.add_edge(stations[i], stations[i + 1], color=color)
    
    # Set up the plot
    plt.figure(figsize=(12, 8))
    
    # Draw edges with respective colors
    for edge in G.edges(data=True):
        nx.draw_networkx_edges(G, pos, edgelist=[(edge[0], edge[1])], edge_color=edge[2]['color'], width=2)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=700, alpha=0.7)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    plt.title("Lines with Respective Colors", pad=20, fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.show()