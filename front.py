import tkinter as tk
from typing import Any
import csv


class TkinterApp:
    selected_movies: set
    list_of_movies: list
    root: tk.Tk
    movies: tk.Listbox
    movie_entry: tk.Entry
    spinbox: tk.Spinbox
    selected_movies_listbox: tk.Listbox

    def __init__(self, root: tk.Tk, movies_file_path: str) -> None:
        self.selected_movies = set()
        self.list_of_movies = generate_movies(movies_file_path)
        self.root = root

        self.root.geometry("2560x1600")
        self.root.title("Project 2 Window")
        label = tk.Label(self.root, text="Movie Recommender", font=('Arial', 80))
        label.pack(padx=20, pady=20)
        label2 = tk.Label(self.root,
                          text="To begin, enter a movie you have watched or like, \nand your desired number of reviews",
                          font=('Arial', 25))
        label2.pack(padx=20, pady=10)

        movie_input1 = tk.Label(self.root, text="Selected Movies", font=('Arial', 20))
        movie_input1.pack()

        self.selected_movies_listbox = tk.Listbox(self.root, width=50, height=5)
        self.selected_movies_listbox.pack(pady=5)

        movie_input2 = tk.Label(self.root, text="Enter movie(s) by typing, select movie, and hit enter.", font=('Arial', 20))
        movie_input2.pack(pady=5)

        self.movie_entry = tk.Entry(self.root, font=('Arial', 20))
        self.movie_entry.pack(pady=5)

        self.movies = tk.Listbox(self.root, width=50, height=5)
        self.movies.pack(pady=5)

        movie_input3 = tk.Label(self.root, text="Maximum number of recommendations", font=('Arial', 20))
        movie_input3.pack(pady=5)

        self.spinbox = tk.Spinbox(self.root, from_=0, to=5)
        self.spinbox.pack(padx=20, pady=5)

        self.selected_movies_listbox.bind("<<ListboxSelect>>", self.update_selected_movies)

        button = tk.Button(self.root, text="Recommend", font=('Arial', 30), command=self.recommend_movies)
        button.pack()

        self.modify(self.list_of_movies)

        self.movies.bind("<<ListboxSelect>>", self.updater)
        self.movie_entry.bind("<ButtonRelease>", self.verify)

    def updater(self, event: tk.Event) -> None:
        """Replace entry content with selected movie and store it"""
        if len(self.selected_movies) >= 5:
            # error message
            tk.messagebox.showinfo("Limit Reached",
                                   "You can only select up to 5 movies. Press recommend and try again.")
            return

        movie_name = self.movies.get(tk.ACTIVE)
        self.movie_entry.delete(0, tk.END)
        self.movie_entry.insert(tk.END, movie_name)
        self.selected_movies.add(movie_name)
        self.update_selected_movies()

    def modify(self, lst: list) -> Any:
        """Initially display all movie options"""
        self.movies.delete(0, tk.END)
        for movie in lst:
            self.movies.insert(tk.END, movie)

    def verify(self, event: tk.Event) -> Any:
        """Match the user's text to possible movie titles"""
        if self.movie_entry.get() == '':
            lst = self.list_of_movies
        else:
            lst = []
            for i in self.list_of_movies:
                if self.movie_entry.get().lower() in i.lower():
                    lst.append(i)
        self.modify(lst)

    def recommend_movies(self) -> None:
        """Function to update recommended movies when recommended is pressed"""
        self.movie_entry.delete(0, tk.END)
        self.selected_movies = set()
        self.spinbox.delete(0, tk.END)
        self.spinbox.insert(0, '0')

    def update_selected_movies(self, event: tk.Event = None) -> None:
        """Insert the movies the user selected to our box of selected movies"""
        self.selected_movies_listbox.delete(0, tk.END)
        for movie in self.selected_movies:
            self.selected_movies_listbox.insert(tk.END, movie)

    def add_movie(self):
        """TODO: Complete docstring"""
        self.selected_movies.add("Selected Movie")
        self.update_selected_movies()


def generate_movies(movies_file_path: str) -> list:
    """Function needed to store movies in a list"""
    movie_lst = []
    with open(movies_file_path, 'r') as movies_file:
        for line in csv.reader(movies_file):
            movie_lst += [line[2]]
    movie_lst.pop(0)  # remove first MovieTitle
    return movie_lst


"""
TODO:
- Fix search: in progress
- Fix movietitle: DONE
- Fix select bug: in progress
    each time you select a movie, it automatically selects the first movie in our entry box
    doesnt display selected movie in selected movies until you select another one
- Add comments: in progress
"""