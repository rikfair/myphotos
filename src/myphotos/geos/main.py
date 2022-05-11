#!/usr/bin/python3
# -----------------------------------------------
"""
    DESCRIPTION:
        Manage photo latitude and longitude

    ASSUMPTIONS:
        No assumptions to note

    ACCURACY:
        No accuracy issues to note
"""
# -----------------------------------------------

import tkinter as tk

import myphotos.geos.data

# -----------------------------------------------

_BOK_PROGRESS = 'bok_progress'
_BOK_SELECTOR = 'bok_selector'
_BTN_SOURCE = 'btn_source'
_FRM_PROGRESS = 'frm_progress'
_FRM_SELECTOR = 'frm_select'
_TXB_PROGRESS = 'txb_progress'
_TXT_SOURCE = 'txt_source'

_SAVED_DATA = 'geos'

# -----------------------------------------------


class _DateInterface(myphotos.MyPhotosWindow):
    """ Date tkinter interface """

    def __init__(self, win):
        """ Initialises the date interface """

        super().__init__(win, 'Dates')
        self.initialise_elements()
        self.draw_selector_window(True)

    # -------------------------------------------

    def draw_selector_window(self, show):
        """ Packs the selector window objects """

        if show:
            self.elements[_FRM_SELECTOR].pack(anchor=tk.N, side=tk.LEFT)
            self.elements[_BOK_SELECTOR].pack(side=tk.RIGHT)
        else:
            self.elements[_FRM_SELECTOR].pack_forget()
            self.elements[_BOK_SELECTOR].pack_forget()

    # -------------------------------------------


# -----------------------------------------------


def main():
    """ Main function """
    win = tk.Tk()
    _GeoInterface(win)
    win.mainloop()


# -----------------------------------------------

if __name__ == '__main__':
    main()

# -----------------------------------------------
# End.
