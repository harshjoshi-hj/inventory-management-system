import tkinter as tk
from database import connect

def show_logs(content):
    for w in content.winfo_children():
        w.destroy()

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT username, action, ts FROM logs ORDER BY ts DESC")

    for u, a, t in cur.fetchall():
        tk.Label(content, text=f"{t} | {u} | {a}").pack(anchor="w")