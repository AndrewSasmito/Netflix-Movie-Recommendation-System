import tkinter as tk
import csv

from typing import Any
from tkinter import Label, Entry, Listbox, END, messagebox

"""
TODO:
- Fix search: DONE
- Fix movietitle: DONE
- Fix select bug: in progress
    each time you select a movie, it automatically selects the first movie in our entry box
    doesnt display selected movie in selected movies until you select another one
- Add comments: in progress
"""

root = tk.Tk()

list_of_movies = []

for line in csv.reader(open('movies.csv', 'r')):
    list_of_movies += [line[2]]

item = list_of_movies.pop(0)  # remove first MovieTitle

root.geometry("2560x1600")
root.title("Project 2 Window")
label = tk.Label(root, text="Movie Recommender", font=('Arial', 80))
label.pack(padx=20, pady=20)
label2 = tk.Label(root, text="To begin, enter a movie you have watched or like, \nand your desired number of reviews",
                  font=('Arial', 25))
label2.pack(padx=20, pady=10)

movie_input1 = Label(root, text="Selected Movies", font=('Arial', 20))
movie_input1.pack()

selected_movies_listbox = tk.Listbox(root, width=50, height=5)
selected_movies_listbox.pack(pady=5)

movie_input2 = Label(root, text="Enter Movie(s) By Clicking or Typing", font=('Arial', 20))
movie_input2.pack(pady=5)

movie_entry = Entry(root, font=('Arial', 20))
movie_entry.pack(pady=5)

movies = Listbox(root, width=50, height=5)
movies.pack(pady=5)

movie_input3 = Label(root, text="Maximum number of reviews", font=('Arial', 20))
movie_input3.pack(pady=5)

spinbox = tk.Spinbox(root, from_=0, to=50)
spinbox.pack(padx=20, pady=5)

selected_movies = set()  # store the movies we are working with


def modify(lst) -> Any:
    """Display movie options"""
    movies.delete(0, END)
    for movie in lst:
        movies.insert(END, movie)


def updater(event):
    """Replace entry content with selected movie and store it"""
    if len(selected_movies) >= 5:
        # error message
        tk.messagebox.showinfo("Limit Reached", "You can only select up to 5 movies. Press recommend and try again.")
        return

    movie_name = movies.get(tk.ACTIVE)
    movie_entry.delete(0, tk.END)
    movie_entry.insert(tk.END, movie_name)
    selected_movies.add(movie_name)
    update_selected_movies()


def verify(event) -> Any:
    """TODO: Complete docstring"""
    if movie_entry.get() == '':
        lst = list_of_movies
    else:
        lst = []
        for i in list_of_movies:
            if movie_entry.get().lower() in i.lower():
                lst.append(i)
    modify(lst)


def recommend_movies():
    """Function to handle the recommendation process"""
    global selected_movies
    movie_entry.delete(0, tk.END)
    selected_movies = set()
    spinbox.delete(0, tk.END)
    spinbox.insert(0, '0')


def update_selected_movies(event=None):
    """Insert the movies the user selected to our text label"""
    global selected_movies
    selected_movies_listbox.delete(0, tk.END)
    for movie in selected_movies:
        selected_movies_listbox.insert(tk.END, movie)


selected_movies_listbox.bind("<<ListboxSelect>>", update_selected_movies)


def add_movie():
    """TODO: Complete docstring"""
    global selected_movies
    selected_movies.add("Selected Movie")
    update_selected_movies()


button = tk.Button(root, text="Recommend", font=('Arial', 30), command=recommend_movies)
button.pack()

modify(list_of_movies)

movies.bind("<<ListboxSelect>>", updater)
movie_entry.bind("<KeyRelease>", verify)


root.mainloop()
