#!/usr/bin/python3
# -----------------------------------------------
"""
    DESCRIPTION:
        Main launch window

    ASSUMPTIONS:
        No assumptions to note

    ACCURACY:
        No accuracy issues to note
"""
# -----------------------------------------------

import tkinter as tk

import myphotos.check.main
import myphotos.dates.main
import myphotos.descs.main
import myphotos.geos.main

# -----------------------------------------------

_FRM_LAUNCH = 'frm_launch'

_STEPS = {
    1: {'label': myphotos.DATES, 'command': myphotos.dates.main.DateInterface},
    2: {'label': myphotos.DESCS, 'command': myphotos.descs.main.DescInterface},
    3: {'label': myphotos.GEOS, 'command': myphotos.geos.main.GeoInterface},
    4: {'label': myphotos.CHECK, 'command': myphotos.check.main.CheckInterface}
}

# -----------------------------------------------


class _LaunchInterface(myphotos.MyPhotosWindow):
    """ Date tkinter interface """

    def __init__(self, win):
        """ Initialises the date interface """

        super().__init__(win, 'Launch')
        super().go(buttons=False)

        self.win = win

        # ---

        self.steps = {}
        for step in _STEPS:
            self.steps[step] = _STEPS[step]['command'](self.win, self.main)

        # ---

        self.elements[_FRM_LAUNCH] = tk.Frame(self.main, pady=20)
        for step, v in _STEPS.items():
            tk.Button(
                master=self.elements[_FRM_LAUNCH],
                text=f"{step}: {v['label']}",
                bg=myphotos.BG.get(v['label'], myphotos.BG['default']),
                width=20,
                height=5,
                command=lambda s=step: self.launch(s)
            ).pack(side=tk.LEFT, padx=10, pady=10)

        self.elements[_FRM_LAUNCH].pack()

    # -------------------------------------------

    def launch(self, step):
        """ Launches the specified step"""

        self.main.pack_forget()
        self.steps[step].go()


# -----------------------------------------------

def main():
    """ Main function """
    win = tk.Tk()
    _LaunchInterface(win)
    win.mainloop()


# -----------------------------------------------

if __name__ == '__main__':
    main()

# -----------------------------------------------
# End.
