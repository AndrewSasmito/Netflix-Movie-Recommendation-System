import tkinter as tk
import csv

from typing import Any
from tkinter import Label, Entry, Listbox, END, ACTIVE

root = tk.Tk()

list_of_movies = []

for line in csv.reader(open('movies.csv', 'r')):
    list_of_movies += [line[2]]

root.geometry("2560x1600")
root.title("Project 2 Window")

label = tk.Label(root, text="Movie Recommender", font=('Arial', 80))
label.pack(padx=20, pady=20)

label2 = tk.Label(root, text="To begin, enter a movie you have watched or like, \nand your desired number of reviews",
                  font=('Arial', 30))
label2.pack(padx=20, pady=10)

# Search bar code

movie_input = Label(root, text="Enter Movie(s)", font=('Arial', 14))

movie_input.pack()

movie_entry = Entry(root, font=('Arial', 20))
movie_entry.pack()

movies = Listbox(root, width=50)
movies.pack()

selected_movies = []  # the movies we are working with


def modify(lst) -> Any:
    """Display movie options"""
    movies.delete(0, END)
    for movie in lst:
        movies.insert(END, movie)


def updater(event) -> Any:
    """Replace entry content with selected movie and store it"""
    movie_name = movies.get(ACTIVE)
    movie_entry.delete(0, END)
    movie_entry.insert(END, movie_name)
    selected_movies.append(movie_name)


def verify(event) -> Any:
    """idk"""
    if movie_entry.get() == '':
        lst = list_of_movies
    else:
        lst = []
        for item in list_of_movies:
            if movie_entry.get().lower() in item.lower():
                lst.append(item)

    modify(lst)


modify(list_of_movies)
movies.bind("<<ListboxSelect>>", updater)
movie_entry.bind("<KeyRelease>", verify)
button = tk.Button(root, text="Recommend", font=('Arial', 30))
button.pack(padx=20, pady=30)

root.mainloop()
