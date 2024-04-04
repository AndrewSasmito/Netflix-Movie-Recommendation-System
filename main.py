"""CSC111 Project 2: Netflix Movie Recommendation System

This is the main file of the Netflix Movie Recommendation System created by Saahil Kapasi, Andrew Sasmito,
Fiona Verzivolli, and Naoroj Farhan to be submitted for the second CSC111 Project.
"""
from load_graph import load_movie_graph
from clustering import louvain
import tkinter as tk
from front import TkinterApp


if __name__ == "__main__":
    graph = load_movie_graph('data/shuffled_user_ratings.csv', 'data/movies.csv')
    louvain(graph, 3)
    app = TkinterApp(tk.Tk(), 'data/movies.csv', graph)
    app.run()
