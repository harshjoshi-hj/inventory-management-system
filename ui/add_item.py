import tkinter as tk
from database import connect

def show_add_item(content):
    for w in content.winfo_children():
        w.destroy()

    fields = ["Item", "Ref", "Expiry (YYYY-MM-DD)", "Category", "Dept", "Supplier"]
    entries = {}

    for f in fields:
        tk.Label(content, text=f).pack()
        e = tk.Entry(content, width=40)
        e.pack(pady=4)
        entries[f] = e

    def save():
        conn = connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO assets VALUES (NULL,?,?,?,?,?,?)",
            (
                entries["Item"].get(),
                entries["Ref"].get(),
                entries["Expiry (YYYY-MM-DD)"].get(),
                entries["Category"].get(),
                entries["Dept"].get(),
                entries["Supplier"].get()
            )
        )
        conn.commit()
        conn.close()

    tk.Button(content, text="Save Item", command=save).pack(pady=20)