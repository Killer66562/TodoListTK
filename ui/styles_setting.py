from tkinter import ttk

def create_dark_style():
    style = ttk.Style()
    style.theme_use("default")
    
    if "dark" not in style.theme_names():
        style.theme_create("dark", parent="default", settings={
            "TButton": {
                "configure": {
                    "font": ("Segoe UI", 10),
                    "foreground": "white",
                    "background": "#4a4a4a",
                    "padding": [10, 6],
                    "relief": "flat",
                    "borderwidth": 0,
                    "anchor": "center"
                },
                "map": {
                    "background": [("active", "#5c5c5c"), ("pressed", "#333333")],
                    "foreground": [("disabled", "#999999"), ("!disabled", "white")]
                }
            },
            "TFrame": {
                "configure": {
                    "background": "#1e1e1e"
                }
            },
            "TLabel": {
                "configure": {
                    "font": ("Segoe UI", 10),
                    "foreground": "#dddddd",
                    "background": "#1e1e1e",
                    "padding": 4
                }
            },
            "TEntry": {
                "configure": {
                    "padding": 5,
                    "relief": "flat",
                    "foreground": "white",
                    "background": "#333333",
                    "fieldbackground": "#333333",
                    "insertcolor": "white",
                }
            },
            "Treeview": {
                "configure": {
                    "background": "#2e2e2e",
                    "fieldbackground": "#2e2e2e",
                    "foreground": "white",
                    "rowheight": 25,
                    "borderwidth": 0
                },
                "map": {
                    "background": [("selected", "#444444")],
                    "foreground": [("selected", "white")]
                }
            },
            "Vertical.TScrollbar": {
                "configure": {
                    "background": "#444444",
                    "gripcount": 0,
                    "borderwidth": 0,
                    "arrowcolor": "#aaaaaa"
                },
                "map": {
                    "background": [("active", "#666666")]
                }
            },
            "TMenu": {
                "configure": {
                    "background": "#333333",
                    "foreground": "white",
                    "font": ("Segoe UI", 10),
                    "borderwidth": 0
                },
                "map": {
                    "background": [("active", "#555555")],
                    "foreground": [("active", "white")]
                }
            },
            "TMenubutton": {
                "configure": {
                    "background": "#333333",
                    "foreground": "white",
                    "padding": [10, 6],
                    "font": ("Segoe UI", 10)
                }
            }
        })
    style.theme_use("dark")


def create_light_style():
    style = ttk.Style()
    style.theme_use("default")
    
    if "light" not in style.theme_names():
        style.theme_create("light", parent="default", settings={
            "TButton": {
                "configure": {
                    "font": ("Segoe UI", 10),
                    "foreground": "white",
                    "background": "#4a90e2",
                    "padding": [10, 6],
                    "relief": "flat",
                    "borderwidth": 0,
                    "anchor": "center"
                },
                "map": {
                    "background": [("active", "#357ab8"), ("pressed", "#2c5f94")],
                    "foreground": [("disabled", "#cccccc"), ("!disabled", "white")]
                }
            },
            "TFrame": {
                "configure": {
                    "background": "#f5f5f5"
                }
            },
            "TLabel": {
                "configure": {
                    "font": ("Segoe UI", 10),
                    "foreground": "#333333",
                    "background": "#f5f5f5",
                    "padding": 4
                }
            },
            "TEntry": {
                "configure": {
                    "padding": 5,
                    "relief": "flat",
                    "foreground": "#333333",
                    "background": "white",
                    "fieldbackground": "white",
                    "insertcolor": "#333333",
                }
            },
            "Treeview": {
                "configure": {
                    "background": "white",
                    "fieldbackground": "white",
                    "foreground": "#333333",
                    "rowheight": 25,
                    "borderwidth": 0
                },
                "map": {
                    "background": [("selected", "#cce6ff")],
                    "foreground": [("selected", "black")]
                }
            },
            "Vertical.TScrollbar": {
                "configure": {
                    "background": "#cccccc",
                    "gripcount": 0,
                    "borderwidth": 0,
                    "arrowcolor": "#666666"
                },
                "map": {
                    "background": [("active", "#aaaaaa")]
                }
            },
            "TMenu": {
                "configure": {
                    "background": "#f5f5f5",
                    "foreground": "#333333",
                    "font": ("Segoe UI", 10),
                    "borderwidth": 0
                },
                "map": {
                    "background": [("active", "#dcdcdc")],
                    "foreground": [("active", "black")]
                }
            },
            "TMenubutton": {
                "configure": {
                    "background": "#f5f5f5",
                    "foreground": "#333333",
                    "padding": [10, 6],
                    "font": ("Segoe UI", 10)
                }
            }
        })
    style.theme_use("light")