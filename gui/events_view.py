from datetime import datetime, timedelta
from tkinter import messagebox, ttk
from sqlalchemy.orm import Session

from enums.enums import EventType
from events.data import ActivitiesLoadedData, ActivityAddedData, ActivitySelectedData
from events.events import Event
from events.listener import EventListener
from models.db import Activity, Tag

import tkinter as tk


class EventsView(EventListener):
    def __init__(self, master):
        super().__init__()

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

        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.treeview.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.treeview.bind("<ButtonRelease-1>", self.on_tree_selected)

        self.add_handler(EventType.ACTIVITY_ADDED, self.on_activity_added)
        self.add_handler(EventType.ACTIVITIES_LOADED, self.on_activities_loaded)

    def on_activity_added(self, data: ActivityAddedData):
        starts_at = data.starts_at.strftime("%Y-%m-%d %H:%M")
        ends_at = data.ends_at.strftime("%Y-%m-%d %H:%M")
        self.treeview.insert("", "end", values=(data.id_, starts_at, ends_at, data.description))

    def on_tree_selected(self, _):
        current = self.treeview.focus()
        item = self.treeview.item(current)
        values = item.get('values')
        if not values:
            activity_id = None
            event = Event(EventType.ACTIVITY_SELECTED, ActivitySelectedData(activity_id))
        else:
            activity_id = values[0]
            activity_id = int(activity_id)
            event = Event(EventType.ACTIVITY_SELECTED, ActivitySelectedData(activity_id))
        event.emit()

    def clear(self):
        for child in self.treeview.get_children():
            self.treeview.delete(child)
        self.treeview.update()

    def on_activities_loaded(self, data: ActivitiesLoadedData):
        self.clear()
        for activity in data.activities:
            starts_at = activity.starts_at.strftime("%Y-%m-%d %H:%M")
            ends_at = activity.ends_at.strftime("%Y-%m-%d %H:%M")
            self.treeview.insert("", "end", values=(activity.id_, starts_at, ends_at, activity.description))