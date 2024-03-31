"""TODO: EMPTY DOCSTRING"""

import movie_class
import load_graph


def community_density(edge: float, vertices: int) -> float:
    """Return the density of the community"""

    # movie_community = graph.get_communities()[community_name]
    # vertices = len(movie_community[0])  # total number of vertices in community, used to calculate max edges
    # edges = (movie_community[1])  # number of edges in community
    #
    if vertices <= 1:
        return 0
    else:
        return (2 * edge) / (vertices * (vertices - 1))


def added_weight(new_vertex: movie_class.Movie, community: tuple[set[movie_class.Movie], float]) -> float:
    """Return the weighted sum of the edges that the vertex is connected to in the community proposed for a merge
    O(N) algorithm wher N is the number of vertices"""

    community_vertices = community[0]
    added_weight = 0
    for vertex in community_vertices:
        # print(vertex.title, [u.title for u in new_vertex.neighbours])
        # print(vertex, new_vertex.neighbours)
        # print('test 1', vertex in new_vertex.neighbours)
        # print('test 2', vertex.title in [u.title for u in new_vertex.neighbours])
        # print(vertex.title, [u.title for u in new_vertex.neighbours])
        if vertex.title in [u.title for u in new_vertex.neighbours]:
            # print(vertex)
            # print('TEST')
            added_weight += new_vertex.neighbours[vertex]

    return community[1] + added_weight


def removed_weight(removed_vertex: movie_class.Movie, community: tuple[set[movie_class.Movie], float]) -> float:
    """Return the weighted sum of edges removed when a vertex leaves it original community"""
    community_vertices = community[0]
    removed_weight = 0
    for vertex in community_vertices:
        if vertex.title in [u.title for u in removed_vertex.neighbours]:
            removed_weight += removed_vertex.neighbours[vertex]

    return community[1] - removed_weight


def community_detection(graph: movie_class.Network, epochs: int) -> None:
    """Cluster the graph into communities, greedily maximizing the density of each community"""
    iterations = 0
    while iterations < epochs:
        # print("test epochs")
        vertex_count = 1
        for vertex_name in graph.get_movies():
            vertex = graph.get_movies()[vertex_name]

            max_density_increase = float('-inf')
            density_add_best = 0
            density_rem_best = 0
            best_community = vertex.community

            for neighbour in vertex.neighbours:

                # print(vertex_count, vertex.title, ' ', neighbour.title, ' ', vertex.neighbours[neighbour])

                original_community = graph.get_communities()[vertex.community]
                neighbour_community = graph.get_communities()[neighbour.community]

                # print([u.title for u in original_community[0]])
                # print(type(original_community[0]), type(neighbour_community[0]))
                # print(u.title for u in original_community[0])

                density_add = community_density(added_weight(vertex, neighbour_community), len(original_community) + 1)
                density_rem = community_density(removed_weight(vertex, original_community), len(original_community) - 1)

                # print(density_add, ' ', density_rem)
                density_change = density_add - density_rem
                if density_change > 0:
                    print('hello world')
                if density_change > max_density_increase:
                    max_density_increase = density_change
                    density_add_best = density_add
                    density_rem_best = density_rem
                    best_community = neighbour.community
            vertex_count += 1
            if max_density_increase > 0:
                vertex.community = best_community
                # remove vertex from old community and place it into new community
                # communities: dict[str, tuple[set[Movie], float]]
                graph.change_communities(vertex, best_community, density_add_best, density_rem_best)

        graph.remove_empty_communities()
        iterations += 1


g = load_graph.load_movie_graph('data/Netflix_User_Ratings.csv', 'data/movies.csv')
community_detection(g, 1)
