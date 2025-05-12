from tkinter import ttk


def create_dark_style():
    style = ttk.Style()
    style.theme_create("dark", parent="default", settings={
        "TButton": {
            "configure": {
                "font": ("Arial", 12),
                "foreground": "white",
                "background": "gray",
                "padding": 5
            },
            "map": {
                "background": [("active", "gray"), ("pressed", "gray")],
                "foreground": [("active", "white"), ("pressed", "white")]
            }
        }, 
        "TFrame": {
            "configure": {
                "font": ("Arial", 12),
                "foreground": "white",
                "background": "gray",
                "padding": 5
            },
            "map": {
                "background": [("active", "gray"), ("pressed", "gray")],
                "foreground": [("active", "white"), ("pressed", "white")]
            }
        }
    })