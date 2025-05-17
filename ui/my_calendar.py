import tkinter as tk

from tkcalendar import Calendar
from .base import Base
from datetime import datetime, date, timedelta
from typing import Callable


class MyCalendar(Base):
    def __init__(self, master, on_date_selected_cb: Callable[[], None]):
        super().__init__(master)
        today = date.today()
        self._selected_date = today

        self.calendar = Calendar(self.frame, selectmode='day', year=today.year, month=today.month, day=today.day, date_pattern="y-mm-dd", selectbackground='#1E90FF')
        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected)
        self.calendar.pack(fill="both", expand=True, padx=5, pady=5)

        self._on_date_selected_cb = on_date_selected_cb
        
        
    def get_date(self) -> date:
        return self._selected_date
    
    def set_date(self, d: date):
        self.calendar.selection_set(d)
        self._selected_date = d
    
    def on_date_selected(self, _):
        d_str = self.calendar.get_date()
        d = datetime.strptime(d_str, "%Y-%m-%d").date()
        self._selected_date = d
        self._on_date_selected_cb()

if __name__ == "__main__":
    window = tk.Tk()

    def on_day_selected():
        d = my_calendar.get_date()
        d = d + timedelta(days=1)
        my_calendar.set_date(d)

    my_calendar = MyCalendar(window, on_day_selected)
    my_calendar.frame.pack(fill="both", expand=True)

    window.mainloop()