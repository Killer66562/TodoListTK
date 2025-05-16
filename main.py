from datetime import date, datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from db.manager import DatabaseManager

from ui.filter_row import FilterRow
from ui.sidebar import SideBar
from ui.my_calendar import MyCalendar
from ui.activity_form import ActivityForm
from ui.activities_view import ActivitiesView

from ui.styles_setting import create_light_style, create_dark_style
from ui.settings_frame import SettingsFrame


class TodoList:
    def __init__(self):
        self._db_manager = DatabaseManager("sqlite:///database.sqlite3")

        self._current_frame: tk.Frame | None = None

        self._window = tk.Tk()
        self._window.title("TodoList")
        self._window.minsize(800, 600)
        
        # 測試主題~
        create_dark_style()
        create_light_style()
        ttk.Style().theme_use("light")

        self._main_frame = tk.Frame(self._window)

        self._sidebar = SideBar(
            self._window, 
            self.on_sidebar_add_tag_btn_clicked, 
            self.on_sidebar_all_btn_clicked, 
            self.on_sidebar_today_btn_clicked, 
            self.on_sidebar_settings_btn_clicked
        )
        self._sidebar.frame.configure(width=200)
        self._sidebar.frame.pack_propagate(False)
        self._sidebar.frame.pack(side="left", fill="y")

        self._activity_form = ActivityForm(
            self._main_frame, 
            self.on_activity_form_add_btn_clicked, 
            self.on_activity_form_delete_btn_clicked, 
            self.on_activity_form_modify_btn_clicked, 
            self.on_activity_form_cancel_btn_clicked
        )
        self._activity_form.frame.pack(side="top", fill="x")

        self._my_calendar = MyCalendar(self._main_frame, self.on_calander_date_selected)
        self._my_calendar.frame.pack(side="top", fill="x")

        self._filter_row = FilterRow(self._main_frame, self.on_filter_row_option_changed)
        self._filter_row.frame.pack(anchor="e")

        self._activities_view = ActivitiesView(self._main_frame, self.on_activities_view_activity_selected)
        self._activities_view.frame.pack(side="top", fill="both", expand=True)

        self._settings = SettingsFrame(self._window)

    def _switch_frame(self, frame: tk.Frame):
        if self._current_frame:
            self._current_frame.pack_forget()
        self._current_frame = frame
        self._current_frame.pack(side="top", fill="both", expand=True)

    def _reload_components(self):
        d = self._my_calendar.get_date()
        starts_at = datetime(d.year, d.month, d.day, 9, 0)
        ends_at = datetime(d.year, d.month, d.day, 17, 0)
        self._activity_form.reset(starts_at, ends_at)
        self._sidebar.reset_filter()
        all_activities = self._db_manager.get_activities()
        for activity in all_activities:
            d_start = activity.starts_at.date()
            d_end = activity.ends_at.date()
            tag_start = str(activity.id_) + "_start"
            tag_end = str(activity.id_) + "_end"
            self._my_calendar.calendar.calevent_create(date=d_start, text=None, tags=[tag_start])
            self._my_calendar.calendar.calevent_create(date=d_end, text=None, tags=[tag_end])
            self._my_calendar.calendar.tag_config(tag_start, background="green")
            self._my_calendar.calendar.tag_config(tag_end, background="red")
        self.update_activities_view(d)

    def update_activities_view(self, d: date | None):
        done = self._filter_row.get()
        filt = self._sidebar.get_filter()
        if filt == "all":
            activities = self._db_manager.get_activities(None, done=done)
        elif filt == "today":
            today = date.today()
            activities = self._db_manager.get_activities(today, done=done)
        elif filt == "recent":
            activities = []
        else:
            activities = self._db_manager.get_activities(d, done=done)
        self._activities_view.clear()
        for activity in activities:
            self._activities_view.add_activity(activity)

    def on_activity_form_add_btn_clicked(self, starts_at: datetime, ends_at: datetime, description: str):
        try:
            self._db_manager.add_activity(description, starts_at, ends_at)
            messagebox.showinfo("成功", "活動新增成功")
            d = self._my_calendar.get_date()
            starts_at = datetime(d.year, d.month, d.day, 9, 0)
            ends_at = datetime(d.year, d.month, d.day, 17, 0)
            self._activity_form.reset(starts_at, ends_at)
            self._reload_components()
        except:
            messagebox.showerror("錯誤", "資料庫錯誤")

    def on_activity_form_delete_btn_clicked(self, id_: int):
        confirm = messagebox.askyesno("確認", "你確定要刪除這個活動嗎")
        if not confirm:
            return
        try:
            self._db_manager.remove_activity(id_)
            messagebox.showinfo("成功", "活動刪除成功")
            self._reload_components()
        except:
            messagebox.showerror("錯誤", "資料庫錯誤")

    def on_activity_form_modify_btn_clicked(self, id_: int, starts_at: datetime, ends_at: datetime, description: str, done: bool):
        try:
            self._db_manager.modify_activity(id_, description, starts_at, ends_at, done)
            messagebox.showinfo("成功", "活動修改成功")
            self._reload_components()
        except Exception as e:
            print(e)
            messagebox.showerror("錯誤", "資料庫錯誤")

    def on_activity_form_cancel_btn_clicked(self):
        d = self._my_calendar.get_date()
        starts_at = datetime(d.year, d.month, d.day, 0, 0)
        ends_at = datetime(d.year, d.month, d.day, 17, 0)
        self._activity_form.reset(starts_at, ends_at)

    def on_calander_date_selected(self):
        '''
        activity_form的起始和結束設成日曆那天
        清掉sidebar的狀態
        '''
        d = self._my_calendar.get_date()
        starts_at = datetime(d.year, d.month, d.day, 9, 0)
        ends_at = datetime(d.year, d.month, d.day, 17, 0)
        self._activity_form.set_starts_at(starts_at)
        self._activity_form.set_ends_at(ends_at)
        self._sidebar.reset_filter()
        self.update_activities_view(d)

    def on_filter_row_option_changed(self, done: bool | None):
        '''
        
        '''
        d = self._my_calendar.get_date()
        self.update_activities_view(d)

    def on_activities_view_activity_selected(self, activity_id: int | None):
        if activity_id:
            activity = self._db_manager.get_activity(activity_id)
            self._activity_form.set_activity(activity)
            self._activity_form.set_starts_at(activity.starts_at)
            self._activity_form.set_ends_at(activity.ends_at)
            self._activity_form.set_description(activity.description)
            self._activity_form.set_done(activity.done)

    def on_sidebar_add_tag_btn_clicked(self, tag_name: str):
        if self._current_frame is not self._main_frame:
            self._switch_frame(self._main_frame)
        try:
            self._db_manager.add_tag(tag_name)
            messagebox.showinfo("成功", "標籤新增成功")
            tags = self._db_manager.get_tags()
            self._sidebar.set_tag_btns(tags, self.on_tag_find, self.on_tag_delete)
        except ValueError:
            messagebox.showerror("錯誤", "已存在同名的標籤")
        except Exception as e:
            print(e)
            messagebox.showerror("錯誤", "資料庫錯誤")

    def on_sidebar_settings_btn_clicked(self):
        if self._current_frame is self._settings.frame:
            self._switch_frame(self._main_frame)
        else:
            self._switch_frame(self._settings.frame)

    def on_tag_find(self, name: str):
        try:
            tag = self._db_manager.get_tag(name)
            print(tag)
        except:
            messagebox.showerror("錯誤", "資料庫錯誤")

    def on_tag_delete(self, name: str):
        try:
            self._db_manager.remove_tag(name)
            messagebox.showinfo("成功", "標籤刪除成功")
            tags = self._db_manager.get_tags()
            self._sidebar.set_tag_btns(tags, self.on_tag_find, self.on_tag_delete)
        except:
            messagebox.showerror("錯誤", "資料庫錯誤")

    def on_sidebar_all_btn_clicked(self):
        if self._current_frame is not self._main_frame:
            self._switch_frame(self._main_frame)
        try:
            self.update_activities_view(None)
        except:
            messagebox.showerror("錯誤", "資料庫錯誤")

    def on_sidebar_today_btn_clicked(self):
        if self._current_frame is not self._main_frame:
            self._switch_frame(self._main_frame)
        try:
            today = date.today()
            starts_at = datetime(today.year, today.month, today.day, 9, 0)
            ends_at = datetime(today.year, today.month, today.day, 17, 0)
            self._activity_form.set_starts_at(starts_at)
            self._activity_form.set_ends_at(ends_at)
            self._my_calendar.set_date(today)
            self.update_activities_view(today)
        except:
            messagebox.showerror("錯誤", "資料庫錯誤")

    def on_sidebar_recent_btn_clicked(self):
        if self._current_frame is not self._main_frame:
            self._switch_frame(self._main_frame)
        try:
            today = date.today()
            self.update_activities_view(today)
        except:
            messagebox.showerror("錯誤", "資料庫錯誤")

    def run(self):
        self._reload_components()

        create_dark_style()
        create_light_style()

        tags = self._db_manager.get_tags()
        self._sidebar.set_tag_btns(tags, self.on_tag_find, self.on_tag_delete)

        self._switch_frame(self._main_frame)
        self._window.mainloop()

app = TodoList()
app.run()