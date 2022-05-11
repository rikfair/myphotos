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

_BOK_GEOS = 'bok_geos'
_BOK_PROGRESS = 'bok_progress'
_BOK_SELECTOR = 'bok_selector'
_BTN_SOURCE = 'btn_source'
_FRM_GEOS = 'frm_geos'
_FRM_PROGRESS = 'frm_progress'
_FRM_SELECTOR = 'frm_select'
_TXB_PROGRESS = 'txb_progress'
_TXT_SOURCE = 'txt_source'

_SAVED_DATA = 'geos'

# -----------------------------------------------


class _GeoInterface(myphotos.MyPhotosWindow):
    """ Date tkinter interface """

    def __init__(self, win):
        """ Initialises the date interface """

        super().__init__(win, 'Dates')
        self.initialise_elements()
        self.draw_selector_window(True)

    # -------------------------------------------

    def create_geo_record(self, geo):
        """ Creates a geo record """

        frame = tk.Frame(_FRM_GEOS)
        label = tk.Label(frame, text=geo['filename'])
        lat_long = tk.StringVar()
        entry = tk.Entry(frame)

    # -------------------------------------------

    def draw_geos_window(self, show):
        """ Packs the geos window objects """

        if show:
            self.elements[_FRM_GEOS].pack(anchor=tk.N, side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.elements[_BOK_GEOS].pack(side=tk.RIGHT)
        else:
            self.elements[_FRM_GEOS].pack_forget()
            self.elements[_BOK_GEOS].pack_forget()

    # -------------------------------------------

    def draw_progress_window(self, show):
        """ Packs the progress window objects """

        if show:
            self.elements[_FRM_PROGRESS].pack(anchor=tk.N, side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.elements[_BOK_PROGRESS].pack(side=tk.RIGHT)
        else:
            self.elements[_FRM_PROGRESS].pack_forget()
            self.elements[_BOK_PROGRESS].pack_forget()

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

    def initialise_elements(self):
        """ Initialises the tkinter elements for this interface """

        self.elements[_FRM_SELECTOR] = tk.Frame(self.main, bg='red')
        self._create_directory_selector(self.elements[_FRM_SELECTOR], _TXT_SOURCE, 'Source')
        self._create_ok_button(_BOK_SELECTOR, self.ok_selector)

        data = myphotos.get_saved_data(_SAVED_DATA)
        self.elements[_TXT_SOURCE].config(text=data.get(_TXT_SOURCE, ''))

        self.elements[_FRM_GEOS] = tk.Frame(self.main, bg='yellow')
        self._create_ok_button(_BOK_GEOS, self.ok_geos)

        self.elements[_FRM_PROGRESS] = tk.Frame(self.main, bg='yellow')
        self._create_progress_box(self.elements[_FRM_PROGRESS], _TXB_PROGRESS)
        self._create_ok_button(_BOK_PROGRESS, self.ok_progress)

    # -------------------------------------------

    def ok_geos(self):
        """ OK button command for the geos frame """

        self.draw_geos_window(False)
        self.draw_progress_window(True)

    # -------------------------------------------

    def ok_progress(self):
        """ OK button command for the progress frame """

        self.draw_progress_window(False)
        self.draw_selector_window(True)

    # -------------------------------------------

    def ok_selector(self):
        """ OK button command for the selector frame """

        data = {_TXT_SOURCE: self.elements[_TXT_SOURCE].cget('text')}
        myphotos.set_saved_data(data, _SAVED_DATA)
        # ---
        self.draw_selector_window(False)
        self.draw_geos_window(True)
        # ---
        geos = myphotos.geos.data.get_data(data[_TXT_SOURCE])
        for geo in geos:
            print(geo)


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
