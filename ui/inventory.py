import tkinter as tk
from tkinter import ttk
from database import connect

def show_inventory(content, username, role, mode=None):
    for w in content.winfo_children():
        w.destroy()

    tk.Label(
        content,
        text="Inventory",
        font=("Segoe UI", 16, "bold"),
        bg="#ecf0f1"
    ).pack(pady=10)

    columns = ("Item", "Ref", "Expiry", "Category", "Dept", "Supplier")

    tree = ttk.Treeview(content, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(fill="both", expand=True, padx=20, pady=10)

    conn = connect()
    cur = conn.cursor()

    if mode == "expired":
        cur.execute("SELECT item_name, reference_no, expiry_date, category, department, supplier FROM assets WHERE expiry_date < date('now')")
    elif mode == "expiring":
        cur.execute("SELECT item_name, reference_no, expiry_date, category, department, supplier FROM assets WHERE expiry_date BETWEEN date('now') AND date('now','+30 day')")
    else:
        cur.execute("SELECT item_name, reference_no, expiry_date, category, department, supplier FROM assets")

    for row in cur.fetchall():
        tree.insert("", "end", values=row)

    conn.close()