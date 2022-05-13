#!/usr/bin/python3
# -----------------------------------------------
"""
    DESCRIPTION:
        Common functions for the myphotos app

    ASSUMPTIONS:
        No assumptions to note

    ACCURACY:
        No accuracy issues to note
"""
# -----------------------------------------------

import os
import pickle
import tkinter as tk
from tkinter import filedialog

# -----------------------------------------------

ERRORS = '_errors_'
NON_PHOTOS = '_non-photos_'
WIN_HEIGHT = 300
WIN_WIDTH = 800
GEOMETERY = f'{WIN_WIDTH}x{WIN_HEIGHT}'

# -----------------------------------------------


class MyPhotosWindow:
    """ Main window and common functions for the myphoto tkinter interface """

    def __init__(self, win, title):
        win.title(f'My Photos - {title}')
        win.geometry(GEOMETERY)
        self.main = tk.Frame(win, bg='green')
        self.main.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.btns = tk.Frame(win, height=50, bg='blue')
        self.btns.pack(side=tk.BOTTOM, fill=tk.X)
        self.elements = {}

    # -------------------------------------------

    def _create_directory_selector(self, master, name, label):
        """ Creates a directory selector frame """

        frame = tk.Frame(master)
        tk.Button(
            master=frame, text=f'Select {label} Directory', width=24, command=lambda: self._set_directory(name)
        ).pack(side=tk.LEFT)
        self.elements[name] = tk.Label(frame)
        self.elements[name].pack(side=tk.LEFT, padx=10)
        frame.pack(anchor=tk.W, padx=10, pady=(10, 0))

    # -------------------------------------------

    def _create_ok_button(self, name, command):
        """ Creates an ok button in the bottom right """

        frame = tk.Frame(self.btns)
        tk.Button(frame, text='OK', width=10, command=command).pack(side=tk.RIGHT, padx=10, pady=10)
        self.elements[name] = frame

    # -------------------------------------------

    def _create_options_menu(self, master, name, options):
        """ Creates an options menu """

        frame = tk.Frame(master)
        self.elements[name] = tk.StringVar()
        tk.OptionMenu(frame, self.elements[name], *options).pack(side=tk.LEFT)
        frame.pack(anchor=tk.W, padx=10, pady=(10, 0))

    # -------------------------------------------

    def _create_progress_box(self, master, name):
        """ Creates a scrollable text area for showing progress"""

        frame = tk.Frame(master, padx=10, pady=10)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        progress_box = tk.Text(frame, height=5, padx=10, pady=10, yscrollcommand=scrollbar.set)
        progress_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.elements[name] = progress_box

    # -------------------------------------------

    def create_scroll_canvas(self, master, name):
        """ Creates a scrollable canvas within a frame """

        canvas = tk.Canvas(master, height=10)  # Presence of height parameter stops ok button being squashed
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(master, command=canvas.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda _: canvas.configure(scrollregion=canvas.bbox(tk.ALL)))
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), tk.UNITS))
        self.elements[name] = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.elements[name], anchor='nw')

    # -------------------------------------------

    def _set_directory(self, name):
        """ Sets the directory """

        path = filedialog.askdirectory()
        self.elements[name].config(text=path)

    # -------------------------------------------

    def _update_progress(self, name, text):
        """ Updates a progress text box """

        if isinstance(text, list):
            text = '\n'.join(text)
        self.elements[name].insert(tk.END, text + '\n')
        self.elements[name].see(tk.END)
        self.main.update()


# -----------------------------------------------


def _get_pickle_file_path(filename):
    """ Gets the pickle filename """

    return os.path.join(os.path.dirname(os.path.realpath(__file__)), '.data', filename + '.pickle')


# -----------------------------------------------


def get_saved_data(filename):
    """ Gets the pickle data if it exists """

    file_path = _get_pickle_file_path(filename)
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
        return data
    return {}


# -----------------------------------------------


def set_saved_data(data, filename):
    """ Pickles the data:dict parameter to a file """

    file_path = _get_pickle_file_path(filename)
    directory = os.path.dirname(file_path)

    if not os.path.isdir(directory):
        os.makedirs(directory)

    with open(file_path, 'wb') as file:
        pickle.dump(data, file)


# -----------------------------------------------
# End.
