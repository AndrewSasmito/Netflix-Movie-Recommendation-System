"""TODO: EMPTY DOCSTRING"""

import movie_class
def density(graph: movie_class.Network, community_name: str) -> float:
    """Return the density of the community"""
    # TODO: MOVE THIS FUNCTION TO THE CLUSTERING FILE??
    movie_community = graph.get_communities()[community_name]
    vertices = len(movie_community[0])  # total number of vertices in community, used to calculate max edges
    edges = (movie_community[1])  # number of edges in community

    return (2 * edges) / (vertices * (vertices - 1))

    # movie_community = self._communities[community_name][0]  # this is the set of all vertices in subgraph
    # density = 0
    #
    # _communities: dict[str, tuple[set[_Movie], int]]
    #
    # for u in movie_community:
    #     for v in movie_community:
    #         if u in v.neighbours:
    #             density += u.neighbours[v]
    #
    # return 2 * density / (len(self._movies.keys()) * (len(self._movies.keys()) - 1))
