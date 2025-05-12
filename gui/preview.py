import tkinter as tk
from tkinter import ttk, font
from datetime import datetime, timedelta
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from enums.enums import DB_URL, EventType
from events.listener import EventListener
from events.data import FontSizeChangedData
from models.models import Activity


class PreviewFrame(EventListener):
    def __init__(self, master=None):
        super().__init__()
        self.engine = create_engine(DB_URL)
        self.current_font_size = 10
        self.base_font = font.Font(size=self.current_font_size)

        self.frame = tk.Frame(master)

        tk.Label(self.frame, text="近期活動", font=self.base_font).pack(anchor="w", padx=10, pady=5)

        columns = ("name", "starts_at", "ends_at")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        self.tree.heading("name", text="活動名稱")
        self.tree.heading("starts_at", text="開始時間")
        self.tree.heading("ends_at", text="結束時間")

        self.tree.column("name", width=200)
        self.tree.column("starts_at", width=150)
        self.tree.column("ends_at", width=150)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        self.load_preview_events()

        self.add_handler(EventType.FS_CHANGED, self.on_fs_changed)

    def load_preview_events(self):
        today = datetime.today().date()
        start_time = datetime.combine(today - timedelta(days=1), datetime.min.time())  # 昨天 00:00
        end_time = datetime.combine(today + timedelta(days=2), datetime.min.time())    # 後天 00:00，不含

        with Session(self.engine) as session:
            stmt = session.query(Activity).filter(Activity.starts_at >= start_time).filter(Activity.starts_at < end_time)
            results = stmt.all()
            results.sort(key=lambda a: a.starts_at)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for activity in results:
            self.tree.insert("", "end", values=(
                activity.name,
                activity.starts_at.strftime("%Y-%m-%d %H:%M"),
                activity.ends_at.strftime("%Y-%m-%d %H:%M"),
            ))

    def on_fs_changed(self, data: FontSizeChangedData):
        self.current_font_size = data.font_size
        self.base_font.configure(size=self.current_font_size)