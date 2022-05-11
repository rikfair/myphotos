#!/usr/bin/python3
# -----------------------------------------------
"""
    DESCRIPTION:
        Manage photo dates

    ASSUMPTIONS:
        No assumptions to note

    ACCURACY:
        No accuracy issues to note
"""
# -----------------------------------------------

import tkinter as tk

import myphotos

# -----------------------------------------------

_BTN_SOURCE = 'btn_source'
_BTN_TARGET = 'btn_target'
_FRM_SELECT = 'frm_select'
_TXT_SOURCE = 'txt_source'
_TXT_TARGET = 'txt_target'

# -----------------------------------------------


class _DateInterface(myphotos.MyPhotosWindow):
    """ Date tkinter interface """

    def __init__(self, win):
        """ Initialises the date interface """

        super().__init__(win, 'Dates')
        self.initialise_elements()
        self.draw_select_window()

    # -------------------------------------------

    def draw_select_window(self):
        """ Packs the select window objects """

        self.elements[_FRM_SELECT].pack(side=tk.LEFT, anchor=tk.N)

    # -------------------------------------------

    def initialise_elements(self):
        """ Initialises the tkinter elements for this interface """

        self.elements[_FRM_SELECT] = tk.Frame(self.win)
        self._create_directory_selector(self.elements[_FRM_SELECT], _TXT_SOURCE, 'Source')
        self._create_directory_selector(self.elements[_FRM_SELECT], _TXT_TARGET, 'Target')

    # -------------------------------------------


# -----------------------------------------------


def main():
    """ Main function """
    win = tk.Tk()
    _DateInterface(win)
    win.mainloop()


# -----------------------------------------------

if __name__ == '__main__':
    main()

# -----------------------------------------------
# End.
