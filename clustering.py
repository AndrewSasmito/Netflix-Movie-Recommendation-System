"""TODO: EMPTY DOCSTRING"""

import movie_class


def community_density(edge: float, vertices: int) -> float:
    """Return the density of the community"""

    # movie_community = graph.get_communities()[community_name]
    # vertices = len(movie_community[0])  # total number of vertices in community, used to calculate max edges
    # edges = (movie_community[1])  # number of edges in community
    #
    return (2 * edge) / (vertices * (vertices - 1))


def added_weight(new_vertex: movie_class.Movie, community: tuple[set[movie_class.Movie], float]) -> float:
    """Return the weighted sum of the edges that the vertex is connected to in the community proposed for a merge
    O(N) algorithm wher N is the number of vertices"""

    community_vertices = community[0]
    added_weight = 0
    for vertex in community_vertices:
        if vertex in new_vertex.neighbours:
            added_weight += new_vertex.neighbours[vertex]

    return community[1] + added_weight


def removed_weight(removed_vertex: movie_class.Movie, community: tuple[set[movie_class.Movie], float]) -> float:
    """Return the weighted sum of edges removed when a vertex leaves it original community"""
    community_vertices = community[0]
    removed_weight = 0
    for vertex in community_vertices:
        if vertex in removed_vertex.neighbours:
            removed_weight += removed_vertex.neighbours[vertex]

    return community[1] - removed_weight


def community_detection(graph: movie_class.Network, epochs: int) -> None:
    """Cluster the graph into communities, greedily maximizing the density of each community"""
    iterations = 0
    while iterations < epochs:
        for vertex_name in graph.get_movies():
            vertex = graph.get_movies()[vertex_name]

            max_density_increase = float('-inf')
            best_community = vertex.community

            for neighbour in vertex.neighbours:
                original_community = graph.get_communities()[vertex.community]
                neighbour_community = graph.get_communities()[neighbour.community]

                density_add = community_density(added_weight(vertex, neighbour_community), len(original_community) + 1)
                density_rem = community_density(removed_weight(vertex, original_community), len(original_community) - 1)

                density_change = density_add - density_rem
                if density_change > max_density_increase:
                    max_density_increase = density_change
                    best_community = neighbour.community

            if max_density_increase > 0:
                vertex.community = best_community
        graph.remove_empty_communities()
        iterations += 1
