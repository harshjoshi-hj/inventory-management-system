import tkinter as tk
from tkinter import messagebox
from database import connect
from auth import hash_password

# ================= CREATE FIRST ADMIN =================

def show_create_admin():
    root = tk.Tk()
    root.title("Create Admin Account")
    root.geometry("360x280")
    root.resizable(False, False)

    tk.Label(root, text="Create Admin", font=("Segoe UI", 14, "bold")).pack(pady=10)

    tk.Label(root, text="Username").pack()
    user = tk.Entry(root)
    user.pack()

    tk.Label(root, text="Password").pack()
    pwd = tk.Entry(root, show="*")
    pwd.pack()

    tk.Label(root, text="Confirm Password").pack()
    cpwd = tk.Entry(root, show="*")
    cpwd.pack()

    def create():
        if not user.get() or not pwd.get():
            messagebox.showerror("Error", "All fields required")
            return

        if pwd.get() != cpwd.get():
            messagebox.showerror("Error", "Passwords do not match")
            return

        conn = connect()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
                (user.get(), hash_password(pwd.get()), "admin")
            )
            conn.commit()
        except Exception as e:
            messagebox.showerror("Error", "Admin already exists")
            conn.close()
            return

        conn.close()
        messagebox.showinfo("Success", "Admin created")

        root.destroy()
        from ui.login import show_login
        show_login()

    tk.Button(root, text="Create Admin", width=20, command=create).pack(pady=20)

    root.mainloop()

# ================= VIEW USERS (ADMIN PANEL) =================

def show_users(content):
    for w in content.winfo_children():
        w.destroy()

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT username, role FROM users")
    users = cur.fetchall()
    conn.close()

    tk.Label(content, text="Users", font=("Segoe UI", 14, "bold")).pack(pady=10)

    for u, r in users:
        tk.Label(content, text=f"{u} ({r})").pack(anchor="w", padx=20)