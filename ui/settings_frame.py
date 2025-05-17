from tkinter import ttk
from tkinter import font
from ui.styles_setting import create_dark_style, create_light_style

class SettingsFrame:
    def __init__(self, parent, on_mode_switch_cb):
        self.parent = parent
        self.current_theme = "light"

        self.frame = ttk.Frame(parent)

        label = ttk.Label(self.frame, text="設定", font=font.Font(family='Arial', size=28))
        label.pack(pady=10)

        self.theme_button = ttk.Button(
            self.frame,
            text="暗色模式",
            command=self.toggle_theme
        )
        self.theme_button.pack(pady=20)

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