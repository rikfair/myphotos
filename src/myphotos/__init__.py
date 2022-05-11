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

import tkinter as tk
from tkinter import filedialog

# -----------------------------------------------

WIN_HEIGHT = 300
WIN_WIDTH = 800
GEOMETERY = f'{WIN_WIDTH}x{WIN_HEIGHT}'

# -----------------------------------------------


class MyPhotosWindow:
    """ Main window and common functions for the myphoto tkinter interface """

    def __init__(self, win, title):
        # ---
        self.win = win
        self.win.title(f'My Photos - {title}')
        self.win.geometry(GEOMETERY)
        self.elements = {}

    # -------------------------------------------

    def _create_directory_selector(self, parent, name, label):
        """ Creates a directory selector frame """

        frame = tk.Frame(parent)
        tk.Button(
            master=frame, text=f'Select {label} Directory', width=24, command=lambda: self._set_directory(name)
        ).pack(side=tk.LEFT)
        self.elements[name] = tk.StringVar()
        tk.Label(frame, textvariable=self.elements[name]).pack(side=tk.LEFT, padx=10)
        frame.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=(10, 0))

    # -------------------------------------------

    def _set_directory(self, name):
        """ Sets the directory """

        path = filedialog.askdirectory()
        self.elements[name].set(path)


# -----------------------------------------------
# End.
