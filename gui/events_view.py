from datetime import datetime, timedelta
from events.listener import EventListener
from tkinter import messagebox, ttk
from enums.enums import DB_URL

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models.models import Activity, Tag

import tkinter as tk


class EventsView:
    def __init__(self, master):
        self.engine = create_engine(DB_URL)
        self.selected_activity_id = None
        self.current_date = None

        self.frame = tk.Frame(master)
        
        self.treeview = ttk.Treeview(self.frame, selectmode="browse")
        self.treeview.pack(side="left", fill="both", expand=True)
        self.treeview["columns"] = ("1", "2", "3", "4")
        self.treeview["show"] = "headings"
        self.treeview.column("1", width=30, stretch=False, anchor="center")
        self.treeview.column("2", width=120, stretch=False)
        self.treeview.column("3", width=120, stretch=False)
        self.treeview.column("4", stretch=True)
        self.treeview.heading("1", text="#")
        self.treeview.heading("2", text="開始時間")
        self.treeview.heading("3", text="結束時間")
        self.treeview.heading("4", text="內容")

        for i in range(100):
            self.treeview.insert("", "end", values=("N", "i"))

        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.treeview.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.treeview.bind("<ButtonRelease-1>", self.on_tree_selected)

    def on_tree_selected(self, _):
        current = self.treeview.focus()
        item = self.treeview.item(current)
        values = item.get('values')
        if not values:
            self.selected_activity_id = None
        else:
            activity_id = values[0]
            self.selected_activity_id = int(activity_id)

    def clear(self):
        for child in self.treeview.get_children():
            self.treeview.delete(child)
        self.treeview.update()

    def load_events(self, date: datetime, tag: str | None = None):
        self.clear()
        self.current_date = date
        with Session(self.engine) as session:
            query = session.query(Activity).filter(Activity.ends_at >= date).filter(Activity.ends_at < date + timedelta(days=1))
            if tag:
                query = query.join(Tag, Activity.tags).filter(Tag.name == tag)
            activities = query.all()
            for activity in activities:
                self.treeview.insert("", "end", values=(activity.id_, activity.starts_at, activity.ends_at, activity.name))

    def add_event(self, starts_at: datetime, ends_at: datetime, description: str, tags: list[str] | None = None):
        try:
            with Session(self.engine) as session:
                activity = Activity(
                    starts_at=starts_at, 
                    ends_at=ends_at,
                    name=description
                )
                session.add(activity)
                session.commit()
                messagebox.showinfo("成功", "活動新增成功")
                starts_at = datetime.strftime(starts_at, "%Y-%m-%d %H:%M")
                ends_at = datetime.strftime(ends_at, "%Y-%m-%d %H:%M")
                self.treeview.insert("", "end", values=(activity.id_, starts_at, ends_at, description))
        except ValueError:
            messagebox.showerror("錯誤", "日期格式錯誤")
        except Exception as e:
            print(e)
            messagebox.showerror("錯誤", "資料庫錯誤")

    def remove_event(self):
        if not self.selected_activity_id:
            messagebox.showwarning("警告", "請選擇一個活動")
            return
        try:
            with Session(self.engine) as session:
                activity = session.query(Activity).filter(Activity.id_ == self.selected_activity_id).first()
                session.delete(activity)
                session.commit()
                messagebox.showinfo("成功", "活動刪除成功")
                self.selected_activity_id = None
                self.load_events(self.current_date)
        except ValueError:
            messagebox.showerror("錯誤", "日期格式錯誤")
        except Exception as e:
            print(e)
            messagebox.showerror("錯誤", "資料庫錯誤")