"""File to run Louvains clustering algorithm"""

import movie_class


def sigma_in(community: list[set[movie_class.Movie] | float]) -> float:
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
    """Helper function to calculate the sum of all the weighted edges that added_vertex connect to
    inside the new community we are considering merging it into"""
    incident_edges = 0

    for community_vertex in community[0]:
        if added_vertex in community_vertex.neighbours:
            incident_edges += added_vertex.neighbours[community_vertex]

    return incident_edges


def k_i_out(removed_vertex: movie_class.Movie, community: list[set[movie_class]]) -> float:
    """Helper function to calculate the sum of all the weighted edges that removed_vertex connect to in
    its original community"""
    removed_edges = 0
    for vertex in community[0]:
        if vertex in removed_vertex.neighbours:
            removed_edges += removed_vertex.neighbours[vertex]
    return removed_edges


def k_i(added_vertex: movie_class.Movie) -> float:
    """Helper function to return the sum of weighted of the edges of a given vertex"""
    return added_vertex.sum_weights


def m_func(graph: movie_class.Network) -> float:
    """function to determine the sum of weighted edges of an entire graph"""
    all_edge_weight = 0
    for vertex in graph.get_movies():
        all_edge_weight += graph.get_movies()[vertex].sum_weights
    return all_edge_weight / 2


def louvain(graph: movie_class.Network, epochs: int) -> None:
    """Modified Louvains algorithm for community detection. Our algorithm follows phase 1
    of the Louvains algorithm for a certain number of epochs to assign the movies in a graph
    to communities. Although the resulting graph might result in a lower overall modularity,
    we insist the size of a community is less than 50, in order to make more balanced calculations
    with respect to the dataset so the majority of the dataset doesn't fall under a single community"""
    m = m_func(graph)
    for _ in range(epochs):
        for vertex_name in graph.get_movies():
            vertex = graph.get_movies()[vertex_name]
            max_q = 0
            best_community = vertex.community
            for neighbour in vertex.neighbours:
                community = graph.get_communities()[neighbour.community]
                sum_in = sigma_in(community)
                sum_tot = sigma_tot(community)
                ki = k_i(vertex)
                kin = k_i_in(vertex, community)

                # Formula from the paper to calculate the modularity gain of moving vertex to its
                # neighbours community
                delta_q = ((((sum_in + kin) / (2 * m)) - (((sum_tot + ki) / (2 * m)) ** 2)) -
                           ((sum_in / (2 * m)) - ((sum_tot / (2 * m)) ** 2) - (ki / (2 * m)) ** 2))

                if max_q < delta_q and len(community[0]) < 50:
                    max_q = delta_q
                    best_community = neighbour.community

            # If modularity gain is greater than 0, reassign communities
            if max_q > 0:
                neighbour_community = graph.get_communities()[best_community]
                old_community = graph.get_communities()[vertex.community]
                best_k_i_in = k_i_in(vertex, neighbour_community)
                best_k_i_out = k_i_out(vertex, old_community)
                graph.change_communities(vertex, best_community, best_k_i_in, best_k_i_out)
                vertex.community = best_community


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['movie_class'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
