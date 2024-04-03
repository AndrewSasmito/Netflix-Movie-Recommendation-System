import csv
import tkinter as tk
from typing import Any
from tkinter import messagebox


class TkinterApp:
    """Class that stores all of our information for the frontend interface.
    This includes the initialization (creating our window and tkinter widgets), as
    well as the methods needed to make our frontend interactive."""

    selected_movies: set
    list_of_movies: list
    root: tk.Tk
    movies: tk.Listbox
    movie_entry: tk.Entry
    spinbox: tk.Spinbox
    selected_movies_listbox: tk.Listbox

    def __init__(self, window_root: tk.Tk, movies_file_path: str) -> None:
        """Function to create our user interface window. Includes all tkinter widgets."""
        self.selected_movies = set()
        self.list_of_movies = generate_movies(movies_file_path)
        self.root = window_root

        self.root.geometry("2560x1600")  # initialize window
        self.root.title("Project 2 Window")
        label = tk.Label(self.root, text="Movie Recommender", font=('Courier', 80))
        label.pack(padx=20, pady=20)
        label2 = tk.Label(self.root,
                          text="To begin, enter a movie you have watched or like, \nand your desired number of reviews",
                          font=('Courier', 25))
        label2.pack(padx=20, pady=10)

        movie_input1 = tk.Label(self.root, text="Selected Movies", font=('Courier', 20))
        movie_input1.pack()

        self.selected_movies_listbox = tk.Listbox(self.root, width=50, height=5)
        self.selected_movies_listbox.pack(pady=5)

        movie_input2 = tk.Label(self.root, text="Enter movie(s) by typing, click movie twice, and hit enter.",
                                font=('Courier', 20))
        movie_input2.pack(pady=5)

        self.movie_entry = tk.Entry(self.root, font=('Courier', 20))
        self.movie_entry.pack(pady=5)

        self.movies = tk.Listbox(self.root, width=50, height=5)
        self.movies.pack(pady=5)

        movie_input3 = tk.Label(self.root, text="Maximum number of recommendations (1-5)", font=('Courier', 20))
        movie_input3.pack(pady=5)

        self.spinbox = tk.Spinbox(self.root, from_=0, to=5)
        self.spinbox.pack(padx=20, pady=5)

        # update our box of selected movies to include the movie we are currently selecting in our selection box
        self.selected_movies_listbox.bind("<<ListboxSelect>>", self.update_selected_movies)

        button = tk.Button(self.root, text="Recommend", font=('Courier', 30), command=self.recommend_movies)
        button.pack()

        self.modify(self.list_of_movies)

        self.movies.bind("<<ListboxSelect>>", self.updater)  # create keybinds

    def updater(self, event: tk.Event) -> None:
        """Replace entered text with selected movie and store it.
        Raise an error if the user selected too many movies."""
        if len(self.selected_movies) >= 5:
            # error message
            tk.messagebox.showinfo("Limit Reached",
                                   "You can only select up to 5 movies. Press recommend and try again.")
            return

        movie_name = self.movies.get(tk.ACTIVE)  # get currently selected item
        self.movie_entry.delete(0, tk.END)  # delete all movies
        self.movie_entry.insert(0, movie_name)  # insert current movie to our entries
        self.selected_movies.add(movie_name)  # add selected movie to selected_movies
        self.update_selected_movies()  # update selected movies

    def modify(self, lst: list) -> Any:
        """Initially display all movie options in our dropdown menu"""
        self.movies.delete(0, tk.END)  # clear dropdown menu so it updates
        for movie in lst:
            self.movies.insert(tk.END, movie)  # add each movie

    def verify(self, event: tk.Event) -> Any:
        """Match the user's text to movie titles in our movies.csv file"""
        if self.movie_entry.get() != '':  # if there is text,
            lst = []
            for i in self.list_of_movies:
                if self.movie_entry.get().lower() in i.lower():
                    lst.append(i)  # add each corresponding movie to lst
            self.modify(lst)  # update

    def recommend_movies(self) -> None:
        """Function to update recommended movies when recommended is pressed
        and reset several visual elements, such as """
        self.movie_entry.delete(0, tk.END)  # clear search bar
        self.selected_movies_listbox.delete(0, tk.END)  # clear selected movies box
        self.selected_movies = set()  # empty selected movies set
        self.spinbox.delete(0, tk.END)  # clear number of reviews
        self.spinbox.insert(0, '0')

    def update_selected_movies(self, event: tk.Event = None) -> None:
        """Insert the movies the user selected to our box of selected movies"""
        self.selected_movies_listbox.delete(0, tk.END)  # clear our selected movies at first
        for movie in self.selected_movies:  # after clearing,
            self.selected_movies_listbox.insert(tk.END, movie)


def generate_movies(movies_file_path: str) -> list:
    """Function needed to store movies in a list for our search feature"""
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
- Fix select bug: half done
    each time you select a movie, it automatically selects the first movie in our entry box
    doesnt display selected movie in selected movies until you select another one
- Add comments: DONE
"""

root = tk.Tk()
app = TkinterApp(root, 'movies.csv')
app.root.mainloop()
