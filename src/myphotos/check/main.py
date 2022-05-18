#!/usr/bin/python3
# -----------------------------------------------
"""
    DESCRIPTION:
        Interface to launch the check data function.

    ASSUMPTIONS:
        No assumptions to note

    ACCURACY:
        No accuracy issues to note
"""
# -----------------------------------------------

import tkinter as tk

import myphotos.check.data

# -----------------------------------------------

_BOK_PROGRESS = 'bok_progress'
_BOK_SELECTOR = 'bok_selector'
_FRM_PROGRESS = 'frm_progress'
_FRM_SELECTOR = 'frm_select'
_TXB_PROGRESS = 'txb_progress'
_TXT_SOURCE = 'txt_source'

_SAVED_DATA = 'check'

# -----------------------------------------------


class _CheckInterface(myphotos.MyPhotosWindow):
    """ Date tkinter interface """

    def __init__(self, win):
        """ Initialises the date interface """

        super().__init__(win, myphotos.CHECK)
        self.initialise_elements()
        self.draw_selector_window(True)

    # -------------------------------------------

    def draw_progress_window(self, show):
        """ Packs the progress window objects """

        self.elements[_TXB_PROGRESS].delete('1.0', tk.END)

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

        self.elements[_FRM_SELECTOR] = tk.Frame(self.main)
        self.create_directory_selector(self.elements[_FRM_SELECTOR], _TXT_SOURCE, 'Source')
        self.create_ok_button(_BOK_SELECTOR, self.ok_selector)

        data = myphotos.get_saved_data(_SAVED_DATA)
        self.elements[_TXT_SOURCE].config(text=data.get(_TXT_SOURCE, ''))

        self.elements[_FRM_PROGRESS] = tk.Frame(self.main)
        self.create_progress_box(self.elements[_FRM_PROGRESS], _TXB_PROGRESS)
        self.create_ok_button(_BOK_PROGRESS, self.ok_progress)

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
        self.draw_progress_window(True)
        # ---
        for p in myphotos.check.data.main(data[_TXT_SOURCE]):
            self.update_progress(_TXB_PROGRESS, p)
        self.update_progress(_TXB_PROGRESS, '\nCompleted.')


# -----------------------------------------------


def main():
    """ Main function """
    win = tk.Tk()
    _CheckInterface(win)
    win.mainloop()


# -----------------------------------------------

if __name__ == '__main__':
    main()

# -----------------------------------------------
# End.
