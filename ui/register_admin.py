import tkinter as tk
from tkinter import messagebox
from database import connect
from utils import hash_password

def show_register_admin():
    root = tk.Tk()
    root.title("Create Admin Account")
    root.geometry("400x300")

    tk.Label(root, text="Create Admin", font=("Segoe UI", 16, "bold")).pack(pady=15)

    tk.Label(root, text="Username").pack()
    user = tk.Entry(root)
    user.pack()

    tk.Label(root, text="Password").pack()
    pwd = tk.Entry(root, show="*")
    pwd.pack()

    def create_admin():
        username = user.get().strip()
        password = pwd.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields required")
            return

        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, 'admin')
        """, (username, hash_password(password)))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Admin created successfully")
        root.destroy()

        from ui.login import show_login
        show_login()

    tk.Button(root, text="Create Admin", command=create_admin).pack(pady=20)
    root.mainloop()