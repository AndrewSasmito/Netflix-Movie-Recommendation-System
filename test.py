import clustering
import movie_class
import load_graph

if __name__ == '__main__':
    g = load_graph.load_movie_graph('data/shuffled_user_ratings.csv', 'data/movies.csv')
    print(g._movies)
    clustering.louvain(g, 3)
    print(g._communities)

    for x in g._communities:
        print(len(g._communities[x][0]),g._communities[x][0])
# recommendations = g.get_best_movies([g._movies["My Mother Likes Women"]], 10)

# print(recommendations)
