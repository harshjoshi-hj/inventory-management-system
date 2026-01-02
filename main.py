from database import init_db, has_admin
from ui.login import show_login
from ui.setup_admin import show_setup_admin
from ui.dashboard import show_dashboard

def open_dashboard(username, role):
    show_dashboard(username, role)

def open_login():
    show_login(open_dashboard)

if __name__ == "__main__":
    init_db()

    if has_admin():
        open_login()
    else:
        show_setup_admin(open_login)