"""TODO: EMPTY DOCSTRING"""

import movie_class

def sigma_in(community: list[set[movie_class.Movie] | float]):
    """ A helper function to find the sum of all the weighted edges strictly inside community"""
    return community[1]


def sigma_tot(community: list[set[movie_class.Movie] | float]) -> float:
    """ A helper function to find the sum of all the edges inside the community. The sum of all
    incident edges double counts edges in the community, so subtract that to get sum of all weighted
    edges incident"""
    incident_edges = 0
    for vertex in community[0]:
        incident_edges += vertex.sum_weights
    return incident_edges - sigma_in(community)


def k_i_in(added_vertex: movie_class.Movie, community: list[set[movie_class.Movie] | float]) -> float:
    """TODO: Docstring for k_i_in"""
    incident_edges = 0

    for community_vertex in community[0]:
        if added_vertex in community_vertex.neighbours:
            incident_edges += added_vertex.neighbours[community_vertex]

    return incident_edges


def k_i_out(removed_vertex: movie_class.Movie, community: list[set[movie_class]]) -> float:
    """TODO: Docstring for k_i_out"""
    removed_edges = 0
    for vertex in community[0]:
        if vertex in removed_vertex.neighbours:
            removed_edges += removed_vertex.neighbours[vertex]
    return removed_edges


def k_i(added_vertex: movie_class.Movie):
    """TODO: Docstring for k_i"""
    return added_vertex.sum_weights


def m_func(graph: movie_class.Network):
    """TODO: Docstring for m"""
    all_edge_weight = 0
    for vertex in graph.get_movies():
        all_edge_weight += graph.get_movies()[vertex].sum_weights
    return all_edge_weight / 2


def louvain(graph: movie_class.Network, epochs: int) -> None:
    """TODO: Docstring for louvain"""
    m = m_func(graph)
    for _ in range(epochs):
        for vertex_name in graph.get_movies():
            vertex = graph.get_movies()[vertex_name]
            max_q = 0
            best_community = vertex.community
            for neighbour in vertex.neighbours:
                # print(vertex_name, neighbour.title)
                community = graph.get_communities()[neighbour.community]
                # print(len(community))
                sum_in = sigma_in(community)
                sum_tot = sigma_tot(community)
                ki = k_i(vertex)
                kin = k_i_in(vertex, community)
                # print(sum_in, sum_tot)

                delta_q = (((sum_in + kin) / (2 * m)) - (((sum_tot + ki) / (2 * m)) ** 2)) - (
                            (sum_in / (2 * m)) - ((sum_tot / (2 * m)) ** 2) - (ki / (2 * m)) ** 2)
                # print(delta_q)
                if max_q < delta_q and len(community[0]) < 50:
                    max_q = delta_q
                    best_community = neighbour.community

            if max_q > 0:
                neighbour_community = graph.get_communities()[best_community]
                old_community = graph.get_communities()[vertex.community]
                best_k_i_in = k_i_in(vertex, neighbour_community)
                best_k_i_out = k_i_out(vertex, old_community)
                graph.change_communities(vertex, best_community, best_k_i_in, best_k_i_out)
                vertex.community = best_community
                # print(graph.get_communities())


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['movie_class'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
