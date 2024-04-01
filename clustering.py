"""TODO: EMPTY DOCSTRING"""

import movie_class
import load_graph
import networkx as nx
import matplotlib.pyplot as plt

def Σ_in(community: list[set[movie_class.Movie] | float]):
    """TODO: Docstring for """
    return community[1]

def Σ_tot(community: list[set[movie_class.Movie] | float]) -> float:
    incident_edges = 0
    for vertex in community[0]:
        incident_edges += vertex.sum_weights
    return incident_edges / 2 # TODO divide by 2 bc overcounting?

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
            max_Q = 0
            best_community = vertex.community
            for neighbour in vertex.neighbours:
                print(vertex_name, neighbour.title)
                community = graph.get_communities()[neighbour.community]
                sum_in = Σ_in(community)
                sum_tot = Σ_tot(community)
                ki = k_i(vertex)
                kin = k_i_in(vertex, community)
                # print(sum_in, sum_tot)

                deltaQ = (((sum_in + kin) / (2 * m)) - (((sum_tot + ki) / (2 * m)) ** 2)) - ((sum_in / (2 * m)) - ((sum_tot / (2 * m)) ** 2) - (ki / (2 * m)) ** 2)
                # print(deltaQ)
                if max_Q < deltaQ:
                    max_Q = deltaQ
                    best_community = neighbour.community

            if max_Q > 0:
                neighbour_community = graph.get_communities()[best_community]
                old_community = graph.get_communities()[vertex.community]
                best_k_i_in = k_i_in(vertex, neighbour_community)
                best_k_i_out = k_i_out(vertex, old_community)
                graph.change_communities(vertex, best_community, best_k_i_in, best_k_i_out)
                vertex.community = best_community
                # print(graph.get_communities())


# TEST GRAPH 1:
g = movie_class.Network()
G = nx.Graph()
for i in range(6):
    g.add_movie(str(i))
    G.add_node(str(i))

for i in range(0, 3):
    for j in range(i + 1, 3):
        g.add_edge(str(i), str(j), 1)
        G.add_edge(str(i), str(j))
for i in range(3, 6):
    for j in range(i + 1, 6):
        g.add_edge(str(i), str(j), 1)
        G.add_edge(str(i), str(j))

g.add_edge('4', '2', 1)
G.add_edge('4', '2')

g.add_sum_of_weights()
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
plt.show()

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
louvain(g, 10)

print(g._communities)

for u in g._communities:
    if len(g._communities[u][0]) > 0:
        ans = ''
        for v in g._communities[u][0]:
            ans += v.title + ', '
        print(len(g._communities[u][0]), 'title: ', u,' ', ans)
        # print(len(g._communities[u][0]), g._communities[u][0])




# def community_density(edge: float, vertices: int) -> float:
#     """Return the density of the community"""
#     if vertices <= 1:
#         return 0
#     else:
#         return (2 * edge) / (vertices * (vertices - 1))
#
#
# def added_weight(new_vertex: movie_class.Movie, community: list[set[movie_class.Movie] | float]) -> float:
#     """Return the weighted sum of the edges that the vertex is connected to in the community proposed for a merge
#     O(N) algorithm wher N is the number of vertices"""
#     community_vertices = community[0]
#     added_weight = 0
#     for vertex in community_vertices:
#         if vertex in new_vertex.neighbours:
#             added_weight += new_vertex.neighbours[vertex]
#
#     return added_weight
#
#
# def removed_weight(removed_vertex: movie_class.Movie, community: list[set[movie_class.Movie] | float]) -> float:
#     """Return the weighted sum of edges removed when a vertex leaves it original community"""
#     community_vertices = community[0]
#     removed_weight = 0
#     for vertex in community_vertices:
#         if vertex in removed_vertex.neighbours:
#             removed_weight += removed_vertex.neighbours[vertex]
#     return removed_weight
#
#
# def community_detection(graph: movie_class.Network, epochs: int) -> None:
#     """Cluster the graph into communities, greedily maximizing the density of each community"""
#
#     for _ in range(epochs):
#         # print("test epochs")
#         # vertex_count = 1
#         for vertex_name in graph.get_movies():
#             vertex = graph.get_movies()[vertex_name]
#             # print(vertex_name)
#
#             max_density_increase = 0
#             weight_add_best = 0
#             weight_rem_best = 0
#             size_tiebreaker = len(graph.get_communities()[vertex.community][0])
#             # print('size', size_tiebreaker)
#             best_community = vertex.community
#             # print(f'the initial community of {vertex.title} is: {best_community}')
#
#             for neighbour in vertex.neighbours:
#
#                 print(vertex.title, ' ', neighbour.title)
#                 if vertex.community == neighbour.community:
#                     # Case when vertex is moved to its own community, do nothing
#                     continue
#
#                 original_community = graph.get_communities()[vertex.community]
#                 neighbour_community = graph.get_communities()[neighbour.community]
#
#                 initial_density_original = community_density(original_community[1], len(original_community[0]))
#                 initial_density_neighbour = community_density(neighbour_community[1], len(neighbour_community[0]))
#
#                 print('initial: orig/neigh', initial_density_original, initial_density_neighbour)
#
#                 added_edge_weight = added_weight(vertex, neighbour_community)
#                 rem_edge_weight = removed_weight(vertex, original_community)
#
#                 new_density_original = community_density(original_community[1] - rem_edge_weight, len(original_community[0]) - 1)
#                 new_density_neighbour = community_density(neighbour_community[1] + added_edge_weight, len(neighbour_community[0]) + 1)
#
#                 print('new: orig/neigh if moved to: ', neighbour.community, '|', new_density_original, new_density_neighbour)
#
#                 density_change = (new_density_neighbour - initial_density_neighbour) + (new_density_original - initial_density_original)
#
#                 if density_change > max_density_increase:
#                     # TODO: break ties based on the size of the community
#                     # print('I in here', density_change)
#                     max_density_increase = density_change
#                     weight_add_best = added_edge_weight
#                     weight_rem_best = rem_edge_weight
#                     best_community = neighbour.community
#                     size_tiebreaker = len(neighbour_community[0]) + 1
#                 elif density_change == max_density_increase and len(neighbour_community[0]) > size_tiebreaker:
#                     print('edge case')
#                     max_density_increase = density_change
#                     weight_add_best = added_edge_weight
#                     weight_rem_best = rem_edge_weight
#                     best_community = neighbour.community
#                     size_tiebreaker = len(neighbour_community[0]) + 1
#
#                 elif density_change == 0 and len(neighbour_community[0]) > size_tiebreaker:
#                     print('lol',len(neighbour_community[0]), size_tiebreaker)
#                     max_density_increase = density_change
#                     weight_add_best = added_edge_weight
#                     weight_rem_best = rem_edge_weight
#                     best_community = neighbour.community
#                     size_tiebreaker = len(neighbour_community[0]) + 1
#
#             if max_density_increase >= 0 and vertex.community != best_community:
#                 # remove vertex from old community and place it into new community
#                 graph.change_communities(vertex, best_community, weight_add_best, weight_rem_best)
#                 vertex.community = best_community
#                 print(
#                     f'{vertex.title} is moved to the community of {best_community} and max density change is: {max_density_increase}')
#
#         # graph.remove_empty_communities()


# g = load_graph.load_movie_graph('data/Netflix_User_Ratings.csv', 'data/movies.csv')
# community_detection(g, 3)
#
# # community_detection(g, 3)
#
# print(g._communities)
#
# for u in g._communities:
#     if len(g._communities[u][0]) > 0:
#         ans = ''
#         # for v in g._communities[u][0]:
#         #     ans += v.title + ', '
#         print(len(g._communities[u][0]))
#         # print(len(g._communities[u][0]), g._communities[u][0])



# # TEST GRAPH
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
'''
community_detection(g, 3)

print(g._communities)

for u in g._communities:
    if len(g._communities[u][0]) > 0:
        ans = ''
        for v in g._communities[u][0]:
            ans += v.title + ', '
        print(len(g._communities[u][0]), 'title: ', u,' ', ans)
        # print(len(g._communities[u][0]), g._communities[u][0])
'''
