import csv
import tkinter
from tkinter import Tk, Label, Entry, Listbox, END, ACTIVE, IntVar, Spinbox, Button, messagebox


def modify(lst: list) -> None:
    """Display movie options"""
    movies.delete(0, END)
    for movie in lst:
        movies.insert(END, movie)


def updater(event: tkinter.Event) -> None:
    """Replace entry content with selected movie and store it"""
    if len(selected_movies) >= 5:
        # error message
        messagebox.showinfo("Limit Reached", "You can only select up to 5 movies. Press recommend and try again.")
        return

    movie_name = movies.get(ACTIVE)
    movie_entry.delete(0, END)
    movie_entry.insert(END, movie_name)
    selected_movies.add(movie_name)
    update_selected_movies()


def verify(event: tkinter.Event) -> None:
    """TODO: Complete this docstring"""
    if movie_entry.get() == '':
        lst = list_of_movies
    else:
        lst = []
        for item in list_of_movies:
            if movie_entry.get().lower() in item.lower():
                lst.append(item)
    modify(lst)


def recommend_movies() -> None:
    """Function to handle the recommendation process"""
    global selected_movies
    movie_entry.delete(0, END)
    selected_movies = set()
    spinbox.delete(0, END)
    spinbox.insert(0, '0')
    movies.selection_clear(0, END)


def update_selected_movies(event: tkinter.Event = None) -> None:
    """Insert the movies the user selected to our text label"""
    global selected_movies
    selected_movies_listbox.delete(0, END)
    for movie in selected_movies:
        selected_movies_listbox.insert(END, movie)
    movies.focus_set()


def add_movie() -> None:
    """TODO: Complete this docstring"""
    global selected_movies
    selected_movies.add("Selected Movie")
    update_selected_movies()


def clear_entry_selection(event: tkinter.Event) -> None:
    """Clear any selection in the entry widget"""
    movie_entry.selection_clear()


def set_entry_cursor(event: tkinter.Event) -> None:
    """Set cursor position to the end of the entry widget"""
    movie_entry.icursor(END)


root = Tk()

list_of_movies = []

with open('movies.csv', 'r') as movies_file:
    for line in csv.reader(movies_file):
        list_of_movies += [line[2]]

root.geometry("2560x1600")
root.title("Project 2 Window")

label = Label(root, text="Movie Recommender", font=('Arial', 80))
label.pack(padx=20, pady=10)

label2 = Label(root, text="To begin, enter a movie you have watched or like, and your \ndesired number of reviews",
               font=('Arial', 24))
label2.pack(padx=20, pady=5)

movie_input1 = Label(root, text="Selected:", font=('Arial', 14))
movie_input1.pack()

selected_movies_listbox = Listbox(root, width=50, height=5)
selected_movies_listbox.pack(pady=5)

movie_input2 = Label(root, text="Enter Movie(s) By Double Clicking. \nFeel free to type to search for movies.",
                     font=('Arial', 14), width=50)
movie_input2.pack(pady=5)

movie_entry = Entry(root, font=('Arial', 20))
movie_entry.pack()

movie_entry.bind("<FocusIn>", clear_entry_selection)

movies = Listbox(root, width=50, height=5)
movies.pack(pady=5)

movie_input3 = Label(root, text="Maximum number of reviews:", font=('Arial', 14))
movie_input3.pack()

num_of_reviews = IntVar()  # gets passed to backend later

num_of_reviews.set(0)

spinbox = Spinbox(root, from_=0, to=100, textvariable=num_of_reviews)
spinbox.pack(padx=20, pady=10)

selected_movies = set()  # store the movies we are working with

selected_movies_listbox.bind("<<ListboxSelect>>", update_selected_movies)

button = Button(root, text="Recommend", font=('Arial', 30), command=recommend_movies)
button.pack()

modify(list_of_movies)

movies.bind("<ButtonRelease-1>", updater)

movie_entry.bind("<Leave>", clear_entry_selection)
movie_entry.bind("<FocusIn>", set_entry_cursor)

movie_input4 = Label(root, text="Recommendations:", font=('Arial', 20))
movie_input4.pack()

root.mainloop()
