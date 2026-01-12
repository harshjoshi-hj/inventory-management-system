from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, 
                             QLabel, QMessageBox)
from PyQt6.QtCore import pyqtSignal, Qt
from auth import login_user
from logs import log_action  # <--- NEW IMPORT

class LoginWindow(QWidget):
    login_success = pyqtSignal(str, str) # Signals to main.py when login is valid

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - LS Cable")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel("Login")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.user_input.setFixedWidth(280)
        self.user_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        layout.addWidget(self.user_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setFixedWidth(280)
        self.pass_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        layout.addWidget(self.pass_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.login_btn = QPushButton("Login")
        self.login_btn.setFixedWidth(280)
        self.login_btn.setStyleSheet("background-color: #2980b9; color: white; padding: 12px; border-radius: 5px; font-weight: bold;")
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def handle_login(self):
        u = self.user_input.text()
        p = self.pass_input.text()
        
        res = login_user(u, p)
        
        if res:
            # ✅ LOG THE LOGIN EVENT
            log_action(u, "Login", "System Access")
            
            self.login_success.emit(u, res["role"])
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid Credentials")