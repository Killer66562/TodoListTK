import tkinter as tk
from typing import Callable

from .base import Base


class TagButton(Base):
    def __init__(
        self, master, 
        name: str, 
        on_main_btn_clicked_cb: Callable[[str], None], 
        on_delete_btn_clicked_cb: Callable[[str], None]
    ):
        super().__init__(master)
        self.name = name

        self._main_btn = tk.Button(self.frame, text=self.name, command=self.on_main_btn_clicked)
        self._main_btn.pack(side="left", expand=True, fill="x")

        self._delete_btn = tk.Button(self.frame, text="x", command=self.on_delete_btn_clicked)
        self._delete_btn.pack(side="right")

        self._on_main_btn_clicked_cb = on_main_btn_clicked_cb
        self._on_delete_btn_clicked_cb = on_delete_btn_clicked_cb

    def on_main_btn_clicked(self):
        self._on_main_btn_clicked_cb(self.name)

    def on_delete_btn_clicked(self):
        self._on_delete_btn_clicked_cb(self.name)