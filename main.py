import sys
from PyQt6.QtWidgets import QApplication
from database import init_db, has_admin
from ui.login import LoginWindow
from ui.dashboard import DashboardWindow
from ui.setup_admin import SetupWindow

class MainApp:
    def __init__(self):
        init_db()
        self.current_window = None
        
        if not has_admin():
            self.show_setup()
        else:
            self.show_login()

    def show_setup(self):
        self.current_window = SetupWindow()
        self.current_window.setup_finished.connect(self.show_login)
        self.current_window.show()

    def show_login(self):
        if self.current_window:
            self.current_window.close()
        self.current_window = LoginWindow()
        self.current_window.login_success.connect(self.show_dashboard)
        self.current_window.show()

    def show_dashboard(self, username, role):
        if self.current_window:
            self.current_window.close()
        self.current_window = DashboardWindow(username, role)
        self.current_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Using 'Helvetica' is safer on Mac to avoid the aliasing delay
    app.setStyleSheet("QWidget { font-family: 'Helvetica', 'Arial', sans-serif; font-size: 14px; }")
    main = MainApp()
    sys.exit(app.exec())