from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                             QLabel, QFormLayout, QLineEdit, QComboBox, QPushButton, 
                             QMessageBox, QHBoxLayout, QHeaderView, QAbstractItemView, QInputDialog)
from PyQt6.QtCore import Qt
from database import connect
from auth import hash_password
from logs import log_action

class UsersPage(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user # Store the Admin's username for logging
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- Section 1: Create User ---
        layout.addWidget(QLabel("Add New User", styleSheet="font-size: 18px; font-weight: bold; color: #2c3e50;"))
        
        form_layout = QHBoxLayout()
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.role_input = QComboBox()
        self.role_input.addItems(["admin", "manager", "user"])
        
        btn_add = QPushButton("Create User")
        btn_add.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 8px;")
        btn_add.clicked.connect(self.add_user)

        form_layout.addWidget(self.user_input)
        form_layout.addWidget(self.pass_input)
        form_layout.addWidget(self.role_input)
        form_layout.addWidget(btn_add)
        
        layout.addLayout(form_layout)

        # --- Section 2: Manage Users (Table) ---
        layout.addWidget(QLabel("Existing Users", styleSheet="font-size: 18px; font-weight: bold; margin-top: 20px; color: #2c3e50;"))
        
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Username", "Role"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) # Select full row
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # specific edit buttons only
        layout.addWidget(self.table)

        # --- Section 3: Action Buttons ---
        action_layout = QHBoxLayout()
        
        btn_reset = QPushButton("Reset Password")
        btn_reset.setStyleSheet("background-color: #f39c12; color: white; font-weight: bold; padding: 10px;")
        btn_reset.clicked.connect(self.reset_password)
        
        btn_role = QPushButton("Change Role")
        btn_role.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 10px;")
        btn_role.clicked.connect(self.change_role)
        
        btn_delete = QPushButton("Delete User")
        btn_delete.setStyleSheet("background-color: #c0392b; color: white; font-weight: bold; padding: 10px;")
        btn_delete.clicked.connect(self.delete_user)

        action_layout.addWidget(btn_reset)
        action_layout.addWidget(btn_role)
        action_layout.addStretch() # Push delete to the right
        action_layout.addWidget(btn_delete)
        
        layout.addLayout(action_layout)

        self.load_users()

    def load_users(self):
        self.table.setRowCount(0)
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT username, role FROM users")
        rows = cur.fetchall()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(row[0]))
            self.table.setItem(i, 1, QTableWidgetItem(row[1]))
        conn.close()

    def add_user(self):
        u = self.user_input.text().strip()
        p = self.pass_input.text().strip()
        r = self.role_input.currentText()

        if not u or not p:
            QMessageBox.warning(self, "Error", "Username and Password are required.")
            return

        conn = connect()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password_hash, role) VALUES (?,?,?)", (u, hash_password(p), r))
            conn.commit()
            log_action(self.current_user, "Created User", f"{u} ({r})")
            QMessageBox.information(self, "Success", f"User '{u}' created successfully.")
            self.user_input.clear()
            self.pass_input.clear()
            self.load_users()
        except Exception as e:
            QMessageBox.warning(self, "Error", "Username already exists or database error.")
        finally:
            conn.close()

    def get_selected_user(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Selection", "Please select a user from the table first.")
            return None
        return self.table.item(row, 0).text()

    def delete_user(self):
        username = self.get_selected_user()
        if not username: return
        
        if username == self.current_user:
            QMessageBox.critical(self, "Error", "You cannot delete your own account while logged in.")
            return

        confirm = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete user '{username}'?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:
            conn = connect()
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.commit()
            conn.close()
            
            log_action(self.current_user, "Deleted User", username)
            self.load_users()
            QMessageBox.information(self, "Success", "User deleted.")

    def reset_password(self):
        username = self.get_selected_user()
        if not username: return

        new_pass, ok = QInputDialog.getText(self, "Reset Password", f"Enter new password for '{username}':", QLineEdit.EchoMode.Password)
        
        if ok and new_pass:
            conn = connect()
            cur = conn.cursor()
            cur.execute("UPDATE users SET password_hash = ? WHERE username = ?", (hash_password(new_pass), username))
            conn.commit()
            conn.close()
            
            log_action(self.current_user, "Reset Password", username)
            QMessageBox.information(self, "Success", "Password updated successfully.")

    def change_role(self):
        username = self.get_selected_user()
        if not username: return

        roles = ["admin", "manager", "user"]
        new_role, ok = QInputDialog.getItem(self, "Change Role", f"Select new role for '{username}':", roles, 0, False)
        
        if ok and new_role:
            conn = connect()
            cur = conn.cursor()
            cur.execute("UPDATE users SET role = ? WHERE username = ?", (new_role, username))
            conn.commit()
            conn.close()
            
            log_action(self.current_user, "Changed Role", f"{username} -> {new_role}")
            self.load_users()
            QMessageBox.information(self, "Success", "Role updated successfully.")