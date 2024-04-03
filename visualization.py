import networkx as nx
from plotly.graph_objs import Scatter, Figure
import movie_class
import colorsys

import load_graph
import clustering

class GraphVisualization:
    """
    Graph Visualization class
    """

    colour_scheme: list[str]
    line_colour: str
    border_colour: str
    movie_colour: str

    def __init__(self, colour_scheme: list[str], line_colour: str, border_colour: str, movie_colour: str) -> None:
        # In the format 'rgb(x,y,z)'
        # Colour scheme, list of hexadecimals
        self.colour_scheme = colour_scheme
        self.line_colour = line_colour
        self.border_colour = border_colour
        self.movie_colour = movie_colour


def generate_color_scheme(graph: movie_class.Network) -> dict[str, str]:
    """
    Generate random colours
    """
    colors = {}
    i = 0
    for community in graph.get_communities():
        hue = i / len(graph.get_communities())  # Varying the hue across the color spectrum
        lightness = 0.5  # You can adjust lightness if needed
        saturation = 0.7  # You can adjust saturation if needed
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        hex_color = '#{:02x}{:02x}{:02x}'.format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        colors[community] = hex_color
        i += 1

    return colors


def setup_graph(graph: movie_class.Network,
                layout: str = 'spring_layout',
                max_vertices: int = 5000) -> list:
    """Use plotly and networkx to setup the visuals for the given graph.

    Optional arguments:
        - weighted: True when weight data should be visualized
    """

    # Creating the graph
    graph_nx = nx.Graph()
    movies = graph.get_movies()
    visited = set()
    for movie in movies:
        graph_nx.add_node(movie, kind=movies[movie].community)

    for movie in movies:
        visited.add(movies[movie])
        for neighbour in movies[movie].neighbours:
            if neighbour not in visited:
                graph_nx.add_edge(neighbour.title, movies[movie].title, weight=round(neighbour.neighbours[movies[movie]], 2))


    # graph_nx set up?
    pos = getattr(nx, layout)(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)

    weights = nx.get_edge_attributes(graph_nx, 'weight')

    kinds = [graph_nx.nodes[k]['kind'] for k in graph_nx.nodes]

    # Generating the colours
    possible_colours = generate_color_scheme(graph)
    colours = [possible_colours[kind] for kind in kinds]

    x_edges = []
    y_edges = []
    weight_positions = []

    for edge in graph_nx.edges:
        x1, x2 = pos[edge[0]][0], pos[edge[1]][0]
        x_edges += [x1, x2, None]
        y1, y2 = pos[edge[0]][1], pos[edge[1]][1]
        y_edges += [y1, y2, None]
        weight_positions.append(((x1 + x2) / 2, (y1 + y2) / 2, weights[(edge[0], edge[1])]))

    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines+text',
                     name='edges',
                     line=dict(color='rgb(220,220,220)', width=1),
                     )

    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker=dict(symbol='circle-dot',
                                 size=5,
                                 color=colours,
                                 line=dict(color='rgb(50,50,50)', width=0.5)
                                 ),
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    data = [trace3, trace4]

    return [weight_positions, data]


def visualize_weighted_graph(graph: movie_class.Network,
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

    weight_positions, data = setup_graph(graph, layout, max_vertices)
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


graph = load_graph.load_movie_graph('data/shuffled_user_ratings.csv', 'data/movies.csv', 20, 20000)
print('a')
clustering.louvain(graph, 3)
print('b')
visualize_weighted_graph(graph)
print('C')
