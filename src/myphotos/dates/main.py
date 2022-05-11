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

_OPTIONS = ['Photo to Filename', 'Filename to Photo']
_SAVED_DATA = 'dates'

# -----------------------------------------------


class _DateInterface(myphotos.MyPhotosWindow):
    """ Date tkinter interface """

    def __init__(self, win):
        """ Initialises the date interface """

        super().__init__(win, 'Dates')
        self.initialise_elements()
        self.draw_selector_window(True)

    # -------------------------------------------

    def draw_progress_window(self, show):
        """ Packs the selector window objects """

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
        self._create_directory_selector(self.elements[_FRM_SELECTOR], _TXT_TARGET, 'Target')
        self._create_options_menu(self.elements[_FRM_SELECTOR], _OMU_OPTIONS, _OPTIONS)
        self._create_ok_button(_BOK_SELECTOR, self.ok_selector)

        data = myphotos.get_saved_data(_SAVED_DATA)
        self.elements[_TXT_SOURCE].config(text=data.get(_TXT_SOURCE, ''))
        self.elements[_TXT_TARGET].config(text=data.get(_TXT_TARGET, ''))
        self.elements[_OMU_OPTIONS].set(data.get(_OMU_OPTIONS, _OPTIONS[0]))

        self.elements[_FRM_PROGRESS] = tk.Frame(self.main, bg='yellow')
        self._create_progress_box(self.elements[_FRM_PROGRESS], _TXB_PROGRESS)
        self._create_ok_button(_BOK_PROGRESS, self.ok_progress)

    # -------------------------------------------

    def ok_progress(self):
        """ OK button command for the progress frame """

        self.draw_progress_window(False)
        self.draw_selector_window(True)

    # -------------------------------------------

    def ok_selector(self):
        """ OK button command for the selector frame """

        data = {
            _TXT_SOURCE: self.elements[_TXT_SOURCE].cget('text'),
            _TXT_TARGET: self.elements[_TXT_TARGET].cget('text'),
            _OMU_OPTIONS: self.elements[_OMU_OPTIONS].get()
        }
        myphotos.set_saved_data(data, _SAVED_DATA)
        # ---
        self.draw_selector_window(False)
        self.draw_progress_window(True)
        self.main.update()
        # ---
        func = filename_to_photo if _OMU_OPTIONS == _OPTIONS[0] else photo_to_filename
        for p in func.main(data[_TXT_SOURCE], data[_TXT_TARGET]):
            self._update_progress(_TXB_PROGRESS, p)
        self._update_progress(_TXB_PROGRESS, '\nCompleted.')


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
