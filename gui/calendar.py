import tkinter as tk
from tkinter import messagebox, font
from tkcalendar import Calendar
import datetime

from events.listener import EventListener
from events.events import Event
from enums.enums import EventType
from events.data import FontSizeChangedData


class CalendarFrame(EventListener):
    def __init__(self, master=None):
        super().__init__()
        self.frame = tk.Frame(master)
        self.events = {}

        self.current_font_size = 10
        self.base_font = font.Font(size=self.current_font_size)

        self.calendar = Calendar(self.frame, selectmode='day', year=2025, month=1, day=1)
        self.calendar.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.date_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.desc_var = tk.StringVar()

        tk.Label(self.frame, text="事件日期 (YYYY-MM-DD):", font=self.base_font).grid(row=1, column=0, sticky="e")
        tk.Entry(self.frame, textvariable=self.date_var, font=self.base_font).grid(row=1, column=1)

        tk.Label(self.frame, text="事件時間 (HH:MM 上午/下午):", font=self.base_font).grid(row=2, column=0, sticky="e")
        tk.Entry(self.frame, textvariable=self.time_var, font=self.base_font).grid(row=2, column=1)

        tk.Label(self.frame, text="事件描述：", font=self.base_font).grid(row=3, column=0, sticky="e")
        tk.Entry(self.frame, textvariable=self.desc_var, font=self.base_font).grid(row=3, column=1)

        tk.Button(self.frame, text="新增事件", command=self.add_event, font=self.base_font).grid(row=4, column=0, pady=10)
        tk.Button(self.frame, text="刪除事件", command=self.delete_event, font=self.base_font).grid(row=4, column=1, pady=10)
        tk.Button(self.frame, text="查看所有事件", command=self.view_events, font=self.base_font).grid(row=4, column=2, pady=10)

    def add_event(self):
        date = self.date_var.get()
        time = self.time_var.get()
        desc = self.desc_var.get()

        if not date or not time or not desc:
            messagebox.showwarning("輸入錯誤", "請填寫所有欄位。")
            return

        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("輸入錯誤", "日期格式錯誤，請使用 YYYY-MM-DD。")
            return

        self.events[(date, time)] = desc
        messagebox.showinfo("新增成功", f"事件「{desc}」已新增至 {date} {time}。")
        self.clear_inputs()

    def delete_event(self):
        date = self.date_var.get()
        time = self.time_var.get()

        if not date or not time:
            messagebox.showwarning("輸入錯誤", "請輸入日期與時間以刪除事件。")
            return

        if (date, time) in self.events:
            del self.events[(date, time)]
            messagebox.showinfo("刪除成功", f"已刪除 {date} {time} 的事件。")
        else:
            messagebox.showwarning("找不到事件", "找不到指定的事件。")
        self.clear_inputs()

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

    def on_event(self, event: Event):
        if event.type == EventType.FS_CHANGED:
            fs_data = event.data
            if isinstance(fs_data, FontSizeChangedData):
                self.current_font_size = fs_data.font_size
                self.base_font.configure(size=self.current_font_size)
                for widget in self.frame.winfo_children():
                    if isinstance(widget, (tk.Label, tk.Entry, tk.Button)):
                        widget.configure(font=self.base_font)