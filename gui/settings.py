import tkinter as tk


def show_settings(root, content_area):

    # 外層容器
    settings_frame = tk.Frame(content_area)
    settings_frame.pack(expand=True, fill="both", pady=20, padx=20)
    
    # 標題
    title_label = tk.Label(settings_frame, text="應用程式設定", font=tk.Font(size=20, weight="bold"))
    title_label.pack(pady=(0, 20))

    # 字體大小
    font_frame = tk.Frame(settings_frame, fg_color="transparent")
    font_frame.pack(pady=10, fill="x")

    font_size_label = tk.Label(font_frame, text="字體大小", anchor="w")
    font_size_label.pack(side="left", padx=10)

    font_size_var = tk.IntVar(value=16)
    font_size_entry = tk.Entry(font_frame, textvariable=font_size_var)
    font_size_entry.pack(side="left", fill="x", padx=10, expand=True)

    apply_font_button = tk.Button(font_frame, text="套用字體大小")
    apply_font_button.pack(side="right", padx=10)