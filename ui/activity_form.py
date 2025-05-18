from datetime import datetime
from tkinter import messagebox

from models import local
from models.local import Activity
from .base import Base
from .datetime_row import DateTimeRow
from typing import Callable

import tkinter as tk

class ActivityForm(Base):
    def __init__(
        self, master, 
        tags: list[local.Tag], 
        on_add_btn_clicked_cb: Callable[[datetime, datetime, str, list[local.Tag]], None], 
        on_delete_btn_clicked_cb: Callable[[int], None], 
        on_modify_btn_clicked_cb: Callable[[int, datetime, datetime, str, list[local.Tag]], None], 
        on_cancel_btn_clicked_cb: Callable[[], None]
    ):
        super().__init__(master)
        self._activity: Activity | None = None
        self._tag_checkboxes = []
        self._tags = tags

        self._tag_id_var_mapping: dict[int, tk.BooleanVar] = {}

        self._activity_var = tk.StringVar(value="")
        self._done_var = tk.BooleanVar(value=False)

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

        self._center_bottom_frame = tk.Frame(self._center_frame)
        self._center_bottom_frame.pack(fill="x")

        self._tags_label = tk.Label(self._center_bottom_frame, text="標籤:")
        self._tags_label.pack(side="left")

        self._done_checkbox = tk.Checkbutton(self._center_bottom_frame, onvalue=True, offvalue=False, text="已完成", variable=self._done_var)

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

        for tag in self._tags:
            var = tk.BooleanVar(value=False)
            self._tag_id_var_mapping[tag.id_] = var
            label = tk.Checkbutton(self._center_bottom_frame, text=tag.name, onvalue=True, offvalue=False, variable=var)
            label.pack(side="left")

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
        return self._activity.id_
    
    def get_done(self) -> bool:
        return self._done_var.get()
    
    def set_done(self, done: bool):
        self._done_var.set(done)

    def set_tags(self, tags: list[local.Tag]):
        self._tags = tags
        self.clear_tag_checkboxes()
        for tag in self._tags:
            var = tk.BooleanVar(value=False)
            self._tag_id_var_mapping[tag.id_] = var
            checkbox = tk.Checkbutton(self._center_bottom_frame, text=tag.name, onvalue=True, offvalue=False, variable=var)
            checkbox.pack(side="left")
            self._tag_checkboxes.append(checkbox)
        self.update_activity_tags()

    def clear_tag_checkboxes(self):
        for tag_checkbox in self._tag_checkboxes:
            tag_checkbox.pack_forget()
    
    def _make_btns_normal(self):
        self._add_activity_btn.configure(state="disabled")
        self._delete_activity_btn.configure(state="normal")
        self._modify_activity_btn.configure(state="normal")
        self._cancel_btn.configure(state="normal")
        self._done_checkbox.pack(anchor="w")

    def _make_btns_disabled(self):
        self._add_activity_btn.configure(state="normal")
        self._delete_activity_btn.configure(state="disabled")
        self._modify_activity_btn.configure(state="disabled")
        self._cancel_btn.configure(state="disabled")
        self._done_checkbox.pack_forget()

    def reset(self, starts_at: datetime, ends_at: datetime):
        self.set_starts_at(starts_at)
        self.set_ends_at(ends_at)
        self.set_description("")
        self.set_done(False)
        self.set_activity(None)

    def update_activity_tags(self):
        for var in self._tag_id_var_mapping.values():
            var.set(value=False)
        if not self._activity:
            return
        activity_tag_ids = [activity.id_ for activity in self._activity.tags]
        for tag_id in activity_tag_ids:
            var = self._tag_id_var_mapping.get(tag_id)
            if not var:
                continue
            var.set(value=True)
    
    def set_activity(self, activity: Activity | None):
        self._activity = activity
        self.update_activity_tags()
        if self._activity:
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
        
        tags = [local.Tag(
            tag.id_, 
            tag.name
        ) for tag in self._tags if self._tag_id_var_mapping.get(tag.id_).get()]
        self.on_add_btn_clicked_cb(starts_at, ends_at, description, tags)

        self.set_description("")

    def on_modify_btn_clicked(self):
        starts_at = self.get_starts_at()
        ends_at = self.get_ends_at()
        description = self.get_description()
        done = self._done_var.get()

        tags = [local.Tag(
            tag.id_, 
            tag.name
        ) for tag in self._tags if self._tag_id_var_mapping.get(tag.id_).get()]

        if not description:
            messagebox.showwarning("警告", "請輸入活動名稱")
            return
        
        self.on_modify_btn_clicked_cb(self._activity.id_, starts_at, ends_at, description, done, tags)

    def on_cancel_btn_clicked(self):
        self.on_cancel_btn_clicked_cb()

    def on_delete_btn_clicked(self):
        if self._activity:
            self.on_delete_btn_clicked_cb(self._activity.id_)


if __name__ == "__main__":
    window = tk.Tk()

    activity_form = ActivityForm(window)
    activity_form.frame.pack(expand=True, fill="both")

    window.mainloop()