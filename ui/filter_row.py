import tkinter as tk

from ui.base import Base


class FilterRow(Base):
    def __init__(
        self, 
        master, 
        on_combobox_changed_cb
    ):
        super().__init__(master)
        self._option_var = tk.StringVar(value="all")

        self._all_btn = tk.Radiobutton(self.frame, text="全部", value="all", variable=self._option_var, command=self.on_combobox_changed)
        self._all_btn.pack(side="left")

        self._not_done_btn = tk.Radiobutton(self.frame, text="未完成", value="not_done", variable=self._option_var, command=self.on_combobox_changed)
        self._not_done_btn.pack(side="left")

        self._done_btn = tk.Radiobutton(self.frame, text="已完成", value="done", variable=self._option_var, command=self.on_combobox_changed)
        self._done_btn.pack(side="left")

        self._on_combobox_changed_cb = on_combobox_changed_cb

    def get(self) -> bool | None:
        if self._option_var.get() == "all":
            return None
        elif self._option_var.get() == "not_done":
            return False
        elif self._option_var.get() == "done":
            return True

    def on_combobox_changed(self):
        self._on_combobox_changed_cb(self.get())