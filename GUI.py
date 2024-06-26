"""This is a module that creates the GUI for the Spotify Tagger."""
# pylint: disable=invalid-name
# pylint: disable=too-many-locals
# pylint: disable=unused-argument
# pylint: disable=global-statement
# pylint: disable=global-variable-undefined
# pylint: disable=consider-using-f-string
# pylint: disable=redefined-builtin
# pylint: disable=global-variable-not-assigned

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pygame import mixer
import mp3
import spotify

# If pygame is not functioning an uninstall and reinstall may be required

# Global variable to store the order of sorting
ASCENDING_ORDER = True
SORTING_COLUMN = 'title'
file_paths = []

# initilizating mixer
mixer.init()

# Refrencing spotify.py
s = spotify.Spotify()


class HoverButton(tk.Button):
    """Custom button class for hover effect"""
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.default_background = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        """A function for entering."""
        self["background"] = self["activebackground"]

    def on_leave(self, e):
        """A function for leaving."""
        self["background"] = self.default_background


# Window creation
root = tk.Tk()
root.title("Pytunes")

# Set background color
root.configure(bg='#1a1a1a')

# Window size
root.minsize(675, 600)

# Load the image for the output label
output_image = tk.PhotoImage(file="GUI_assets/Pytunes_banner.png")

# Label for the output field
output_label = tk.Label(root, image=output_image, bg='#1a1a1a')
output_label.pack(pady=10)


def search_music():
    """A function to search for music."""
    search_term = search_entry.get()
    if search_term:
        matching_music = [item for item in music if search_term.lower()
                          in item.title.lower() or search_term.lower()
                          in item.artist.lower() or search_term.lower()
                          in item.album.lower() or search_term.lower()
                          in item.genre.lower()]
        output_sorted_data(matching_music, 'title')
    else:
        print("Please enter a search term.")


# Search bar frame
search_bar_frame = tk.Frame(root, bg='#1a1a1a')
search_bar_frame.pack(pady=10)


def display_all_songs():
    """A function for when the home button is pressed."""
    output_sorted_data(music, 'title')
    search_entry.delete(0, tk.END)


# Home button
home_button_image = tk.PhotoImage(file="GUI_assets/home.png")
home_button = HoverButton(search_bar_frame, image=home_button_image,
                          command=display_all_songs, bg='#3b3b3b',
                          activebackground='#4b4b4b')
home_button.pack(side=tk.LEFT, padx=5, pady=5)

# Search bar entry
style = ttk.Style()
style.configure("TEntry", fieldbackground='#2b2b2b', background='#2b2b2b',
                foreground='#000000', bordercolor='#2b2b2b',
                lightcolor='#2b2b2b', darkcolor='#2b2b2b', borderwidth=20,
                relief=tk.GROOVE)
search_entry = ttk.Entry(search_bar_frame, width=30, font=("Arial", 14),
                         style='TEntry')
search_entry.pack(side=tk.LEFT, padx=5, pady=5)

# Search button
search_button_image = tk.PhotoImage(file="GUI_assets/search.png")
search_button = HoverButton(search_bar_frame, image=search_button_image,
                            command=search_music, bg='#3b3b3b',
                            activebackground='#4b4b4b')
search_button.pack(side=tk.LEFT, padx=5, pady=5)


# Switch button function
def switch_function():
    "A function for when the switch button is pressed. It will switch\
        between ascending and decending order"
    global ASCENDING_ORDER
    ASCENDING_ORDER = not ASCENDING_ORDER
    output_sorted_data(music, SORTING_COLUMN, reverse=not ASCENDING_ORDER)


switch_button_image = tk.PhotoImage(file="GUI_assets/switch.png")
switch_button = HoverButton(search_bar_frame, image=switch_button_image,
                            command=switch_function, bg='#3b3b3b',
                            activebackground='#4b4b4b')
switch_button.pack(side=tk.RIGHT, padx=5, pady=5)
switch_button.pack(side=tk.RIGHT, padx=5, pady=5)

# Center the search bar
search_bar_frame.pack(anchor='center')

# Output field - Replacing the Text widget with a Treeview widget
columns = ("Title", "Artist", "Album", "Genre", "Length", "Date")
output_tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    output_tree.heading(col, text=col)
output_tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

output_tree.column("Title", width=100, minwidth=100, anchor=tk.CENTER)
output_tree.column("Artist", width=100, minwidth=100, anchor=tk.CENTER)
output_tree.column("Album", width=100, minwidth=100, anchor=tk.CENTER)
output_tree.column("Genre", width=150, minwidth=150, anchor=tk.CENTER)
output_tree.column("Length", width=25, minwidth=25, anchor=tk.CENTER)
output_tree.column("Date", width=25, minwidth=25, anchor=tk.CENTER)


def sort_data_menu():
    """A function for the sort data menu."""
    global sort_window
    sort_window = tk.Toplevel()
    sort_window.resizable(False, False)

    # Create a gradient background using rectangles
    canvas = tk.Canvas(sort_window, width=200, height=240)
    red_start, green_start, blue_start = 70, 0, 192
    red_end, green_end, blue_end = 230, 0, 255

    for i in range(200):
        red = red_start + int((red_end - red_start) * i / 200)
        green = green_start + int((green_end - green_start) * i / 200)
        blue = blue_start + int((blue_end - blue_start) * i / 200)
        color = "#{:02x}{:02x}{:02x}".format(red, green, blue)
        canvas.create_rectangle(i, 0, i + 1, 240, outline=color, fill=color)

    # Create the buttons
    button1 = tk.Button(sort_window, text="Sort by Song Name",
                        command=sort_song_name)
    button2 = tk.Button(sort_window, text="Sort by Artist Name",
                        command=sort_artist_name)
    button3 = tk.Button(sort_window, text="Sort by Song Album",
                        command=sort_song_album)
    button4 = tk.Button(sort_window, text="Sort by Genre Type",
                        command=sort_song_genre)
    button5 = tk.Button(sort_window, text="Sort by Song Length",
                        command=sort_song_length)
    button6 = tk.Button(sort_window, text="Sort by Date",
                        command=sort_song_date)

    # Add the buttons to the canvas
    canvas.create_window(100, 20, window=button1)
    canvas.create_window(100, 60, window=button2)
    canvas.create_window(100, 100, window=button3)
    canvas.create_window(100, 140, window=button4)
    canvas.create_window(100, 180, window=button5)
    canvas.create_window(100, 220, window=button6)

    # Pack the canvas
    canvas.pack()


# Empty list for mp3s
music = []


# Function to append file paths to the list
def append_file_path(file_path):
    """A function to append file path to the list."""
    if file_path not in file_paths:
        file_paths.append(file_path)


def output_sorted_data(list, type, reverse=False):
    """A function that displays the results of a sucessful sort."""
    global SORTING_COLUMN
    SORTING_COLUMN = type
    output_tree.delete(*output_tree.get_children())  # Clears existing rows
    sorted_list = sorted(list, key=lambda x: getattr(x, type), reverse=reverse)

    for item in sorted_list:
        # Convert length to minutes:seconds format
        minutes, seconds = divmod(item.length, 60)
        duration = f"{int(minutes)}:{int(seconds):02d}"
        output_tree.insert("", tk.END, values=(item.title, item.artist,
                                               item.album, item.genre,
                                               duration, item.date))


def sort_song_length():
    """A function that will sort songs by length when the sort button is\
        clicked."""
    sorted_music = sorted(music, key=lambda x: x.length)
    output_sorted_data(sorted_music, 'length')
    print("Sorting by song length...")
    # Close the window
    sort_window.destroy()


def sort_song_date():
    """A function that will sort songs by publication date when the sort\
        button is clicked."""
    sorted_music = sorted(music, key=lambda x: x.date)
    output_sorted_data(sorted_music, 'date')
    print("Sorting by song date...")
    # Close the window
    sort_window.destroy()


def sort_song_name():
    """A function that will sort songs by name when the sort button is \
        clicked"""
    sorted_music = sorted(music, key=lambda x: x.title)
    output_sorted_data(sorted_music, 'title')
    print("Sorting by song name...")
    # Close the window
    sort_window.destroy()


def sort_artist_name():
    """A function that will sort songs by artist when the sort button \
        is clicked."""
    sorted_music = sorted(music, key=lambda x: x.artist)
    output_sorted_data(sorted_music, 'artist')
    print("Sorting by artist name...")
    # Close the window
    sort_window.destroy()


def sort_song_album():
    """A function that will sort songs by album when the sort button
        is clicked."""
    sorted_music = sorted(music, key=lambda x: x.album)
    output_sorted_data(sorted_music, 'album')
    print("Sorting by song album...")
    # Close the window
    sort_window.destroy()


def sort_song_genre():
    """A function that will sort songs by album when the sort button
        is clicked."""
    sorted_music = sorted(music, key=lambda x: x.genre)
    output_sorted_data(sorted_music, 'genre')
    print("Sorting by song genre...")
    # Close the window
    sort_window.destroy()


# Upload file function
def upload_file():
    """A function that allows the user to upload .mp3 files into the \
        program."""
    global music, file_paths
    new_file_paths = filedialog.askopenfilenames()
    for file_path in new_file_paths:
        append_file_path(file_path)
    music = [mp3.Mp3(file_path) for file_path in file_paths]
    output_sorted_data(music, 'title')


# Function to sync songs with spotify
def sync_website():
    """A function to sync data."""
    global music
    for song in music:
        s.sync_spotify(song)
    music = [mp3.Mp3(file_path) for file_path in file_paths]
    output_sorted_data(music, 'title')


# Function to play music
def play_music():
    """A function to play the selected music."""
    try:
        selection = output_tree.selection()[0]
        selected_values = output_tree.item(selection, "values")
        selected_title = selected_values[0]

        # Find the correct song based on the title
        for song in music:
            if song.title == selected_title:
                item = song
                break

        mixer.music.load(item.file_path)
        mixer.music.play()
        root.after(10, check_music_status)
    finally:
        pass


# Pause music function
def pause_music():
    """A function to pause the currently playing music."""
    mixer.music.pause()


def previous_song():
    """A fuction to play the previous song in the list."""
    try:
        selection = output_tree.selection()[0]
        prev_item = output_tree.prev(selection)
        if prev_item:
            output_tree.selection_set(prev_item)
            play_music()
    finally:
        pass


def next_song():
    """A function to play the next song in the list."""
    try:
        selection = output_tree.selection()[0]
        next_item = output_tree.next(selection)
        if next_item:
            output_tree.selection_set(next_item)
            play_music()
    finally:
        pass


# Function to check music status
def check_music_status():
    """A function to check if the music is still playing."""
    if not mixer.music.get_busy():
        output_tree.selection_remove(output_tree.selection())
    else:
        root.after(10, check_music_status)


# volume slider function
def set_volume(val):
    """A fuction to work the volume slider."""
    volume = int(val) / 100
    mixer.music.set_volume(volume)


# Frame for buttons
button_frame = tk.Frame(root, bg='#1a1a1a')
button_frame.pack(pady=10)

# Frame for play/pause buttons
play_pause_frame = tk.Frame(button_frame, bg='#1a1a1a')
play_pause_frame.pack(side=tk.TOP, pady=10)

# Volume control frame
volume_control_frame = tk.Frame(play_pause_frame, bg='#404040')
volume_control_frame.pack(side=tk.LEFT, padx=5)

# Volume label
volume_label = tk.Label(volume_control_frame, text="Volume", bg='#404040',
                        fg='white')
volume_label.pack(side=tk.TOP)

# Volume slider
volume_slider = tk.Scale(volume_control_frame, from_=0, to=100,
                         orient=tk.HORIZONTAL, command=set_volume,
                         sliderlength=10, length=100, background='#be00ff',
                         troughcolor='#88f1fc', activebackground='#000000')
volume_slider.set(75)  # Sets the initial volume to 75%
volume_slider.pack(side=tk.BOTTOM)

# previous button
previous_button_image = tk.PhotoImage(file="GUI_assets/previous.png")
previous_button = HoverButton(play_pause_frame, image=previous_button_image,
                              command=previous_song, bg='#3b3b3b',
                              activebackground='#4b4b4b')
previous_button.pack(side=tk.LEFT, padx=5)

# play button
play_button_image = tk.PhotoImage(file="GUI_assets/play.png")
play_button = HoverButton(play_pause_frame, image=play_button_image,
                          command=play_music, bg='#3b3b3b',
                          activebackground='#4b4b4b')
play_button.pack(side=tk.LEFT, padx=5)

# pause button
pause_button_image = tk.PhotoImage(file="GUI_assets/pause.png")
pause_button = HoverButton(play_pause_frame, image=pause_button_image,
                           command=pause_music, bg='#3b3b3b',
                           activebackground='#4b4b4b')
pause_button.pack(side=tk.LEFT, padx=5)

# next button
next_button_image = tk.PhotoImage(file="GUI_assets/next.png")
next_button = HoverButton(play_pause_frame, image=next_button_image,
                          command=next_song, bg='#3b3b3b',
                          activebackground='#4b4b4b')
next_button.pack(side=tk.LEFT, padx=5)

# upload file button
upload_button_image = tk.PhotoImage(file="GUI_assets/upload.png")
upload_button = HoverButton(button_frame, image=upload_button_image,
                            command=upload_file, bg='#3b3b3b',
                            activebackground='#4b4b4b')
upload_button.pack(side=tk.LEFT, padx=5)

# sort data menu button
sort_button_image = tk.PhotoImage(file="GUI_assets/sort.png")
sort_button = HoverButton(button_frame, image=sort_button_image,
                          command=sort_data_menu, bg='#3b3b3b',
                          activebackground='#4b4b4b')
sort_button.pack(side=tk.LEFT, padx=5)

# sync button
ping_button_image = tk.PhotoImage(file="GUI_assets/sync.png")
ping_button = HoverButton(button_frame, image=ping_button_image,
                          command=sync_website, bg='#3b3b3b',
                          activebackground='#4b4b4b')
ping_button.pack(side=tk.LEFT, padx=5)

# start
root.mainloop()
