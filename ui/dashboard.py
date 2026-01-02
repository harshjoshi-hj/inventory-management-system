import tkinter as tk
from ui.inventory import show_inventory
from ui.add_item import show_add_item
from ui.users import show_users
from ui.activity_logs import show_logs

def show_dashboard(username, role):
    win = tk.Tk()
    win.title("LS Cable Inventory Management System")
    win.geometry("1200x700")

    # ================= SIDEBAR =================
    # Using the original dark color (#2c3e50)
    sidebar = tk.Frame(win, bg="#2c3e50", width=220)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # ================= CONTENT =================
    content = tk.Frame(win, bg="#ecf0f1")
    content.pack(side="right", fill="both", expand=True)

    def clear():
        for w in content.winfo_children():
            w.destroy()

    # This replaces the Button with a Label for a transparent look
    def menu(text, command):
        lbl = tk.Label(
            sidebar,
            text=text,
            fg="white",           # White text
            bg="#2c3e50",         # Matches sidebar exactly (Transparent look)
            font=("Segoe UI", 11, "bold"),
            anchor="w",
            padx=15,
            pady=10,
            cursor="hand2"        # Changes cursor to hand on hover
        )
        
        # Binds the click action
        lbl.bind("<Button-1>", lambda e: (clear(), command(content, username, role)))
        
        # Adds hover effects
        lbl.bind("<Enter>", lambda e: lbl.config(bg="#34495e")) # Lighten on hover
        lbl.bind("<Leave>", lambda e: lbl.config(bg="#2c3e50")) # Return to normal
        
        lbl.pack(fill="x", padx=10, pady=2)

    # Sidebar Header
    tk.Label(
        sidebar,
        text="LS Cable",
        fg="white",
        bg="#2c3e50",
        font=("Segoe UI", 16, "bold")
    ).pack(pady=20)

    # Menu Items
    menu("Inventory", show_inventory)
    menu("Add Item", show_add_item)
    menu("Expired Items", lambda c, u, r: show_inventory(c, u, r, "expired"))
    menu("Expiring (30 Days)", lambda c, u, r: show_inventory(c, u, r, "expiring"))

    if role == "admin":
        menu("Users", show_users)
        menu("Activity Logs", show_logs)

    def logout():
        win.destroy()
        from ui.login import show_login
        show_login(lambda u, r: show_dashboard(u, r))

    # Logout button kept as a standard button for high visibility
    tk.Button(
        sidebar,
        text="Logout",
        fg="white",
        bg="#e74c3c",
        activebackground="#c0392b",
        activeforeground="white",
        relief="flat",
        pady=8,
        command=logout
    ).pack(fill="x", padx=20, pady=20)

    # Load default page
    show_inventory(content, username, role)

    win.mainloop()