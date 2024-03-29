"""CSC111 Project 2: Netflix Movie Recommendation System

This is the graph implementation file of the Netflix Movie Recommendation System created by Saahil Kapasi,
Andrew Sasmito, Fiona Verzivolli, and Naoroj Farhan to be submitted for the second CSC111 Project.
"""
from __future__ import annotations
import csv

class _Movie:
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
    neighbours: dict[_Movie, int | float]
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
        - _movies: A collection of the vertices contained in this graph,
            maps a movie title to a _Movie object.
        - _community: A collection of vertices within a given community
    """
    _movies: dict[str, _Movie]
    _communities: dict[str, set[_Movie]]

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
            self._movies[title] = _Movie(title)
            self._communities[title] = {_Movie(title)}

    def add_edge(self, title1: str, title2: str, weight: int | float = 0) -> None:
        """Add an edge between the two movies with the given titles in this graph,
        with the given weight.

        Do nothing if there is already an edge between the two movies.

        Raise a ValueError if item1 or item2 do not appear as movies in this graph.

        Preconditions:
            - item1 != item2
        """
        if title1 in self._movies and title2 in self._movies:
            if self._movies[title2] in self.get_neighbours(title1):
                return

            m1 = self._movies[title1]
            m2 = self._movies[title2]

            # Add the new edge
            m1.neighbours[m2] = weight
            m2.neighbours[m1] = weight
        else:
            # We didn't find an existing movie for both items.
            raise ValueError

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

    def average_weight(self, title: str) -> float:
        """Return the average weight of the edges adjacent to the movie corresponding to title.

        Raise ValueError if title does not correspond to a movie in the graph.
        """
        if title in self._movies:
            v = self._movies[title]
            return sum(v.neighbours.values()) / len(v.neighbours)
        else:
            raise ValueError

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

    def density(self, community_name: str) -> float:
        """Return the density of the community"""
        movie_community = self._communities[community_name]
        density = 0

        for u in movie_community:
            for v in u.neighbours:
                density += u.neighbours[v]

        return 2 * density / (len(self._movies.keys()) * (len(self._movies.keys()) - 1))


def load_weighted_review_graph(reviews_file_path: str, movies_file_path: str) -> Network:
    """
    Load a weighted review_graph
    """
    graph = Network()
    with open(reviews_file_path, 'r') as reviews_file, open(movies_file_path, 'r') as movies_file:
        next(movies_file)
        movies_dict: dict[int, str] = {}
        for line in csv.reader(movies_file):
            movies_dict[int(line[0])] = line[2]
            graph.add_movie(movies_dict[int(line[0])])

        print("first")

        next(reviews_file)
        users = {}
        cnt1 = 0
        for line in csv.reader(reviews_file):
            customer, rating, date, movie = line
            if customer not in users:
                users[customer] = []
            if cnt1 % 10000000 == 0:
                print(f'cnt1: {cnt1}')
            cnt1 += 1
            users[customer].append((movies_dict[int(movie)], int(rating)))

        cnt = 0
        for user in users:
            rating_dictionary = users[user]
            for movie_index1 in range(len(rating_dictionary)):
                for movie_index2 in range(movie_index1 + 1, len(rating_dictionary)):
                    graph.add_edge(rating_dictionary[movie_index1][0], rating_dictionary[movie_index2][0])
                    graph.increment_edge(rating_dictionary[movie_index1][0], rating_dictionary[movie_index2][0], 1 - abs(rating_dictionary[movie_index1][1] - rating_dictionary[movie_index2][1]) / 5)
            if cnt % 10000 == 0:
                print(f'cnt: {cnt}')
            cnt += 1

    return graph
