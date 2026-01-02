import tkinter as tk
from tkinter import messagebox
from auth import create_user

def show_setup_admin(on_done):
    win = tk.Tk()
    win.title("Initial Setup – Create Admin")
    win.geometry("400x300")

    tk.Label(win, text="Create Admin Account", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(win, text="Username").pack()
    user = tk.Entry(win)
    user.pack()

    tk.Label(win, text="Password").pack()
    pwd = tk.Entry(win, show="*")
    pwd.pack()

    def create():
        if not user.get() or not pwd.get():
            messagebox.showerror("Error", "All fields required")
            return

        create_user(user.get(), pwd.get(), "admin")
        messagebox.showinfo("Success", "Admin created successfully")

        win.destroy()
        on_done()

    tk.Button(win, text="Create Admin", command=create).pack(pady=20)

    win.mainloop()