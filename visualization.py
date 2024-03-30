import networkx as nx
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.colors as mcolors


import movie_class
import load_graph
import clustering
g = load_graph.load_weighted_review_graph('data/Netflix_User_Ratings.csv', 'data/movies.csv')
clustering.community_detection(g, 1)

def visualize_network(graph: movie_class.Network) -> None:
    """Function to visualize the graph"""
    # communities: dict[str, tuple[set[Movie], float]]
    G = nx.Graph()
    counter = 0
    for movie in graph.get_movies():
        print(counter)
        counter += 1
        G.add_node(movie, color='red')
        for neighbour in graph.get_movies()[movie].neighbours:
            G.add_edge(neighbour.title, round(graph.get_movies()[movie].neighbours[neighbour]))

    # Draw the graph
    pos = nx.spring_layout(G)  # Positions for all nodes
    nx.draw(G, pos, with_labels=True, node_color='red', font_size=10)  # Draw nodes and labels
    nx.draw_networkx_edge_labels(G, pos)  # Draw edge labels
    plt.show()

    # all_communities = [title for title in graph.get_communities() if len(graph.get_communities()[title][0]) > 0]
    # print(all_communities)
    # print(graph.get_communities())
    # for vertex in graph.get_movies():
    #     G.add_node(vertex.title, color)

    return None

# visualize_network(g)
#
# def funct():
#     # Create a graph
#     G = nx.Graph()
#
#     # Add nodes with attributes
#     G.add_node('A', color='red')
#     G.add_node('B', color='blue')
#     G.add_node('C', color='green')
#
#     # Add edges
#     G.add_edge('A', 'B')
#     G.add_edge('B', 'C')
#     G.add_edge('B', "A")
#
#     # Get node colors from node attributes
#     node_colors = [G.nodes[n]['color'] for n in G.nodes]
#
#     # Draw the graph with specified node colors
#     nx.draw(G, with_labels=True, node_color=node_colors, node_size=1500, font_size=15)
#
#     all_colors = dict(mcolors.CSS4_COLORS)
#
#     # Print the dictionary (for demonstration purposes)
#     print(all_colors)
#
#     filtered_colors = {name: color for name, color in all_colors.items() if
#                        mcolors.rgb_to_hsv(mcolors.to_rgb(color))[2] > 0.5}
#
#     # Print the filtered dictionary (for demonstration purposes)
#     print(filtered_colors)
#
#     # Draw the graph
#     pos = nx.spring_layout(G)  # Define layout (positions of nodes)
#     # nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=15)
#
#     # Add interactivity: Display node attributes on hover
#     mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_text()))
#
#     # Show the plot
#     plt.show()
