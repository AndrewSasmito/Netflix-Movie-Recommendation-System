"""TODO: EMPTY DOCSTRING"""

import movie_class
import load_graph
import networkx as nx
import matplotlib.pyplot as plt


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


def added_weight(new_vertex: movie_class.Movie, community: list[set[movie_class.Movie] | float]) -> float:
    """Return the weighted sum of the edges that the vertex is connected to in the community proposed for a merge
    O(N) algorithm wher N is the number of vertices"""
    community_vertices = community[0]
    print('testing', community[1])
    # print(community_vertices)
    added_weight = 0
    for vertex in community_vertices:
        if vertex in new_vertex.neighbours:

            added_weight += new_vertex.neighbours[vertex]

    return community[1] + added_weight


def removed_weight(removed_vertex: movie_class.Movie, community: list[set[movie_class.Movie] | float]) -> float:
    """Return the weighted sum of edges removed when a vertex leaves it original community"""
    community_vertices = community[0]
    removed_weight = 0
    for vertex in community_vertices:
        if vertex in removed_vertex.neighbours:
            removed_weight += removed_vertex.neighbours[vertex]

    return community[1] - removed_weight


def community_detection(graph: movie_class.Network, epochs: int) -> None:
    """Cluster the graph into communities, greedily maximizing the density of each community"""

    for _ in range(epochs):
        # print("test epochs")
        # vertex_count = 1
        for vertex_name in graph.get_movies():
            vertex = graph.get_movies()[vertex_name]
            print(vertex_name)

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

                print(density_add, ' ', density_rem)
                density_change = density_add - density_rem
                # if density_change > 0:
                #     print('hello world')
                if density_change > max_density_increase:
                    max_density_increase = density_change
                    density_add_best = density_add
                    density_rem_best = density_rem
                    best_community = neighbour.community
            # vertex_count += 1
            if max_density_increase > 0:
                # remove vertex from old community and place it into new community
                graph.change_communities(vertex, best_community, density_add_best, density_rem_best)
                vertex.community = best_community

        # graph.remove_empty_communities()


# g = load_graph.load_movie_graph('data/Netflix_User_Ratings.csv', 'data/movies.csv')
# community_detection(g, 10)


# TEST GRAPH
g = movie_class.Network()
G = nx.Graph()
for i in range(7):
    g.add_movie(str(i))
    G.add_node(str(i))

g.add_edge('0', '1', 1)
g.add_edge('0', '2', 1)
g.add_edge('2', '1', 1)
g.add_edge('2', '3', 1)

G.add_edge('0', '1')
G.add_edge('0', '2')
G.add_edge('2', '1')
G.add_edge('2', '3')
pos = nx.spring_layout(G)
for i in range(3, 7):
    for j in range(i + 1, 7):
        g.add_edge(str(i), str(j), 1)
        G.add_edge(str(i), str(j))
# pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels = True)
plt.show()

community_detection(g, 3)

print(g._communities)

for u in g._communities:
    if len(g._communities[u][0]) > 0:
        print(len(g._communities[u][0]), g._communities[u][0])
