from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from auth import create_user

class SetupWindow(QWidget):
    # Signal to tell main.py that the admin is created
    setup_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Initial Setup – Create Admin")
        self.setFixedSize(400, 350)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Create Admin Account")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

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

        self.create_btn = QPushButton("Create Admin")
        self.create_btn.setFixedWidth(280)
        self.create_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 12px; border-radius: 5px; font-weight: bold;")
        self.create_btn.clicked.connect(self.handle_setup)
        layout.addWidget(self.create_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def handle_setup(self):
        u = self.user_input.text().strip()
        p = self.pass_input.text().strip()

        if not u or not p:
            QMessageBox.warning(self, "Error", "All fields are required")
            return

        # Save to database using your existing auth logic
        create_user(u, p, "admin")
        QMessageBox.information(self, "Success", "Admin created successfully!")
        
        # Emit signal to main.py to switch to Login
        self.setup_finished.emit()