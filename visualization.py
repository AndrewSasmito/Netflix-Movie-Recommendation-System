"""CSC111 Winter 2024 Exercise 4 (Graphs Visualization)

Module Description
==================

This module contains some Python functions that you can use to visualize the graphs
you're working with on this assignment. You should not modify anything in this file.
It will not be submitted for grading.

Disclaimer: we didn't have time to make this file fully PythonTA-compliant!

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
import networkx as nx
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.colors as mcolors


import movie_class
import load_graph
import clustering
from plotly.graph_objs import Scatter, Figure

g = load_graph.load_weighted_review_graph('data/Netflix_User_Ratings.csv', 'data/movies.csv')

# Colours to use when visualizing different clusters.
COLOUR_SCHEME = [
    '#2E91E5', '#E15F99', '#1CA71C', '#FB0D0D', '#DA16FF', '#222A2A', '#B68100',
    '#750D86', '#EB663B', '#511CFB', '#00A08B', '#FB00D1', '#FC0080', '#B2828D',
    '#6C7C32', '#778AAE', '#862A16', '#A777F1', '#620042', '#1616A7', '#DA60CA',
    '#6C4516', '#0D2A63', '#AF0038'
]

LINE_COLOUR = 'rgb(210,210,210)'
VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'
BOOK_COLOUR = 'rgb(89, 205, 105)'
USER_COLOUR = 'rgb(105, 89, 205)'


def setup_graph(graph: movie_class.Network) -> list:
    """Use plotly and networkx to setup the visuals for the given graph.

    Optional arguments:
        - weighted: True when weight data should be visualized
    """

    G = nx.Graph()
    # counter = 0
    for movie in graph.get_movies():
        # print(counter)
        # counter += 1
        G.add_node(movie, color='red')
        # if len(graph.get_movies()[movie].neighbours) == 0:
        #     pass
        for neighbour in graph.get_movies()[movie].neighbours:
            G.add_edge(neighbour.title, round(graph.get_movies()[movie].neighbours[neighbour]))

    pos = getattr(nx, 'spring_layout')(G)

    x_values = [pos[k][0] for k in G.nodes]
    y_values = [pos[k][1] for k in G.nodes]
    labels = list(G.nodes)

    weights = nx.get_edge_attributes(G, 'weight')

    # kinds = [graph_nx.nodes[k]['kind'] for k in graph_nx.nodes]

    # colours = [BOOK_COLOUR if kind == 'book' else USER_COLOUR for kind in kinds]

    x_edges = []
    y_edges = []
    weight_positions = []

    for edge in G.edges:
        x1, x2 = pos[edge[0]][0], pos[edge[1]][0]
        x_edges += [x1, x2, None]
        y1, y2 = pos[edge[0]][1], pos[edge[1]][1]
        y_edges += [y1, y2, None]
        weight_positions.append(((x1 + x2) / 2, (y1 + y2) / 2, weights[(edge[0], edge[1])]))

    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines+text',
                     name='edges',
                     line=dict(color=LINE_COLOUR, width=1),
                     )

    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker=dict(symbol='circle-dot',
                                 size=5,
                                 color='red',
                                 line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                                 ),
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    data = [trace3, trace4]


    return [weight_positions, data]



def visualize_graph(graph: movie_class.Network) -> None:
    """Use plotly and networkx to visualize the given graph.

    Optional arguments:
        - layout: which graph layout algorithm to use
        - max_vertices: the maximum number of vertices that can appear in the graph
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
    """

    draw_graph(setup_graph(graph, 'spring_layout', 1001), output_file)


def visualize_weighted_graph(graph: ex4_part2.WeightedGraph,
                             layout: str = 'spring_layout',
                             max_vertices: int = 5000,
                             output_file: str = '') -> None:
    """Use plotly and networkx to visualize the given weighted graph.

    Optional arguments:
        - layout: which graph layout algorithm to use
        - max_vertices: the maximum number of vertices that can appear in the graph
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
    """

    weight_positions, data = setup_graph(graph, layout, max_vertices, True)
    draw_graph(data, output_file, weight_positions)


def draw_graph(data: list, output_file: str = '', weight_positions=None) -> None:
    """
    Draw graph based on given data.

    Optional arguments:
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
        - weight_positions: weights to draw on edges for a weighted graph
    """

    fig = Figure(data=data)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    if weight_positions:
        for w in weight_positions:
            fig.add_annotation(
                x=w[0], y=w[1],  # Text annotation position
                xref="x", yref="y",  # Coordinate reference system
                text=w[2],  # Text content
                showarrow=False  # Hide arrow
            )

    if output_file == '':
        fig.show()
    else:
        fig.write_image(output_file)








# import networkx as nx
# import matplotlib.pyplot as plt
# import mplcursors
# import matplotlib.colors as mcolors
#
#
# import movie_class
# import load_graph
# import clustering
# from plotly.graph_objs import Scatter, Figure
#
# g = load_graph.load_weighted_review_graph('data/Netflix_User_Ratings.csv', 'data/movies.csv')
# # clustering.community_detection(g, 1)
#
#
# def visualize_network(graph: movie_class.Network) -> None:
#     """Function to visualize the graph"""
#     # communities: dict[str, tuple[set[Movie], float]]
#     G = nx.Graph()
#     counter = 0
#     for movie in graph.get_movies():
#         # print(counter)
#         counter += 1
#         G.add_node(movie, color='red')
#         # if len(graph.get_movies()[movie].neighbours) == 0:
#         #     pass
#         for neighbour in graph.get_movies()[movie].neighbours:
#             G.add_edge(neighbour.title, round(graph.get_movies()[movie].neighbours[neighbour]))
#
#     pos = getattr(nx, 'spring_layout')(G)
#     print('asdfjk;kjasdf;j',pos)
#
#     x_values = [pos[k][0] for k in G.nodes]
#     y_values = [pos[k][1] for k in G.nodes]
#     labels = list(G.nodes)
#     # kinds = [G.nodes[k]['kind'] for k in G.nodes]
#
#     # colours = [BOOK_COLOUR if kind == 'book' else USER_COLOUR for kind in kinds]
#
#     x_edges = []
#     y_edges = []
#     for edge in G.edges:
#         x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
#         y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]
#
#     trace3 = Scatter(x=x_edges,
#                      y=y_edges,
#                      mode='lines',
#                      name='edges',
#                      line=dict(color='rgb(210,210,210)', width=1),
#                      hoverinfo='none',
#                      )
#     trace4 = Scatter(x=x_values,
#                      y=y_values,
#                      mode='markers',
#                      name='nodes',
#                      marker=dict(symbol='circle-dot',
#                                  size=5,
#                                  color='blue',
#                                  line=dict(color='rgb(50, 50, 50)', width=0.5)
#                                  ),
#                      text=labels,
#                      hovertemplate='%{text}',
#                      hoverlabel={'namelength': 0}
#                      )
#
#     data1 = [trace3, trace4]
#     fig = Figure(data=data1)
#     fig.update_layout({'showlegend': False})
#     fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
#     fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
#
#     fig.show()
#
#     # Draw the graph
#     # pos = nx.spring_layout(G)  # Positions for all nodes
#     # nx.draw(G, pos, with_labels=True, node_color='red', font_size=10)  # Draw nodes and labels
#     # nx.draw_networkx_edge_labels(G, pos)  # Draw edge labels
#     # plt.show()
#
#     # all_communities = [title for title in graph.get_communities() if len(graph.get_communities()[title][0]) > 0]
#     # print(all_communities)
#     # print(graph.get_communities())
#     # for vertex in graph.get_movies():
#     #     G.add_node(vertex.title, color)
#
#     return None
#
# visualize_network(g)
#
# # def funct():
# #     # Create a graph
# #     G = nx.Graph()
# #
# #     # Add nodes with attributes
# #     G.add_node('A', color='red')
# #     G.add_node('B', color='blue')
# #     G.add_node('C', color='green')
# #
# #     # Add edges
# #     G.add_edge('A', 'B')
# #     G.add_edge('B', 'C')
# #     G.add_edge('B', "A")
# #
# #     # Get node colors from node attributes
# #     node_colors = [G.nodes[n]['color'] for n in G.nodes]
# #
# #     # Draw the graph with specified node colors
# #     nx.draw(G, with_labels=True, node_color=node_colors, node_size=1500, font_size=15)
# #
# #     all_colors = dict(mcolors.CSS4_COLORS)
# #
# #     # Print the dictionary (for demonstration purposes)
# #     print(all_colors)
# #
# #     filtered_colors = {name: color for name, color in all_colors.items() if
# #                        mcolors.rgb_to_hsv(mcolors.to_rgb(color))[2] > 0.5}
# #
# #     # Print the filtered dictionary (for demonstration purposes)
# #     print(filtered_colors)
# #
# #     # Draw the graph
# #     pos = nx.spring_layout(G)  # Define layout (positions of nodes)
# #     # nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=15)
# #
# #     # Add interactivity: Display node attributes on hover
# #     mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_text()))
# #
# #     # Show the plot
# #     plt.show()
