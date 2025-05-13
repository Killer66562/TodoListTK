from datetime import datetime
import tkinter as tk
from tkinter import messagebox

from db.manager import DatabaseManager

from ui.sidebar import SideBar
from ui.my_calendar import MyCalendar
from ui.activity_form import ActivityForm
from ui.activities_view import ActivitiesView
from ui.tag import TagButton


class TodoList:
    def __init__(self):
        self._db_manager = DatabaseManager("sqlite:///database.sqlite3")

        self._current_frame: tk.Frame | None = None

        self._window = tk.Tk()
        self._window.title("TodoList")
        self._window.minsize(800, 600)

        self._main_frame = tk.Frame(self._window)
        self._settings_frame = tk.Frame(self._window)

        self._sidebar = SideBar(self._window, self.on_sidebar_add_tag_btn_clicked)
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

        self._activities_view = ActivitiesView(self._main_frame, self.on_activities_view_activity_selected)
        self._activities_view.frame.pack(side="top", fill="both", expand=True)

    def _switch_frame(self, frame: tk.Frame):
        if self._current_frame:
            self._current_frame.pack_forget()
        self._current_frame = frame
        self._current_frame.pack(side="top", fill="both", expand=True)

    def on_activity_form_add_btn_clicked(self, starts_at: datetime, ends_at: datetime, description: str):
        try:
            activity = self._db_manager.add_activity(description, starts_at, ends_at)
            messagebox.showinfo("成功", "活動新增成功")
            d = self._my_calendar.get_date()
            if starts_at.date() == d or ends_at.date() == d:
                self._activities_view.add_activity(
                    activity.id_, 
                    activity.starts_at, 
                    activity.ends_at, 
                    activity.description
                )
        except:
            messagebox.showerror("錯誤", "資料庫錯誤")

    def update_activities_view(self, dt: datetime):
        activities = self._db_manager.get_activities(dt, dt)
        self._activities_view.clear()
        for activity in activities:
            self._activities_view.add_activity(
                activity.id_, 
                activity.starts_at, 
                activity.ends_at, 
                activity.description
            )

    def on_activity_form_delete_btn_clicked(self, id_: int):
        try:
            self._db_manager.remove_activity(id_)
            messagebox.showinfo("成功", "活動刪除成功")
            d = self._my_calendar.get_date()
            dt = datetime(d.year, d.month, d.day)
            self.update_activities_view(dt)
        except:
            messagebox.showerror("錯誤", "資料庫錯誤")

    def on_activity_form_modify_btn_clicked(self, id_: int, starts_at: datetime, ends_at: datetime, description: str):
        try:
            self._db_manager.modify_activity(id_, description, starts_at, ends_at)
            messagebox.showinfo("成功", "活動新增成功")
            d = self._my_calendar.get_date()
            dt = datetime(d.year, d.month, d.day)
            self.update_activities_view(dt)
        except:
            messagebox.showerror("錯誤", "資料庫錯誤")

    def on_activity_form_cancel_btn_clicked(self):
        d = self._my_calendar.get_date()
        dt = datetime(d.year, d.month, d.day)
        self._activity_form.set_starts_at(dt)
        self._activity_form.set_ends_at(dt)
        self._activity_form.set_description("")

    def on_calander_date_selected(self):
        d = self._my_calendar.get_date()
        dt = datetime(d.year, d.month, d.day)
        self._activity_form.set_activity_id(None)
        self._activity_form.set_starts_at(dt)
        self._activity_form.set_ends_at(dt)
        self._activity_form.set_description("")
        self.update_activities_view(dt)

    def on_activities_view_activity_selected(self, activity_id: int | None):
        self._activity_form.set_activity_id(activity_id)
        if activity_id:
            activity = self._db_manager.get_activity(activity_id)
            self._activity_form.set_starts_at(activity.starts_at)
            self._activity_form.set_ends_at(activity.ends_at)
            self._activity_form.set_description(activity.description)

    def on_sidebar_add_tag_btn_clicked(self, tag_name: str):
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

    def run(self):
        self.on_calander_date_selected()

        tags = self._db_manager.get_tags()
        self._sidebar.set_tag_btns(tags, self.on_tag_find, self.on_tag_delete)

        self._switch_frame(self._main_frame)
        self._window.mainloop()

app = TodoList()
app.run()