"""TODO: EMPTY DOCSTRING"""

import movie_class
import networkx as nx
import matplotlib.pyplot as plt
import load_graph

def sigma_in(community: list[set[movie_class.Movie] | float]):
    """TODO: Docstring for """
    return community[1]


def sigma_tot(community: list[set[movie_class.Movie] | float]) -> float:
    incident_edges = 0
    for vertex in community[0]:
        incident_edges += vertex.sum_weights
    return incident_edges / 2  # TODO divide by 2 bc overcounting?


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
                sum_in = sigma_in(community)
                sum_tot = sigma_tot(community)
                ki = k_i(vertex)
                kin = k_i_in(vertex, community)
                # print(sum_in, sum_tot)

                delta_q = (((sum_in + kin) / (2 * m)) - (((sum_tot + ki) / (2 * m)) ** 2)) - (
                            (sum_in / (2 * m)) - ((sum_tot / (2 * m)) ** 2) - (ki / (2 * m)) ** 2)
                # print(delta_q)
                if max_q < delta_q:
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


# g = load_graph.load_movie_graph('data/Netflix_User_Ratings.csv', 'data/movies.csv')
# TEST GRAPH 1:
# g = movie_class.Network()
# G = nx.Graph()
# for i in range(6):
#     g.add_movie(str(i))
#     G.add_node(str(i))
#
# for i in range(0, 3):
#     for j in range(i + 1, 3):
#         g.add_edge(str(i), str(j), 1)
#         G.add_edge(str(i), str(j))
# for i in range(3, 6):
#     for j in range(i + 1, 6):
#         g.add_edge(str(i), str(j), 1)
#         G.add_edge(str(i), str(j))
#
# g.add_edge('4', '2', 1)
# G.add_edge('4', '2')
#
# g.add_sum_of_weights()
# pos = nx.spring_layout(G)
# nx.draw(G, pos, with_labels=True)
# plt.show()

# TEST GRAPH 2:
# g = movie_class.Network()
# G = nx.Graph()
# for i in range(7):
#     g.add_movie(str(i))
#     G.add_node(str(i))
#
# g.add_edge('0', '1', 1)
# g.add_edge('0', '2', 1)
# g.add_edge('2', '1', 1)
# g.add_edge('2', '3', 1)
#
# g.add_sum_of_weights()
#
# G.add_edge('0', '1')
# G.add_edge('0', '2')
# G.add_edge('2', '1')
# G.add_edge('2', '3')
# pos = nx.spring_layout(G)
# for i in range(3, 7):
#     for j in range(i + 1, 7):
#         g.add_edge(str(i), str(j), 1)
#         G.add_edge(str(i), str(j))
# # pos = nx.spring_layout(G)
# nx.draw(G, pos, with_labels = True)
# plt.show()
#
#
# louvain(g, 10)
#
# print(g._communities)
#
# for u in g._communities:
#     if len(g._communities[u][0]) > 0:
#         ans = ''
#         for v in g._communities[u][0]:
#             ans += v.title + ', '
#         print(len(g._communities[u][0]), 'title: ', u, ' ', ans)
#         # print(len(g._communities[u][0]), g._communities[u][0])
