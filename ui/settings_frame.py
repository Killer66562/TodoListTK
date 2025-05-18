from tkinter import messagebox, ttk
from tkinter import font
from ui.base import Base
from ui.styles_setting import create_dark_style, create_light_style

import json

class SettingsFrame(Base):
    def __init__(self, master, on_mode_switch_cb):
        super().__init__(master)
        self.current_theme = "light"
        label = ttk.Label(self.frame, text="設定", font=font.Font(family='Arial', size=28))
        label.pack(pady=10)

        self.theme_button = ttk.Button(
            self.frame,
            text="暗色模式",
            command=self.toggle_theme
        )
        self.theme_button.pack()

        self.bottom_frame = ttk.Frame(self.frame)
        self.bottom_frame.pack(side="bottom", fill="x")

        self.save_btn = ttk.Button(
            self.bottom_frame,
            text="保存設定",
            command=self.save_settings
        )
        self.save_btn.pack(side="left", pady=10)

        self.on_mode_switch_cb = on_mode_switch_cb

    def toggle_theme(self):
        if self.current_theme == "light":
            create_dark_style()
            self.current_theme = "dark"
            self.theme_button.config(text="亮色模式")
        else:
            create_light_style()
            self.current_theme = "light"
            self.theme_button.config(text="暗色模式")
        self.on_mode_switch_cb()

    def load_settings(self):
        try:
            with open("config.json", mode="r", encoding="utf-8") as file:
                config = json.load(file)
                if not isinstance(config, dict):
                    raise ValueError()
                current_theme = config.get("current_theme", "light")
                self.current_theme = current_theme
                if self.current_theme == "light":
                    create_light_style()
                    self.theme_button.config(text="暗色模式")
                elif self.current_theme == "dark":
                    create_dark_style()
                    self.theme_button.config(text="亮色模式")
                else:
                    self.current_theme = "light"
                    create_light_style()
                    self.theme_button.config(text="暗色模式")
                    self.save_settings()
        except:
            self.save_settings()
            self.load_settings()

    def save_settings(self):
        config = {
            "current_theme": self.current_theme
        }
        with open("config.json", mode="w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)
        messagebox.showinfo("成功", "設定保存成功")