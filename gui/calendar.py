import tkinter as tk
from tkinter import messagebox, font
from tkcalendar import Calendar
import datetime

from events.listener import EventListener
from events.events import Event
from enums.enums import EventType, DB_URL
from events.data import FontSizeChangedData

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from gui.events_view import EventsView
from models.models import Activity, Tag


class CalendarFrame(EventListener):
    def __init__(self, master=None):
        super().__init__()
        self.engine = create_engine(DB_URL)
        self.frame = tk.Frame(master)

        self.current_font_size = 10
        self.base_font = font.Font(size=self.current_font_size)

        self.starts_at_var = tk.StringVar()
        self.ends_at_var = tk.StringVar()
        self.desc_var = tk.StringVar()

        self.top_frame = tk.Frame(self.frame)
        self.top_frame.pack(side="top", fill="x")

        self.top_left_frame = tk.Frame(self.top_frame)
        self.top_left_frame.pack(side="left", fill="x", expand=True)

        self.top_right_frame = tk.Frame(self.top_frame)
        self.top_right_frame.pack(side="right", fill="x", expand=True)

        tk.Label(self.top_left_frame, text="開始時間 (YYYY-MM-DD HH:MM):", font=self.base_font).pack(anchor="w")
        tk.Entry(self.top_left_frame, textvariable=self.starts_at_var, font=self.base_font).pack(fill="x", expand=True)
        tk.Label(self.top_right_frame, text="結束時間 (YYYY-MM-DD HH:MM):", font=self.base_font).pack(anchor="w")
        tk.Entry(self.top_right_frame, textvariable=self.ends_at_var, font=self.base_font).pack(fill="x", expand=True)

        tk.Label(self.frame, text="活動描述：", font=self.base_font).pack(anchor="w")
        tk.Entry(self.frame, textvariable=self.desc_var, font=self.base_font).pack(fill="x")

        self.btns_frame = tk.Frame(self.frame)
        self.btns_frame.pack(fill="x")

        tk.Button(self.btns_frame, text="新增活動", command=self.add_event, font=self.base_font).pack(side="left")
        tk.Button(self.btns_frame, text="刪除活動", command=self.delete_event, font=self.base_font).pack(side="left")
        tk.Button(self.btns_frame, text="查看所有活動", command=self.view_events, font=self.base_font).pack(side="left")

        today = datetime.date.today()

        self.calendar = Calendar(self.frame, selectmode='day', year=today.year, month=today.month, day=today.day, date_pattern="y-mm-dd")
        self.calendar.bind("<<CalendarSelected>>", self.on_day_selected)
        self.calendar.pack(fill="both", padx=5, pady=5)

        self.events_label = tk.Label(self.frame, text="今日活動")
        self.events_label.pack(anchor="w")

        self.events_view = EventsView(self.frame)
        self.events_view.frame.pack(fill="both", expand=True)

        self.add_handler(EventType.FS_CHANGED, self.on_fs_changed)
        self.on_day_selected(None)

    def on_day_selected(self, _):
        date = self.calendar.get_date()
        dt = datetime.datetime.strptime(date, "%Y-%m-%d")
        self.events_view.load_events(dt)

    def add_event(self):
        starts_at = self.starts_at_var.get()
        ends_at = self.ends_at_var.get()
        desc = self.desc_var.get()

        if not starts_at or not ends_at or not desc:
            messagebox.showwarning("輸入錯誤", "請填寫所有欄位。")
            return

        try:
            starts_at = datetime.datetime.strptime(starts_at, '%Y-%m-%d %H:%M')
            ends_at = datetime.datetime.strptime(ends_at, '%Y-%m-%d %H:%M')
        except ValueError:
            messagebox.showwarning("輸入錯誤", "日期格式錯誤，請使用 YYYY-MM-DD HH:MM。")
            return
        
        try:
            self.events_view.add_event(starts_at, ends_at, desc)
        except:
            pass

    def delete_event(self):
        try:
            self.events_view.remove_event()
        except:
            pass

    def view_events(self):
        if not self.events:
            messagebox.showinfo("目前無事件", "您尚未新增任何事件。")
        else:
            all_events = "\n".join([f"{d} {t}:{desc}" for (d, t), desc in self.events.items()])
            messagebox.showinfo("所有事件", all_events)

    def clear_inputs(self):
        self.date_var.set("")
        self.time_var.set("")
        self.desc_var.set("")

    def on_fs_changed(self, data: FontSizeChangedData):
        self.current_font_size = data.font_size
        self.base_font.configure(size=self.current_font_size)
        for widget in self.frame.winfo_children():
            if isinstance(widget, (tk.Label, tk.Entry, tk.Button)):
                widget.configure(font=self.base_font)