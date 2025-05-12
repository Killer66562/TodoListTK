from datetime import datetime
from tkinter import messagebox
from events.events import Event
from gui.calendar import CalendarFrame
import tkinter as tk
from events.data import ActivitiesLoadData, ActivitiesLoadedData, ActivityAddData, ActivityAddedData, ActivityRemoveData, ActivityRemovedData, EventData, InputRowBtnClickedData, TagAddData, TagAddedData
from events.listener import EventListener
from enums.enums import EventType
from gui.add_tag import AddTag
from gui.sidebar import Sidebar
from gui.settings import Settings
from gui.all import AllFrame
from gui.today import TodayFrame
from gui.preview import PreviewFrame

from db.manager import DatabaseManager


class TodoList(EventListener):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager("sqlite:///database.sqlite3")

        self.window = tk.Tk()
        self.window.title("TodoList")
        self.window.minsize(800, 600)

        self.sidebar = Sidebar(self.window)
        self.sidebar.frame.pack(side="left", fill="y")

        self.settings = Settings(self.window)
        self.calendar = CalendarFrame(self.window)
        self.index = AllFrame(self.window)
        self.today = TodayFrame(self.window)
        self.preview = PreviewFrame(self.window)

        self.current_frame = None

        #按鍵事件
        self.add_handler(EventType.TAG_ADD_BTN_CLICKED, self.on_add_tag_btn_clicked_event)
        self.add_handler(EventType.CALANDER_BTN_CLICKED, self.on_calendar_btn_clicked)
        self.add_handler(EventType.SETTINGS_BTN_CLICKED, self.on_settings_btn_clicked)
        self.add_handler(EventType.INDEX_BTN_CLICKED, self.on_index_btn_clicked)
        self.add_handler(EventType.TODAY_BTN_CLICKED, self.on_today_btn_clicked)
        self.add_handler(EventType.PREVIEW_BTN_CLICKED, self.on_preview_btn_clicked)

        #資料庫交互事件
        self.add_handler(EventType.ACTIVITY_ADD, self.on_activity_add)
        self.add_handler(EventType.ACTIVITIES_LOAD, self.on_activities_load)
        self.add_handler(EventType.TAG_ADD, self.on_tag_add)
        self.add_handler(EventType.ACTIVITY_REMOVE, self.on_activity_remove)

    #收到新增活動的事件時要做的事
    def on_activity_add(self, data: ActivityAddData):
        try:
            activity = self.db_manager.add_activity(
                data.description, 
                data.starts_at, 
                data.ends_at
            )
            event = Event(EventType.ACTIVITY_ADDED, activity)
            messagebox.showinfo("成功", "活動新增成功")
            event.emit()
        except:
            messagebox.showerror("錯誤", "資料庫錯誤")

    def on_activity_remove(self, data: ActivityRemoveData):
        try:
            self.db_manager.remove_activity(data.activity_id)
            event = Event(EventType.ACTIVITY_REMOVED, ActivityRemovedData(data.activity_id))
            messagebox.showinfo("成功", "活動刪除成功")
            event.emit()
        except Exception as e:
            messagebox.showerror("錯誤", "資料庫錯誤")

    #收到新增標籤的事件時要做的事
    def on_tag_add(self, data: TagAddData):
        try:
            tag = self.db_manager.add_tag(data.name)
            event = Event(EventType.TAG_ADDED, tag)
            messagebox.showinfo("成功", "活動新增成功")
            event.emit()
        except:
            messagebox.showerror("錯誤", "資料庫錯誤")

    def on_activities_load(self, data: ActivitiesLoadData):
        try:
            activities = self.db_manager.get_activities(data.dt, data.dt, data.tags)
            event = Event(EventType.ACTIVITIES_LOADED, ActivitiesLoadedData(activities))
            event.emit()
        except:
            messagebox.showerror("錯誤", "資料庫錯誤")

    def switch_frame(self, frame: tk.Frame):
        if self.current_frame is frame:
            return
        if self.current_frame:
            self.current_frame.pack_forget()
            self.current_frame.update()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True)

    def on_index_btn_clicked(self, data: EventData):
        self.index.load_all_events()
        self.switch_frame(self.index.frame)

    def on_today_btn_clicked(self, data: EventData):
        self.today.load_today_events()
        self.switch_frame(self.today.frame)

    def on_settings_btn_clicked(self, data: EventData):
        self.switch_frame(self.settings.frame)

    def on_add_tag_btn_clicked_event(self, data: EventData):
        if not self.add_tag:
            self.add_tag = AddTag(self.window)
            self.add_tag.window.bind("<Destroy>", self.on_add_tag_destroy)
            self.add_tag.window.focus()
            self.add_tag.window.mainloop()

    def on_calendar_btn_clicked(self, data: EventData):
        self.switch_frame(self.calendar.frame)

    def on_preview_btn_clicked(self, data: EventData):
        self.preview.load_preview_events()
        self.switch_frame(self.preview.frame)

    def on_add_tag_destroy(self, _):
        self.add_tag = None

    def run(self):
        event = Event(EventType.ACTIVITIES_LOAD, ActivitiesLoadData(datetime.today(), None))
        event.emit()

        self.switch_frame(self.calendar.frame)
        self.window.mainloop()


app = TodoList()
app.run()