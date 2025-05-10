import tkinter as tk
from datetime import datetime
from gui.number_entry import NumberEntry


class Popup(tk.Toplevel):
    def __init__(self, task_name: str, *args, fg_color = None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)
        self._start_year_var = tk.IntVar(value=datetime.now().year)
        self._start_month_var = tk.IntVar(value=datetime.now().month)
        self._start_day_var = tk.IntVar(value=datetime.now().day)
        self._end_year_var = tk.IntVar(value=datetime.now().year)
        self._end_month_var = tk.IntVar(value=datetime.now().month)
        self._end_day_var = tk.IntVar(value=datetime.now().day)

        self.task_name = task_name
        tk.Label(self, text="Starts At").pack()

        sf = tk.Frame(self)
        sf.pack()

        NumberEntry(sf, self._start_year_var, min_val=1900, max_val=2099, step=1).pack(side="left")
        NumberEntry(sf, self._start_month_var, min_val=1, max_val=12, step=1).pack(side="left")
        NumberEntry(sf, self._start_day_var, min_val=1, max_val=31, step=1).pack(side="left")

        tk.Label(self, text="Ends At").pack()

        ef = tk.Frame(self)
        ef.pack()

        NumberEntry(ef, self._end_year_var, min_val=1900, max_val=2099, step=1).pack(side="left")
        NumberEntry(ef, self._end_month_var, min_val=1, max_val=12, step=1).pack(side="left")
        NumberEntry(ef, self._end_day_var, min_val=1, max_val=31, step=1).pack(side="left")
