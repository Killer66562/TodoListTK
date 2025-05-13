from .base import Base
from .number_input import NumberInput

from datetime import datetime

import tkinter as tk


class DateTimeRow(Base):
    def __init__(self, master):
        super().__init__(master)
        now = datetime.now()

        self._year_input = NumberInput(self.frame, 1900, 2100, now.year, label="年")
        self._year_input.frame.pack(side="left", expand=True, fill="x")
        
        self._month_input = NumberInput(self.frame, 1, 12, now.month, label="月")
        self._month_input.frame.pack(side="left", expand=True, fill="x")

        self._day_input = NumberInput(self.frame, 1, 31, now.day, label="日")
        self._day_input.frame.pack(side="left", expand=True, fill="x")

        self._hour_input = NumberInput(self.frame, 0, 23, now.hour, label="時")
        self._hour_input.frame.pack(side="left", expand=True, fill="x")

        self._minute_input = NumberInput(self.frame, 0, 59, now.minute, label="分")
        self._minute_input.frame.pack(side="left", expand=True, fill="x")

    def get_dt(self) -> datetime:
        year = self._year_input.get()
        month = self._month_input.get()
        day = self._day_input.get()
        hour = self._hour_input.get()
        minute = self._minute_input.get()

        try:
            dt = datetime(year, month, day, hour, minute)
            return dt
        except ValueError:
            self._day_input.set(day - 1)
            return self.get_dt()
        
    def set_dt(self, dt: datetime):
        self._year_input.set(dt.year)
        self._month_input.set(dt.month)
        self._day_input.set(dt.day)
        self._hour_input.set(dt.hour)
        self._minute_input.set(dt.minute)


if __name__ == "__main__":
    window = tk.Tk()

    dt_row = DateTimeRow(window)
    dt_row.frame.pack()

    def on_btn_clicked():
        print(dt_row.get_dt())

    def on_btn2_clicked():
        dt_row.set_dt(datetime.now())

    btn = tk.Button(window, text="Test", command=on_btn_clicked)
    btn.pack()

    btn2 = tk.Button(window, text="Test 2", command=on_btn2_clicked)
    btn2.pack()

    window.mainloop()