import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Callable

from .base import Base

class TagButton(Base):
    def __init__(
        self,
        master,
        name: str,
        on_main_btn_clicked_cb: Callable[[str], None],
        on_delete_btn_clicked_cb: Callable[[str], None],
    ):
        super().__init__(master)
        self.name = name

        self._main_btn = ttk.Button(
            self.frame,
            text=self.name,
            command=self.on_main_btn_clicked,
            style="Tag.TButton"
        )
        self._main_btn.pack(side="left", expand=True, fill="x", padx=2, pady=2)

        self._delete_btn = ttk.Button(
            self.frame,
            text="x",
            command=self.on_delete_btn_clicked,
            style="TagDelete.TButton"
        )
        self._delete_btn.pack(side="right", padx=2, pady=2)

        self._on_main_btn_clicked_cb = on_main_btn_clicked_cb
        self._on_delete_btn_clicked_cb = on_delete_btn_clicked_cb

    def on_main_btn_clicked(self):
        if self._on_main_btn_clicked_cb:
            self._on_main_btn_clicked_cb(self.name)

    def on_delete_btn_clicked(self):
        yes = messagebox.askyesno("確認", "你確定要刪除這個標籤嗎?\n被刪除的標籤無法復原")
        if not yes:
            return
        if self._on_delete_btn_clicked_cb:
            self._on_delete_btn_clicked_cb(self.name)