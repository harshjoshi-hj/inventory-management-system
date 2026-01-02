from tkinter import ttk

def load_styles():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Sidebar.TButton",
        font=("Segoe UI", 11, "bold"),
        padding=12,
        background="#2c3e50",
        foreground="white",
        borderwidth=0
    )
    style.map(
        "Sidebar.TButton",
        background=[("active", "#1abc9c")]
    )

    style.configure(
        "Primary.TButton",
        font=("Segoe UI", 11, "bold"),
        padding=10,
        background="#2980b9",
        foreground="white"
    )

    style.configure(
        "Danger.TButton",
        font=("Segoe UI", 11, "bold"),
        padding=10,
        background="#c0392b",
        foreground="white"
    )

    style.configure(
        "Title.TLabel",
        font=("Segoe UI", 20, "bold"),
        foreground="#2c3e50"
    )

    style.configure(
        "Normal.TLabel",
        font=("Segoe UI", 11),
        foreground="#34495e"
    )

    style.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=28
    )
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 11, "bold")
    )