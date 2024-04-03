import tkinter as tk
import csv

from typing import Any
from tkinter import Label, Entry, Listbox, END, messagebox

"""
TODO:
- Fix search: in progress
- Fix movietitle: DONE
- Fix select bug: in progress
    each time you select a movie, it automatically selects the first movie in our entry box
    doesnt display selected movie in selected movies until you select another one
- Add comments: in progress
"""

selected_movies = set()  # store the movies we are working with


def updater(event):
    """Replace entry content with selected movie and store it"""
    if len(selected_movies) >= 5:
        # error message
        tk.messagebox.showinfo("Limit Reached",
                               "You can only select up to 5 movies. Press recommend and try again.")
        return

    movie_name = movies.get(tk.ACTIVE)
    movie_entry.delete(0, tk.END)
    movie_entry.insert(tk.END, movie_name)
    selected_movies.add(movie_name)
    update_selected_movies()


def modify(lst) -> Any:
    """Initially display all movie options"""
    movies.delete(0, END)
    for movie in lst:
        movies.insert(END, movie)


def generate_movies(movies_file: str) -> list:
    """Function needed to store movies in a list"""
    movie_lst = []
    for line in csv.reader(open(movies_file, 'r')):
        movie_lst += [line[2]]
    item = movie_lst.pop(0)  # remove first MovieTitle
    return movie_lst


def verify(event) -> Any:
    """Match the user's text to possible movie titles"""
    if movie_entry.get() == '':
        lst = list_of_movies
    else:
        lst = []
        for i in list_of_movies:
            if movie_entry.get().lower() in i.lower():
                lst.append(i)
    modify(lst)


def recommend_movies():
    """Function to update recommended movies when recommended is pressed"""
    global selected_movies
    movie_entry.delete(0, tk.END)
    selected_movies = set()
    spinbox.delete(0, tk.END)
    spinbox.insert(0, '0')


def update_selected_movies(event=None):
    """Insert the movies the user selected to our box of selected movies"""
    global selected_movies
    selected_movies_listbox.delete(0, tk.END)
    for movie in selected_movies:
        selected_movies_listbox.insert(tk.END, movie)


def add_movie():
    """TODO: Complete docstring"""
    global selected_movies
    selected_movies.add("Selected Movie")
    update_selected_movies()


if __name__ == '__main__':
    root = tk.Tk()

    list_of_movies = generate_movies('movies.csv')

    root.geometry("2560x1600")
    root.title("Project 2 Window")
    label = tk.Label(root, text="Movie Recommender", font=('Arial', 80))
    label.pack(padx=20, pady=20)
    label2 = tk.Label(root,
                      text="To begin, enter a movie you have watched or like, \nand your desired number of reviews",
                      font=('Arial', 25))
    label2.pack(padx=20, pady=10)

    movie_input1 = Label(root, text="Selected Movies", font=('Arial', 20))
    movie_input1.pack()

    selected_movies_listbox = tk.Listbox(root, width=50, height=5)
    selected_movies_listbox.pack(pady=5)

    movie_input2 = Label(root, text="Enter movie(s) by typing, select movie, and hit enter.", font=('Arial', 20))
    movie_input2.pack(pady=5)

    movie_entry = Entry(root, font=('Arial', 20))
    movie_entry.pack(pady=5)

    movies = Listbox(root, width=50, height=5)
    movies.pack(pady=5)

    movie_input3 = Label(root, text="Maximum number of recommendations", font=('Arial', 20))
    movie_input3.pack(pady=5)

    spinbox = tk.Spinbox(root, from_=0, to=5)
    spinbox.pack(padx=20, pady=5)

    selected_movies_listbox.bind("<<ListboxSelect>>", update_selected_movies)

    button = tk.Button(root, text="Recommend", font=('Arial', 30), command=recommend_movies)
    button.pack()

    modify(list_of_movies)

    movies.bind("<<ListboxSelect>>", updater)
    movie_entry.bind("<ButtonRelease>", verify)

    root.mainloop()
