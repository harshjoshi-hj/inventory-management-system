from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, 
                             QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QDateEdit, QComboBox, QFrame, 
                             QGraphicsDropShadowEffect, QAbstractItemView, QDialog, QDialogButtonBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from database import connect
from logs import log_action

class StaffPage(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        
        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # ================= TOP SECTION: REGISTRATION CARD =================
        center_container = QHBoxLayout()
        center_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.card = QFrame()
        self.card.setFixedWidth(600)
        self.card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 5)
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(15)

        title = QLabel("Register New Employee")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("border: none; font-size: 22px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        card_layout.addWidget(title)

        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.input_style = """
            QLineEdit, QComboBox, QDateEdit {
                padding: 10px; border: 1px solid #ccc; border-radius: 5px; font-size: 13px; background-color: #f9f9f9;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 1px solid #3498db; background-color: white;
            }
        """

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. John Doe")
        self.name_input.setStyleSheet(self.input_style)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("e.g. jdoe01")
        self.user_input.setStyleSheet(self.input_style)

        self.email_input = QLineEdit()
        self.email_input.setStyleSheet(self.input_style)

        self.phone_input = QLineEdit()
        self.phone_input.setStyleSheet(self.input_style)
        
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])
        self.gender_input.setStyleSheet(self.input_style)
        
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDate(QDate.currentDate().addYears(-20))
        self.dob_input.setStyleSheet(self.input_style)

        label_style = "border: none; font-size: 14px; font-weight: 600; color: #555;"

        form_layout.addRow(QLabel("Full Name:", styleSheet=label_style), self.name_input)
        form_layout.addRow(QLabel("Username (ID):", styleSheet=label_style), self.user_input)
        form_layout.addRow(QLabel("Email ID:", styleSheet=label_style), self.email_input)
        form_layout.addRow(QLabel("Phone Number:", styleSheet=label_style), self.phone_input)
        form_layout.addRow(QLabel("Gender:", styleSheet=label_style), self.gender_input)
        form_layout.addRow(QLabel("Date of Birth:", styleSheet=label_style), self.dob_input)
        
        card_layout.addLayout(form_layout)

        btn_save = QPushButton("Create Employee ID")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white; padding: 12px; font-size: 15px; font-weight: bold; border-radius: 8px; margin-top: 10px;
            }
            QPushButton:hover { background-color: #219150; }
        """)
        btn_save.clicked.connect(self.add_staff)
        card_layout.addWidget(btn_save)

        center_container.addWidget(self.card)
        main_layout.addLayout(center_container)

        # ================= BOTTOM SECTION: STAFF LIST =================
        list_header = QLabel("Staff Directory")
        list_header.setStyleSheet("font-size: 18px; font-weight: bold; color: #34495e; margin-top: 20px;")
        main_layout.addWidget(list_header)
        
        self.table = QTableWidget()
        # Added "Actions" column
        self.columns = ["ID", "Full Name", "Username", "Email", "Phone", "Gender", "DOB", "Actions"]
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Fix Action column size
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(7, 180) 
        
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white; border: 1px solid #ddd; gridline-color: #f0f0f0; font-size: 13px;
            }
            QHeaderView::section {
                background-color: #f8f9fa; padding: 8px; font-weight: bold; border: none; border-bottom: 2px solid #ddd;
            }
        """)
        main_layout.addWidget(self.table)
        
        self.load_staff()

    def add_staff(self):
        data = (
            self.name_input.text().strip(),
            self.user_input.text().strip(),
            self.email_input.text().strip(),
            self.phone_input.text().strip(),
            self.gender_input.currentText(),
            self.dob_input.date().toString("yyyy-MM-dd"),
            self.username
        )
        
        if not data[0] or not data[1]:
            QMessageBox.warning(self, "Validation Error", "Full Name and Username are required.")
            return

        conn = connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO staff (full_name, username, email, phone, gender, dob, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, data)
            conn.commit()
            log_action(self.username, "Registered Staff", f"{data[0]} ({data[1]})")
            QMessageBox.information(self, "Success", "Employee Registered Successfully!")
            
            self.name_input.clear()
            self.user_input.clear()
            self.email_input.clear()
            self.phone_input.clear()
            self.load_staff()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            conn.close()

    def load_staff(self):
        self.table.setRowCount(0)
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT id, full_name, username, email, phone, gender, dob FROM staff ORDER BY id DESC")
        rows = cur.fetchall()
        self.table.setRowCount(len(rows))
        
        for i, row in enumerate(rows):
            staff_id = row[0]
            # Data Columns
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
            
            # Action Buttons (Edit / Delete)
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 2, 5, 2)
            action_layout.setSpacing(5)

            btn_edit = QPushButton("Edit")
            btn_edit.setStyleSheet("background-color: #3498db; color: white; border-radius: 4px; font-weight: bold; padding: 4px;")
            btn_edit.clicked.connect(lambda checked, s_id=staff_id: self.edit_staff(s_id))

            btn_delete = QPushButton("Delete")
            btn_delete.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 4px; font-weight: bold; padding: 4px;")
            btn_delete.clicked.connect(lambda checked, s_id=staff_id: self.delete_staff(s_id))

            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_delete)
            
            self.table.setCellWidget(i, 7, action_widget)

        conn.close()

    def delete_staff(self, staff_id):
        confirm = QMessageBox.question(self, "Confirm Delete", 
                                     "Are you sure you want to delete this employee?\nThis will also unassign their hardware.",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:
            conn = connect()
            cur = conn.cursor()
            try:
                # 1. Unassign any hardware they have first (Clean up)
                cur.execute("UPDATE hardware SET status='Available', assigned_to_id=NULL, assigned_date=NULL WHERE assigned_to_id=?", (staff_id,))
                
                # 2. Delete the Staff
                cur.execute("DELETE FROM staff WHERE id=?", (staff_id,))
                conn.commit()
                
                log_action(self.username, "Deleted Staff", f"Staff ID: {staff_id}")
                self.load_staff()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
            finally:
                conn.close()

    def edit_staff(self, staff_id):
        # 1. Fetch current data
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT full_name, username, email, phone, gender, dob FROM staff WHERE id=?", (staff_id,))
        data = cur.fetchone()
        conn.close()
        
        if not data: return

        # 2. Open Dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Employee Details")
        dialog.setFixedWidth(400)
        dialog.setStyleSheet("background-color: white;")
        
        layout = QFormLayout(dialog)
        
        name_edit = QLineEdit(data[0])
        name_edit.setStyleSheet(self.input_style)
        
        user_edit = QLineEdit(data[1])
        user_edit.setStyleSheet(self.input_style)
        
        email_edit = QLineEdit(data[2])
        email_edit.setStyleSheet(self.input_style)
        
        phone_edit = QLineEdit(data[3])
        phone_edit.setStyleSheet(self.input_style)
        
        gender_edit = QComboBox()
        gender_edit.addItems(["Male", "Female", "Other"])
        gender_edit.setCurrentText(data[4])
        gender_edit.setStyleSheet(self.input_style)
        
        dob_edit = QDateEdit()
        dob_edit.setCalendarPopup(True)
        dob_edit.setDate(QDate.fromString(data[5], "yyyy-MM-dd"))
        dob_edit.setStyleSheet(self.input_style)
        
        layout.addRow("Full Name:", name_edit)
        layout.addRow("Username:", user_edit)
        layout.addRow("Email:", email_edit)
        layout.addRow("Phone:", phone_edit)
        layout.addRow("Gender:", gender_edit)
        layout.addRow("DOB:", dob_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec():
            # 3. Update Database
            new_data = (
                name_edit.text(), user_edit.text(), email_edit.text(), 
                phone_edit.text(), gender_edit.currentText(), 
                dob_edit.date().toString("yyyy-MM-dd"), staff_id
            )
            
            conn = connect()
            cur = conn.cursor()
            cur.execute("""
                UPDATE staff SET full_name=?, username=?, email=?, phone=?, gender=?, dob=?
                WHERE id=?
            """, new_data)
            conn.commit()
            conn.close()
            
            log_action(self.username, "Edited Staff", f"{new_data[0]}")
            self.load_staff()
            QMessageBox.information(self, "Success", "Staff details updated!")