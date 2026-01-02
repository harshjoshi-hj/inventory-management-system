import tkinter as tk
from tkinter import messagebox
from database import connect

def show_add_item(content, username, role):
    for w in content.winfo_children():
        w.destroy()

    fields = ["Item Name", "Reference No", "Expiry (YYYY-MM-DD)", "Category", "Department", "Supplier"]
    entries = {}

    for f in fields:
        tk.Label(content, text=f).pack()
        e = tk.Entry(content, width=40)
        e.pack(pady=4)
        entries[f] = e

    def save():
        # Validate data
        data = {f: entries[f].get() for f in fields}
        if not all(data.values()):
            messagebox.showerror("Error", "All fields are required")
            return

        conn = connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO assets (item_name, reference_no, expiry_date, category, department, supplier) VALUES (?,?,?,?,?,?)",
            (
                data["Item Name"],
                data["Reference No"],
                data["Expiry (YYYY-MM-DD)"],
                data["Category"],
                data["Department"],
                data["Supplier"]
            )
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Item added successfully")
        # Clear fields
        for e in entries.values(): e.delete(0, tk.END)

    tk.Button(content, text="Save Item", bg="#1abc9c", fg="white", command=save).pack(pady=20)