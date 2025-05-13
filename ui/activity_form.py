from datetime import datetime
from tkinter import messagebox
from .base import Base
from .datetime_row import DateTimeRow
from typing import Callable

import tkinter as tk

class ActivityForm(Base):
    def __init__(
        self, master, 
        on_add_btn_clicked_cb: Callable[[datetime, datetime, str], None], 
        on_delete_btn_clicked_cb: Callable[[int], None], 
        on_modify_btn_clicked_cb: Callable[[int, datetime, datetime, str], None], 
        on_cancel_btn_clicked_cb: Callable[[], None]
    ):
        super().__init__(master)
        self._activity_id: int | None = None

        self._activity_var = tk.StringVar(value="")

        self._top_frame = tk.Frame(self.frame)
        self._top_frame.pack(fill="x")

        self._center_frame = tk.Frame(self.frame)
        self._center_frame.pack(fill="x")

        self._bottom_frame = tk.Frame(self.frame)
        self._bottom_frame.pack(fill="x")

        self._top_left_frame = tk.Frame(self._top_frame)
        self._top_left_frame.pack(side="left", expand=True, fill="x")

        self._top_right_frame = tk.Frame(self._top_frame)
        self._top_right_frame.pack(side="right", expand=True, fill="x")

        self._starts_at_label = tk.Label(self._top_left_frame, text="開始時間")
        self._starts_at_label.pack(anchor="w")

        self._starts_at_row = DateTimeRow(self._top_left_frame)
        self._starts_at_row.frame.pack(fill="x")

        self._starts_at_label = tk.Label(self._top_right_frame, text="結束時間")
        self._starts_at_label.pack(anchor="w")

        self._ends_at_row = DateTimeRow(self._top_right_frame)
        self._ends_at_row.frame.pack(fill="x")

        self._activity_label = tk.Label(self._center_frame, text="活動描述")
        self._activity_label.pack(anchor="w")

        self._activity_entry = tk.Entry(self._center_frame, textvariable=self._activity_var)
        self._activity_entry.pack(fill="x")

        self._add_activity_btn = tk.Button(self._bottom_frame, text="新增活動", command=self.on_add_btn_clicked)
        self._add_activity_btn.pack(side="left")

        self._modify_activity_btn = tk.Button(self._bottom_frame, text="修改活動", state="disabled", command=self.on_modify_btn_clicked)
        self._modify_activity_btn.pack(side="left")

        self._cancel_btn = tk.Button(self._bottom_frame, text="取消修改", state="disabled", command=self.on_cancel_btn_clicked)
        self._cancel_btn.pack(side="left")

        self._delete_activity_btn = tk.Button(self._bottom_frame, text="刪除活動", state="disabled", command=self.on_delete_btn_clicked)
        self._delete_activity_btn.pack(side="left")

        self.on_add_btn_clicked_cb = on_add_btn_clicked_cb
        self.on_delete_btn_clicked_cb = on_delete_btn_clicked_cb
        self.on_modify_btn_clicked_cb = on_modify_btn_clicked_cb
        self.on_cancel_btn_clicked_cb = on_cancel_btn_clicked_cb

    def get_starts_at(self) -> datetime:
        return self._starts_at_row.get_dt()
    
    def set_starts_at(self, dt: datetime):
        self._starts_at_row.set_dt(dt)

    def get_ends_at(self) -> datetime:
        return self._ends_at_row.get_dt()
    
    def set_ends_at(self, dt: datetime):
        self._ends_at_row.set_dt(dt)

    def get_description(self) -> str:
        return self._activity_var.get()
    
    def set_description(self, description: str):
        self._activity_var.set(description)

    def get_activity_id(self) -> int | None:
        return self._activity_id
    
    def _make_btns_normal(self):
        self._delete_activity_btn.configure(state="normal")
        self._modify_activity_btn.configure(state="normal")
        self._cancel_btn.configure(state="normal")

    def _make_btns_disabled(self):
        self._delete_activity_btn.configure(state="disabled")
        self._modify_activity_btn.configure(state="disabled")
        self._cancel_btn.configure(state="disabled")
    
    def set_activity_id(self, activity_id: int | None):
        self._activity_id = activity_id
        if self._activity_id:
            self._make_btns_normal()
        else:
            self._make_btns_disabled()

    def on_add_btn_clicked(self):
        starts_at = self.get_starts_at()
        ends_at = self.get_ends_at()
        description = self.get_description()

        if not description:
            messagebox.showwarning("警告", "請輸入活動名稱")
            return

        self.on_add_btn_clicked_cb(starts_at, ends_at, description)
        self.set_description("")

    def on_modify_btn_clicked(self):
        starts_at = self.get_starts_at()
        ends_at = self.get_ends_at()
        description = self.get_description()

        if not description:
            messagebox.showwarning("警告", "請輸入活動名稱")
            return
        
        self.on_modify_btn_clicked_cb(self._activity_id, starts_at, ends_at, description)

    def on_cancel_btn_clicked(self):
        self.on_cancel_btn_clicked_cb()
        self.set_activity_id(None)

    def on_delete_btn_clicked(self):
        self.on_delete_btn_clicked_cb(self._activity_id)
        self.set_activity_id(None)


if __name__ == "__main__":
    window = tk.Tk()

    activity_form = ActivityForm(window)
    activity_form.frame.pack(expand=True, fill="both")

    window.mainloop()