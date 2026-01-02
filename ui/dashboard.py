import tkinter as tk
from ui.inventory import show_inventory
from ui.add_item import show_add_item
from ui.users import show_users
from ui.activity_logs import show_logs

def show_dashboard(username, role):
    win = tk.Tk()
    win.title("LS Cable Inventory Management System")
    win.geometry("1200x700")

    sidebar = tk.Frame(win, bg="#2c3e50", width=220)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    content = tk.Frame(win, bg="#ecf0f1")
    content.pack(side="right", fill="both", expand=True)

    def clear():
        for w in content.winfo_children():
            w.destroy()

    def menu(text, command):
        tk.Button(
            sidebar,
            text=text,
            fg="white", bg="#34495e", activebackground="#1abc9c",
            font=("Segoe UI", 11, "bold"), anchor="w", padx=15, pady=10, relief="flat",
            command=lambda: (clear(), command(content, username, role))
        ).pack(fill="x", padx=10, pady=4)

    tk.Label(sidebar, text="LS Cable", fg="white", bg="#2c3e50", font=("Segoe UI", 16, "bold")).pack(pady=20)

    menu("Inventory", show_inventory)
    menu("Add Item", show_add_item)
    menu("Expired Items", lambda c, u, r: show_inventory(c, u, r, "expired"))
    menu("Expiring (30 Days)", lambda c, u, r: show_inventory(c, u, r, "expiring"))

    if role == "admin":
        menu("Users", show_users)
        menu("Activity Logs", show_logs)

    def logout():
        win.destroy()
        from main import open_login # Centralized login entry point
        open_login()

    tk.Button(sidebar, text="Logout", fg="white", bg="#e74c3c", relief="flat", pady=10, command=logout).pack(fill="x", padx=10, pady=20)

    show_inventory(content, username, role)
    win.mainloop()