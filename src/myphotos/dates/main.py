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

_BOK_SELECTOR = 'bok_selector'
_BTN_SOURCE = 'btn_source'
_BTN_TARGET = 'btn_target'
_FRM_SELECTOR = 'frm_select'
_OMU_OPTIONS = 'omu_options'
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
        self.draw_selector_window()

    # -------------------------------------------

    def draw_selector_window(self):
        """ Packs the selector window objects """

        self.elements[_FRM_SELECTOR].pack(anchor=tk.N, side=tk.LEFT)
        self.elements[_BOK_SELECTOR].pack(side=tk.RIGHT)

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

    # -------------------------------------------

    def ok_selector(self):
        """ OK button command for the selector frame """

        data = {
            _TXT_SOURCE: self.elements[_TXT_SOURCE].cget('text'),
            _TXT_TARGET: self.elements[_TXT_TARGET].cget('text'),
            _OMU_OPTIONS: self.elements[_OMU_OPTIONS].get()
        }
        myphotos.set_saved_data(data, _SAVED_DATA)


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
