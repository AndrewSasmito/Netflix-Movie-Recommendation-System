"""This file is responsible for loading in the graph that we use"""

import csv
import movie_class

# TODO: took 10 off


def determine_edge_weight(rating1: int | float, rating2: int | float) -> float:
    """Determine the edge weight to increment the weight between movies by. The idea is that if a given user
    gives a pair of movies the exact same rating, the 'correlation' between the movies is exact and we increment
    edge weight by 1. If a user rates a movie 5 stars and another movie 0 stars, increment the weight by 0
    The below formula captures this premise"""
    return 1 - abs(rating1 - rating2) / 5


def load_movie_graph(reviews_file_path: str, movies_file_path: str) -> movie_class.Network:
    """
    Load a weighted review_graph
    """
    graph = movie_class.Network()   # creates a new empty graph

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

        # NOTE: at this point, our graph has 1000 movie vertices, we now move on to the phase where we generate edges

        # next(reviews_file)  # skips first row because its a header

        user_ratings = {}      # users represents: dict[userid, list[movies watched]]
        rating_counter = 0      # want to get 1,000,000 valid ratings with O(N) algorithm, seems fine
        for line in csv.reader(reviews_file):
            #   int (custid),rating(1-5),date, int( movieid)
            # print(line)
            customer, rating, _, movie = line   # replaced date with _ since we don't use it anyways

            if int(movie) not in movies_dict:  # if the user rates a movie we don't consider
                pass
            else:

                if customer not in user_ratings:   # if we haven't seen this customer before, add them to dictionary
                    user_ratings[customer] = []

                user_ratings[customer].append((movies_dict[int(movie)], int(rating)))  # adding tuple of (movie, rating)
                rating_counter += 1

                # if rating_counter % 10000 == 0:
                #     print(f'cnt: {rating_counter}')

                if rating_counter == 1000000:
                    break
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

    graph.add_sum_of_weights()

    return graph
