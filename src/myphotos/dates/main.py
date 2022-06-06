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
from myphotos.dates import filename_to_photo, photo_to_filename

# -----------------------------------------------

_BOK_PROGRESS = 'bok_progress'
_BOK_SELECTOR = 'bok_selector'
_BTN_SOURCE = 'btn_source'
_BTN_TARGET = 'btn_target'
_FRM_PROGRESS = 'frm_progress'
_FRM_SELECTOR = 'frm_select'
_OMU_OPTIONS = 'omu_options'
_TXB_PROGRESS = 'txb_progress'
_TXT_SOURCE = 'txt_source'
_TXT_TARGET = 'txt_target'

_OPTIONS = ['Filename to Photo', 'Photo to Filename']
_SAVED_DATA = 'dates'

# -----------------------------------------------


class DateInterface(myphotos.MyPhotosWindow):
    """ Date tkinter interface """

    def __init__(self, win, return_frame=None):
        """ Initialises the date interface """

        super().__init__(win, myphotos.DATES, return_frame)
        self._initialise_elements()

    # -------------------------------------------

    def go(self, buttons=True):
        super().go(buttons)
        self._draw_progress_window(False)
        self._draw_selector_window(True)

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
        self.create_directory_selector(self.elements[_FRM_SELECTOR], _TXT_TARGET, 'Target')
        self.create_options_menu(self.elements[_FRM_SELECTOR], _OMU_OPTIONS, _OPTIONS)
        self.create_ok_button(_BOK_SELECTOR, self._ok_selector)

        data = myphotos.get_saved_data(_SAVED_DATA)
        self.elements[_TXT_SOURCE].config(text=data.get(_TXT_SOURCE, ''))
        self.elements[_TXT_TARGET].config(text=data.get(_TXT_TARGET, ''))
        self.elements[_OMU_OPTIONS].set(data.get(_OMU_OPTIONS, _OPTIONS[0]))

        self.elements[_FRM_PROGRESS] = tk.Frame(self.main)
        self.create_progress_box(self.elements[_FRM_PROGRESS], _TXB_PROGRESS)
        self.create_ok_button(_BOK_PROGRESS, self._ok_progress)

    # -------------------------------------------

    def _ok_progress(self):
        """ OK button command for the progress frame """

        self._draw_progress_window(False)
        self._draw_selector_window(True)

    # -------------------------------------------

    def _ok_selector(self):
        """ OK button command for the selector frame """

        data = {
            _TXT_SOURCE: self.elements[_TXT_SOURCE].cget('text'),
            _TXT_TARGET: self.elements[_TXT_TARGET].cget('text'),
            _OMU_OPTIONS: self.elements[_OMU_OPTIONS].get()
        }
        myphotos.set_saved_data(data, _SAVED_DATA)
        # ---
        self._draw_selector_window(False)
        self._draw_progress_window(True)
        self.main.update()
        # ---
        func = filename_to_photo if data[_OMU_OPTIONS] == _OPTIONS[0] else photo_to_filename
        for p in func.main(data[_TXT_SOURCE], data[_TXT_TARGET]):
            self.update_progress(_TXB_PROGRESS, p)
        self.update_progress(_TXB_PROGRESS, '\nCompleted.')


# -----------------------------------------------


def main():
    """ Main function """
    win = tk.Tk()
    DateInterface(win).go()
    win.mainloop()


# -----------------------------------------------

if __name__ == '__main__':
    main()

# -----------------------------------------------
# End.
