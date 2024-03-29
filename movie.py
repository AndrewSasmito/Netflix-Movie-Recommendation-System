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
    _communities: dict[str, tuple[set[_Movie], int]]  # CHANGED TYPE TO tuple[set[vertices], numedges in community]

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
            self._movies[title] = _Movie(title)
            self._communities[title] = ({_Movie(title)}, 0)

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

    def average_weight(self, title: str) -> float:
        """Return the average weight of the edges adjacent to the movie corresponding to title.
        TODO: IS THIS FUNCTION USEFUL??
        Raise ValueError if title does not correspond to a movie in the graph.
        """
        if title in self._movies:
            v = self._movies[title]
            return sum(v.neighbours.values()) / len(v.neighbours)
        else:
            raise ValueError

    def get_movies(self) -> dict[str, _Movie]:
        """Return the movies (vertices) that belong to the graph. We need a method since _movies
        is a protected class"""
        return self._movies
        # TODO: SHOULD WE RETURN SELF.MOVIES.COPY()?? EXTRA SPACE COMPLEXITY BUT MAYBE UEFUL IDK

    def get_communities(self) -> dict[str, tuple[set[_Movie], int]]:
        """Return the communities found in the graph"""
        return self._communities

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


def determine_edge_weight(rating1: int | float, rating2: int | float) -> float:
    """Determine the edge weight to increment the weight between movies by. The idea is that if a given user
    gives a pair of movies the exact same rating, the 'correlation' between the movies is exact and we increment
    edge weight by 1. If a user rates a movie 5 stars and another movie 0 stars, increment the weight by 0
    The below formula captures this premise"""

    return 1 - abs(rating1 - rating2) / 5


def load_weighted_review_graph(reviews_file_path: str, movies_file_path: str) -> Network:
    """
    Load a weighted review_graph
    TODO: SHOULD WE MOVE THIS INTO A FILE EXPLICITLY FOR LOADING DATA SINCE ITS A FUNCTION ANYWAYS??
    """
    graph = Network()   # creates a new empty graph

    # NOTE: our objective is to make a graph of the first 1000 movies for easier computation later on

    with open(reviews_file_path, 'r') as reviews_file, open(movies_file_path, 'r') as movies_file:

        next(movies_file)               # skips first row because it is a header
        movies_dict: dict[int, str] = {}    # mapping of movieid (1-17700) to the movie_name (string)
        movie_counter = 0
        for line in csv.reader(movies_file):            # NOTE: iterates 1000 times, seems fine with O(N)
            movies_dict[int(line[0])] = line[2]
            graph.add_movie(movies_dict[int(line[0])])
            movie_counter += 1
            if movie_counter == 1000:
                break

        # print(graph.get_movies())

        # NOTE: at this point, our graph has 1000 movie vertices, we now move on to the phase where we generate edges

        print("first")

        # print(movies_dict)

        next(reviews_file)  # skips first row because its a header

        user_ratings = {}      # users represents: dict[userid, list[movies watched]]
        rating_counter = 0      # want to get 1,000,000 valid ratings with O(N) algorithm, seems fine
        for line in csv.reader(reviews_file):
            #   int (custid),rating(1-5),date, int( movieid)

            customer, rating, _, movie = line   # replaced date with _ since we don't use it anyways

            if int(movie) not in movies_dict:  # if the user rates a movie we don't consider
                # print('asdfjklkj')
                pass
            else:

                if customer not in user_ratings:   # if we haven't seen this customer before, add them to dictionary
                    user_ratings[customer] = []

                # if cnt1 % 10000000 == 0:
                #     print(f'cnt1: {cnt1}')
                # cnt1 += 1
                user_ratings[customer].append((movies_dict[int(movie)], int(rating)))  # adding tuple of (movie, rating)
                rating_counter += 1

                # if rating_counter % 10000 == 0:
                #     print(f'cnt: {rating_counter}')

                if rating_counter == 1000000:
                    break
        print('second')

        cnt = 0
        # if ~500,000 users, 2 ratings per user, 2 x 10^ 6. If 1 user, 1,000,000 per user (impossible if we assume
        # each user rates a movie either 0 or 1 times. # 1000 users, 1000 ratings per user, 1x10^9
        for user in user_ratings:                       # upto 480,000 users 4.8 x 10^6
            movies_rated = user_ratings[user]

            # The goal is to determine a relationship between every pair of movies that a given user rates
            for i1 in range(len(movies_rated)):              # upto 10^3
                for i2 in range(i1 + 1, len(movies_rated)):  # upto 10^3
                    movie1, movie2 = movies_rated[i1][0], movies_rated[i2][0]
                    weight = determine_edge_weight(movies_rated[i1][1], movies_rated[i2][1])

                    if weight > 0 and graph.adjacent(movie1, movie2):
                        graph.increment_edge(movie1, movie2, weight)
                    elif weight > 0:
                        graph.add_edge(movie1, movie2, weight)
                    # graph.increment_edge(movie1, movie2, weight)
                    # if graph.get_weight(movie1, movie2) == 0:   # ensures there are no edges with 0 weight
                    #     graph.remove_edge(movie1, movie2)
            if cnt % 10000 == 0:
                print(f'cnt: {cnt}')
            cnt += 1

    return graph
