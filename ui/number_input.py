from tkinter import messagebox
from .base import Base

import tkinter as tk


class NumberInput(Base):
    def __init__(self, master, min_val: int, max_val: int, default: int, btn_only: bool = False, label: str = ""):
        super().__init__(master)
        if min_val > max_val:
            raise ValueError("Error: min_val should be smaller than max_val")
        if default < min_val or default > max_val:
            raise ValueError("Error: default should be bigger than or equal min_val and smaller than or equal max_val")

        self._min_val = min_val
        self._max_val = max_val

        self._num_var = tk.StringVar(value=str(default))

        self._label = tk.Label(self.frame, text=label)
        self._label.pack()

        self._iframe = tk.Frame(self.frame)
        self._iframe.pack(fill="x")

        self._minus_btn = tk.Button(self._iframe, text="-", command=self._on_minus_btn_clicked, width=0, padx=5)
        self._minus_btn.pack(side="left")

        self._add_btn = tk.Button(self._iframe, text="+", command=self._on_add_btn_clicked, width=0, padx=4)
        self._add_btn.pack(side="right")

        state = "readonly" if btn_only else "normal"
        self._entry = tk.Entry(self._iframe, state=state, validate="focusout", validatecommand=self._validate, invalidcommand=self._on_invalid, textvariable=self._num_var, width=0)
        self._entry.pack(side="top", expand=True, fill="both")
        self._entry.bind("<Return>", self._on_return)

    def _on_invalid(self):
        messagebox.showerror("錯誤", f"請輸入一個介於{self._min_val}~{self._max_val}的值")
        self._entry.focus()

    def _on_minus_btn_clicked(self):
        try:
            num = int(self._num_var.get())
            if num > self._max_val:
                self._num_var.set(str(self._max_val))
            else:
                self._num_var.set(max(self._min_val, num - 1))
        except ValueError:
            self._num_var.set(self._max_val)
        finally:
            self._frame.focus()

    def _on_add_btn_clicked(self):
        try:
            num = int(self._num_var.get())
            if num < self._min_val:
                self._num_var.set(str(self._min_val))
            else:
                self._num_var.set(min(self._max_val, num + 1))
        except ValueError:
            self._num_var.set(self._min_val)
        finally:
            self._frame.focus()

    def _validate(self) -> bool:
        try:
            num = int(self._num_var.get())
            if num < self._min_val or num > self._max_val:
                return False
            return True
        except ValueError:
            return False
        
    def _on_return(self, _):
        self._frame.focus()

    def configure(self, min_val: int, max_val: int):
        if min_val > max_val:
            raise ValueError("Error: min_val should be smaller than max_val")
        self._min_val = min_val
        self._max_val = max_val
        num = int(self._num_var.get())
        if num < self._min_val:
            self._num_var.set(self._min_val)
        elif num > self._max_val:
            self._num_var.set(self._max_val)

    def get(self) -> int:
        return int(self._num_var.get())
    
    def set(self, value: int):
        if value < self._min_val:
            self._num_var.set(str(self._min_val))
        elif value > self._max_val:
            self._num_var.set(str(self._max_val))
        else:
            self._num_var.set(str(value))


if __name__ == "__main__":
    window = tk.Tk()
    
    number_input = NumberInput(window, 1, 31)
    number_input.frame.pack()

    number_input_2 = NumberInput(window, 1, 31, True)
    number_input_2.frame.pack()

    window.mainloop()