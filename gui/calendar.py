import tkinter as tk
from tkinter import messagebox, font
from tkcalendar import Calendar
import datetime

from events.listener import EventListener
from enums.enums import EventType
from events.events import Event
from events.data import ActivitiesLoadData, ActivityAddData, ActivityRemoveData, ActivityRemovedData, ActivitySelectedData, FontSizeChangedData

from gui.events_view import EventsView


class CalendarFrame(EventListener):
    def __init__(self, master):
        super().__init__()
        self._selected_activity_id = None

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
        self.delete_btn = tk.Button(self.btns_frame, text="刪除活動", command=self.delete_event, font=self.base_font, state="disabled")
        self.delete_btn.pack(side="left")
        tk.Button(self.btns_frame, text="查看所有活動", command=self.view_events, font=self.base_font).pack(side="left")
        tk.Button(self.btns_frame, text="回到今天", command=self.to_today, font=self.base_font).pack(side="left")

        today = datetime.date.today()

        self.tips = tk.Label(self.frame, fg="#bb3300", text="提示：點擊行事曆的日期，可以查看當天的活動。")
        self.tips.pack(anchor="w")

        self.calendar = Calendar(self.frame, selectmode='day', year=today.year, month=today.month, day=today.day, date_pattern="y-mm-dd")
        self.calendar.bind("<<CalendarSelected>>", self.on_day_selected)
        self.calendar.pack(fill="both", padx=5, pady=5)

        self.events_label = tk.Label(self.frame, text="今日活動")
        self.events_label.pack(anchor="w")

        self.events_view = EventsView(self.frame)
        self.events_view.frame.pack(fill="both", expand=True)

        self.add_handler(EventType.ACTIVITY_SELECTED, self.on_activity_selected)
        self.add_handler(EventType.ACTIVITY_REMOVED, self.on_activity_removed)

    def to_today(self):
        today = datetime.datetime.today()
        self.calendar.selection_set(
            today
        )
        self.on_day_selected(None)

    def on_activity_selected(self, data: ActivitySelectedData):
        self._selected_activity_id = data.id_
        if not self._selected_activity_id:
            self.delete_btn.configure(state="disabled")
        else:
            self.delete_btn.configure(state="normal")

    def on_activity_removed(self, data: ActivityRemovedData):
        self._selected_activity_id = None
        self.on_day_selected(None)

    def on_day_selected(self, _):
        self.on_activity_selected(ActivitySelectedData(None))
        date = self.calendar.get_date()
        dt = datetime.datetime.strptime(date, "%Y-%m-%d")
        event = Event(EventType.ACTIVITIES_LOAD, ActivitiesLoadData(dt))
        event.emit()

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
        
        event = Event(EventType.ACTIVITY_ADD, ActivityAddData(starts_at, ends_at, desc))
        event.emit()

    def delete_event(self):
        if not self._selected_activity_id:
            messagebox.showwarning("警告", "請選擇你要刪除的活動")
            return
        event = Event(EventType.ACTIVITY_REMOVE, ActivityRemoveData(self._selected_activity_id))
        event.emit()

    def view_events(self):
        if not self.events:
            messagebox.showinfo("目前無事件", "您尚未新增任何事件。")
        else:
            all_events = "\n".join([f"{d} {t}:{desc}" for (d, t), desc in self.events.items()])
            messagebox.showinfo("所有事件", all_events)

    def clear_inputs(self):
        self.starts_at_var.set("")
        self.ends_at_var.set("")
        self.desc_var.set("")

    def on_fs_changed(self, data: FontSizeChangedData):
        self.current_font_size = data.font_size
        self.base_font.configure(size=self.current_font_size)
        for widget in self.frame.winfo_children():
            if isinstance(widget, (tk.Label, tk.Entry, tk.Button)):
                widget.configure(font=self.base_font)