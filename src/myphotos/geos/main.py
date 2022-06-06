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
_SCV_GEOS = 'scv_geos'
_TXB_PROGRESS = 'txb_progress'
_TXT_SOURCE = 'txt_source'

_SAVED_DATA = 'geos'

# -----------------------------------------------


class GeoInterface(myphotos.MyPhotosWindow):
    """ Date tkinter interface """

    def __init__(self, win, return_frame=None):
        """ Initialises the date interface """

        super().__init__(win, myphotos.GEOS, return_frame)
        self._initialise_elements()
        self.geo_data = []
        self.geo_elements = {}
        self.dsc_elements = {}

    # -------------------------------------------

    def go(self, buttons=True):
        super().go(buttons)
        for geo in self.geo_data:
            fn = geo['filename']
            self.geo_elements[fn + '#filename'].destroy()
            self.geo_elements[fn].destroy()
            self.dsc_elements[fn].destroy()
        self._draw_geos_window(False)
        self._draw_progress_window(False)
        self._draw_selector_window(True)

    # -------------------------------------------

    def _create_geo_record(self, geo):
        """ Creates a geo record """

        record = len(self.geo_elements)

        filename = tk.Label(self.elements[_SCV_GEOS], text=geo['filename'])
        filename.grid(row=record, column=0, padx=6, pady=2)
        self.geo_elements[geo['filename'] + '#filename'] = filename

        coordinates = tk.Entry(self.elements[_SCV_GEOS], width=30)
        coordinates.insert(tk.END, geo['coordinates'])
        coordinates.grid(row=record, column=1, padx=6, pady=2)
        self.geo_elements[geo['filename']] = coordinates

        description = tk.Entry(self.elements[_SCV_GEOS], width=40)
        description.insert(tk.END, geo['description'])
        description.grid(row=record, column=2, padx=6, pady=2)
        self.dsc_elements[geo['filename']] = description

    # -------------------------------------------

    def _draw_geos_window(self, show):
        """ Packs the geos window objects """

        if show:
            self.elements[_FRM_GEOS].pack(anchor=tk.N, side=tk.TOP, fill=tk.BOTH, expand=True)
            self.elements[_BOK_GEOS].pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        else:
            self.elements[_FRM_GEOS].pack_forget()
            self.elements[_BOK_GEOS].pack_forget()

    # -------------------------------------------

    def _draw_progress_window(self, show):
        """ Packs the progress window objects """

        self.elements[_TXB_PROGRESS].delete('1.0', tk.END)

        if show:
            self.elements[_FRM_PROGRESS].pack(anchor=tk.N, side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.elements[_BOK_PROGRESS].pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        else:
            self.elements[_FRM_PROGRESS].pack_forget()
            self.elements[_BOK_PROGRESS].pack_forget()

    # -------------------------------------------

    def _draw_selector_window(self, show):
        """ Packs the selector window objects """

        if show:
            self.elements[_FRM_SELECTOR].pack(anchor=tk.N, side=tk.LEFT)
            self.elements[_BOK_SELECTOR].pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        else:
            self.elements[_FRM_SELECTOR].pack_forget()
            self.elements[_BOK_SELECTOR].pack_forget()

    # -------------------------------------------

    def _initialise_elements(self):
        """ Initialises the tkinter elements for this interface """

        self.elements[_FRM_SELECTOR] = tk.Frame(self.main)
        self.create_directory_selector(self.elements[_FRM_SELECTOR], _TXT_SOURCE, 'Source')
        self.create_ok_button(_BOK_SELECTOR, self._ok_selector)

        data = myphotos.get_saved_data(_SAVED_DATA)
        self.elements[_TXT_SOURCE].config(text=data.get(_TXT_SOURCE, ''))

        self.elements[_FRM_GEOS] = tk.Frame(self.main)
        self.create_scroll_canvas(self.elements[_FRM_GEOS], _SCV_GEOS)
        self.create_ok_button(_BOK_GEOS, self._ok_geos)

        self.elements[_FRM_PROGRESS] = tk.Frame(self.main)
        self.create_progress_box(self.elements[_FRM_PROGRESS], _TXB_PROGRESS)
        self.create_ok_button(_BOK_PROGRESS, self._ok_progress)

    # -------------------------------------------

    def _ok_geos(self):
        """ OK button command for the geos frame """

        update_data = []
        for geo in self.geo_data:
            fn = geo['filename']
            if geo['coordinates'] != self.geo_elements[fn].get() or geo['description'] != self.dsc_elements[fn].get():
                update_data.append({
                    'file_path': geo['file_path'],
                    'coordinates': self.geo_elements[fn].get(),
                    'description': self.dsc_elements[fn].get()
                })
            self.geo_elements[fn + '#filename'].destroy()
            self.geo_elements[fn].destroy()
            self.dsc_elements[fn].destroy()

        self.geo_elements = {}
        self._draw_geos_window(False)
        self._draw_progress_window(True)

        for p in myphotos.geos.data.set_data(update_data):
            self.update_progress(_TXB_PROGRESS, p)
        self.update_progress(_TXB_PROGRESS, '\nCompleted.')

    # -------------------------------------------

    def _ok_progress(self):
        """ OK button command for the progress frame """

        self._draw_progress_window(False)
        self._draw_selector_window(True)

    # -------------------------------------------

    def _ok_selector(self):
        """ OK button command for the selector frame """

        data = {_TXT_SOURCE: self.elements[_TXT_SOURCE].cget('text')}
        myphotos.set_saved_data(data, _SAVED_DATA)
        # ---
        self._draw_selector_window(False)
        self._draw_geos_window(True)
        # ---
        self.geo_data = myphotos.geos.data.get_data(data[_TXT_SOURCE])
        for geo in self.geo_data:
            self._create_geo_record(geo)


# -----------------------------------------------


def main():
    """ Main function """
    win = tk.Tk()
    GeoInterface(win).go()
    win.mainloop()


# -----------------------------------------------

if __name__ == '__main__':
    main()

# -----------------------------------------------
# End.
