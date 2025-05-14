from models.local import Activity
from .base import Base


from datetime import datetime, timedelta
from tkinter import ttk

import tkinter as tk


class ActivitiesView(Base):
    def __init__(self, master, on_activity_selected_cb):
        super().__init__(master)        
        self.treeview = ttk.Treeview(self.frame, selectmode="browse")
        self.treeview.pack(side="left", fill="both", expand=True)
        self.treeview["columns"] = ("1", "2", "3", "4", "5")
        self.treeview["show"] = "headings"
        self.treeview.column("1", width=30, stretch=False, anchor="center")
        self.treeview.column("2", width=120, stretch=False)
        self.treeview.column("3", width=120, stretch=False)
        self.treeview.column("4", stretch=True)
        self.treeview.column("5", width=60, stretch=False)
        self.treeview.heading("1", text="#")
        self.treeview.heading("2", text="開始時間")
        self.treeview.heading("3", text="結束時間")
        self.treeview.heading("4", text="內容")
        self.treeview.heading("5", text="已完成")

        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.treeview.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.treeview.bind("<ButtonRelease-1>", self.on_tree_selected)

        self.on_activity_selected_cb = on_activity_selected_cb

    def clear(self):
        for child in self.treeview.get_children():
            self.treeview.delete(child)
        self.treeview.update()

    def add_activity(self, activity: Activity):
        id_str = str(activity.id_)
        starts_at_str = activity.starts_at.strftime("%Y-%m-%d %H:%M")
        ends_at_str = activity.ends_at.strftime("%Y-%m-%d %H:%M")
        description = activity.description
        done_str = "✅" if activity.done else "❌"
        print(activity)
        self.treeview.insert("", "end", values=(id_str, starts_at_str, ends_at_str, description, done_str))

    def on_tree_selected(self, _):
        current = self.treeview.focus()
        item = self.treeview.item(current)
        values = item.get('values')
        if not values:
            activity_id = None
        else:
            activity_id = values[0]
            activity_id = int(activity_id)
        self.on_activity_selected_cb(activity_id)