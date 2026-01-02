import tkinter as tk
from database import connect

def show_logs(content, username, role): # Added arguments for consistency with menu caller
    for w in content.winfo_children():
        w.destroy()

    tk.Label(content, text="Activity Logs", font=("Segoe UI", 14, "bold")).pack(pady=10)

    conn = connect()
    cur = conn.cursor()
    # Corrected column names: user, timestamp
    cur.execute("SELECT user, action, timestamp FROM logs ORDER BY timestamp DESC")

    for u, a, t in cur.fetchall():
        tk.Label(content, text=f"{t} | {u} | {a}", anchor="w").pack(fill="x", padx=20)
    
    conn.close()