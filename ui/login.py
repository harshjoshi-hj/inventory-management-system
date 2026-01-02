import tkinter as tk
from tkinter import messagebox
from auth import login_user

def show_login(on_success):
    win = tk.Tk()
    win.title("Login")
    win.geometry("400x250")

    tk.Label(win, text="Username").pack(pady=5)
    user_entry = tk.Entry(win)
    user_entry.pack()

    tk.Label(win, text="Password").pack(pady=5)
    pass_entry = tk.Entry(win, show="*")
    pass_entry.pack()

    def login():
        # ✅ GET DATA FIRST
        username = user_entry.get()
        password = pass_entry.get()

        result = login_user(username, password)
        if not result:
            messagebox.showerror("Error", "Invalid credentials")
            return

        role = result["role"]

        # ✅ DESTROY WINDOW AFTER DATA IS STORED
        win.destroy()

        # ✅ PASS PURE DATA (NO WIDGETS)
        on_success(username, role)

    tk.Button(win, text="Login", command=login).pack(pady=20)

    win.mainloop()