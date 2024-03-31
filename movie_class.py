"""CSC111 Project 2: Netflix Movie Recommendation System

This is the graph implementation file of the Netflix Movie Recommendation System created by Saahil Kapasi,
Andrew Sasmito, Fiona Verzivolli, and Naoroj Farhan to be submitted for the second CSC111 Project.
"""
from __future__ import annotations
import csv


class Movie:
    """A vertex in a weighted movie network graph, used to represent a movie.

    Each vertex item is a movie title and is represented by a string.

    Instance Attributes:
        - title: The data stored in this vertex, which is a movie title.
        - neighbours: The vertices that are adjacent to this vertex and
            their corresponding edge weights.
        - community: A value used to group this movie into a group of similar movies.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    title: str
    neighbours: dict[Movie, int | float]
    community: str

    def __init__(self, title: str):
        """Initialize a new movie vertex with the given title, and with
        its community being set to the title to start.

        The vertex is initialized with no neighbours to start.
        """
        self.title = title
        self.neighbours = {}
        self.community = title

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)


class Network:
    """An implementation of a movie network graph.

    Private Instance Attributes:
        - s: A collection of the vertices contained in this graph,
            maps a movie title to a _Movie object.
        - _community: A collection of vertices within a given community
    """
    _movies: dict[str, Movie]
    _communities: dict[str, tuple[set[Movie], float]]  # CHANGED TYPE TO tuple[set[vertices], numedges in community]

    # TODO: DO WE NEED TO KNOW WHAT THE EDGES IN THE SUBGRAPH ARE (EXTRA MEMORY), OR IS KNOWING THE NUMBER AND
    # TODO: INCREMENTING SUFFICIENT?

    def __init__(self) -> None:
        """Initialize an empty network graph (no vertices or edges)."""
        self._movies = {}
        self._communities = {}

    def add_movie(self, title: str) -> None:
        """Add a movie vertex with the given item to this graph and
        assign it to its own community.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
        """
        if title not in self._movies:
            self._movies[title] = Movie(title)
            self._communities[title] = ({self._movies[title]}, 0)

            # Reasoning: Since each vertex begins in its own community, the subgraph has only that vertex and
            # 0 edges initially

    def add_edge(self, title1: str, title2: str, weight: int | float = 0) -> None:
        """Add an edge between the two movies with the given titles in this graph,
        with the given weight.

        Do nothing if there is already an edge between the two movies.

        Raise a ValueError if item1 or item2 do not appear as movies in this graph.

        Preconditions:
            - item1 != item2
        """
        if title1 in self._movies and title2 in self._movies:
            if self._movies[title2] in self.get_neighbours(title1): # if the edge exists, do nothing, nice Andrew
                return

            m1 = self._movies[title1]
            m2 = self._movies[title2]

            # Add the new edge
            m1.neighbours[m2] = weight
            m2.neighbours[m1] = weight
        else:
            # We didn't find an existing movie for both items.
            raise ValueError

    def remove_edge(self, title1: str, title2: str) -> None:
        """Remove an edge between the two movies with the given titles in this graph.

        Raise a ValueError if item1 or item2 do not appear as movies in this graph.
        Assumes if they are neigbhours, then m2 in m1.neighbours and m1 in m2.neighbours
        Preconditions:
            - item1 != item2
            - m1 and m2 are in self._movies
            - an edge exists between the two movies
        """
        m1 = self._movies[title1]
        m2 = self._movies[title2]
        # Add the new edge
        m1.neighbours.pop(m2)
        m2.neighbours.pop(m1)

    def increment_edge(self, title1: str, title2: str, weight: float) -> None:
        """Increment the edge weight between the two movies with the given titles in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as movies in this graph.

        Preconditions:
            - item1 != item2
        """
        if title1 in self._movies and title2 in self._movies:
            m1 = self._movies[title1]
            m2 = self._movies[title2]

            # Increment the new edge
            m1.neighbours[m2] += weight
            m2.neighbours[m1] += weight
        else:
            # We didn't find an existing movie for both items.
            raise ValueError

    def get_weight(self, title1: str, title2: str) -> int | float:
        """Return the weight of the edge between the given movies.

        Return 0 if item1 and item2 are not adjacent.

        Preconditions:
            - item1 and item2 are vertices in this graph
        """
        m1 = self._movies[title1]
        m2 = self._movies[title2]
        return m1.neighbours.get(m2, 0)

    def get_movies(self) -> dict[str, Movie]:
        """Return the movies (vertices) that belong to the graph. We need a method since _movies
        is a protected class"""
        return self._movies
        # TODO: SHOULD WE RETURN SELF.MOVIES.COPY()?? EXTRA SPACE COMPLEXITY BUT MAYBE UEFUL IDK

    def get_communities(self) -> dict[str, tuple[set[Movie], float]]:
        """Return the communities found in the graph"""
        return self._communities

    def change_communities(self, vertex: Movie, new_community: str, add_density: float, rem_density: float) -> None:
        """Move a movie to its neighbours community when it improves density"""
        self._communities[vertex.community][0].remove(vertex)
        self._communities[vertex.community][1] -= rem_density
        self._communities[new_community][0].add(vertex)
        self._communities[new_community][1] += add_density

    def remove_empty_communities(self) -> None:
        """Get rid of communities without any members"""
        for community in self._communities:
            if len(self._communities[community][0]) == 0:
                del self._communities[community]

    def adjacent(self, title1: str, title2: str) -> bool:
        """Return whether item1 and item2 are adjacent movies in this graph.

        Return False if item1 or item2 do not appear as movies in this graph.
        """
        if title1 in self._movies and title2 in self._movies:
            m1 = self._movies[title1]
            return any(m2.title == title2 for m2 in m1.neighbours)
        else:
            return False

    def get_neighbours(self, title: str) -> set:
        """Return a set of the neighbours of the given movie.

        Note that the *titles* are returned, not the _Movie objects themselves.

        Raise a ValueError if title does not appear as a movie in this graph.
        """
        if title in self._movies:
            m = self._movies[title]
            return {neighbour.title for neighbour in m.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self) -> set:
        """Return a set of all movies in this graph."""
        return set(self._movies.keys())
