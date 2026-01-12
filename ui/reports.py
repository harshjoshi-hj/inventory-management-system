import webbrowser
from urllib.parse import quote
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QTextEdit,
                             QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QFrame, QGraphicsDropShadowEffect,
                             QDialog, QHBoxLayout, QCheckBox, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from database import connect
from logs import log_action

# CONFIGURATION
ADMIN_PHONE_NUMBER = "919876543210" 

class ReportsPage(QWidget):
    def __init__(self, username, role):
        super().__init__()
        self.username = username
        self.role = role
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Support & Reporting")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)

        if self.role == "admin":
            self.init_admin_view(layout)
        else:
            self.init_user_view(layout)

    # ================= USER VIEW (Send Query) =================
    def init_user_view(self, layout):
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card = QFrame()
        card.setFixedWidth(600)
        card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; border: 1px solid #ddd; }")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0,0,0,30))
        card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)

        card_layout.addWidget(QLabel("Send a Query to Admin", styleSheet="font-size: 18px; font-weight: bold;"))

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Subject...")
        self.subject_input.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 5px;")
        
        self.msg_input = QTextEdit()
        self.msg_input.setPlaceholderText("Describe your issue...")
        self.msg_input.setFixedHeight(150)
        self.msg_input.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 5px;")

        card_layout.addWidget(QLabel("Subject:"))
        card_layout.addWidget(self.subject_input)
        card_layout.addWidget(QLabel("Message:"))
        card_layout.addWidget(self.msg_input)

        btn_save = QPushButton("Submit to App")
        btn_save.setStyleSheet("background-color: #3498db; color: white; padding: 12px; font-weight: bold; border-radius: 5px;")
        btn_save.clicked.connect(self.submit_internal)
        
        btn_whatsapp = QPushButton(f"Send via WhatsApp")
        btn_whatsapp.setStyleSheet("background-color: #25D366; color: white; padding: 12px; font-weight: bold; border-radius: 5px;")
        btn_whatsapp.clicked.connect(self.send_via_whatsapp)

        card_layout.addWidget(btn_save)
        card_layout.addWidget(btn_whatsapp)
        layout.addWidget(card)

    def submit_internal(self):
        sub = self.subject_input.text()
        msg = self.msg_input.toPlainText()
        if not sub or not msg:
            QMessageBox.warning(self, "Error", "Fill all fields")
            return
        conn = connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO reports (username, subject, message) VALUES (?, ?, ?)", (self.username, sub, msg))
        conn.commit()
        conn.close()
        log_action(self.username, "Report Submitted", f"Subject: {sub}")
        QMessageBox.information(self, "Success", "Submitted!")
        self.subject_input.clear()
        self.msg_input.clear()

    def send_via_whatsapp(self):
        sub = self.subject_input.text()
        msg = self.msg_input.toPlainText()
        full_text = f"Hello Admin, this is {self.username}.\n\n*Subject:* {sub}\n*Message:* {msg}"
        webbrowser.open(f"https://wa.me/{ADMIN_PHONE_NUMBER}?text={quote(full_text)}")

    # ================= ADMIN VIEW (Read Queries) =================
    def init_admin_view(self, layout):
        # Action Bar
        action_layout = QHBoxLayout()
        
        btn_view = QPushButton("Read Full Message")
        btn_view.setStyleSheet("background-color: #3498db; color: white; padding: 8px 15px; border-radius: 4px; font-weight: bold;")
        btn_view.clicked.connect(self.open_message_popup)
        
        btn_delete = QPushButton("Delete Selected")
        btn_delete.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px 15px; border-radius: 4px; font-weight: bold;")
        btn_delete.clicked.connect(self.delete_selected)
        
        btn_refresh = QPushButton("Refresh")
        btn_refresh.setStyleSheet("background-color: #f1c40f; color: black; padding: 8px 15px; border-radius: 4px; font-weight: bold;")
        btn_refresh.clicked.connect(self.load_reports)

        action_layout.addWidget(btn_view)
        action_layout.addWidget(btn_delete)
        action_layout.addStretch()
        action_layout.addWidget(btn_refresh)
        layout.addLayout(action_layout)

        # Table Setup
        self.table = QTableWidget()
        # Columns: Checkbox, ID, User, Subject, Message, Time
        self.columns = ["Select", "ID", "User", "Subject", "Message", "Time"]
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed) # Checkbox column fixed width
        self.table.setColumnWidth(0, 50)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setStyleSheet("background-color: white; border: 1px solid #ddd;")
        
        # Double click to open popup
        self.table.cellDoubleClicked.connect(self.open_message_popup)
        
        layout.addWidget(self.table)
        self.load_reports()

    def load_reports(self):
        self.table.setRowCount(0)
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT id, username, subject, message, timestamp FROM reports ORDER BY timestamp DESC")
        rows = cur.fetchall()
        
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            # 0. Checkbox
            chk_widget = QWidget()
            chk_layout = QHBoxLayout(chk_widget)
            chk_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            chk_layout.setContentsMargins(0,0,0,0)
            checkbox = QCheckBox()
            # Store the Report ID in the checkbox for easy deletion
            checkbox.setProperty("report_id", row[0]) 
            chk_layout.addWidget(checkbox)
            self.table.setCellWidget(i, 0, chk_widget)
            
            # 1. ID
            self.table.setItem(i, 1, QTableWidgetItem(str(row[0])))
            # 2. User
            self.table.setItem(i, 2, QTableWidgetItem(str(row[1])))
            # 3. Subject
            self.table.setItem(i, 3, QTableWidgetItem(str(row[2])))
            # 4. Message (Truncated preview)
            msg_preview = str(row[3])[:50] + "..." if len(str(row[3])) > 50 else str(row[3])
            item_msg = QTableWidgetItem(msg_preview)
            item_msg.setData(Qt.ItemDataRole.UserRole, str(row[3])) # Store full message hidden
            self.table.setItem(i, 4, item_msg)
            # 5. Time
            self.table.setItem(i, 5, QTableWidgetItem(str(row[4])))
            
        conn.close()

    def open_message_popup(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Selection", "Please select a row to view.")
            return

        # Get data
        report_id = self.table.item(row, 1).text()
        user = self.table.item(row, 2).text()
        subject = self.table.item(row, 3).text()
        # Retrieve full message from hidden data
        full_msg = self.table.item(row, 4).data(Qt.ItemDataRole.UserRole)
        time = self.table.item(row, 5).text()

        # Create Popup
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Report #{report_id} Details")
        dialog.setFixedSize(500, 400)
        dialog.setStyleSheet("background-color: white;")
        
        dlg_layout = QVBoxLayout(dialog)
        
        # Details
        dlg_layout.addWidget(QLabel(f"<b>From:</b> {user} <span style='color:gray'>({time})</span>"))
        dlg_layout.addWidget(QLabel(f"<b>Subject:</b> {subject}"))
        dlg_layout.addWidget(QLabel("<b>Message:</b>"))
        
        msg_box = QTextEdit()
        msg_box.setPlainText(full_msg)
        msg_box.setReadOnly(True)
        msg_box.setStyleSheet("background-color: #f9f9f9; padding: 10px; border: 1px solid #ddd;")
        dlg_layout.addWidget(msg_box)
        
        # Close Button
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(dialog.accept)
        dlg_layout.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignRight)
        
        dialog.exec()

    def delete_selected(self):
        ids_to_delete = []
        
        # Loop through all rows to find checked boxes
        for i in range(self.table.rowCount()):
            widget = self.table.cellWidget(i, 0) # Get widget from column 0
            if widget:
                checkbox = widget.findChild(QCheckBox) # Find the checkbox inside
                if checkbox and checkbox.isChecked():
                    ids_to_delete.append(checkbox.property("report_id"))

        if not ids_to_delete:
            QMessageBox.warning(self, "Selection", "No reports selected for deletion.")
            return

        confirm = QMessageBox.question(self, "Confirm Delete", 
                                     f"Are you sure you want to delete {len(ids_to_delete)} reports?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:
            conn = connect()
            cur = conn.cursor()
            # SQL: DELETE FROM reports WHERE id IN (1, 2, 3)
            placeholders = ', '.join('?' for _ in ids_to_delete)
            cur.execute(f"DELETE FROM reports WHERE id IN ({placeholders})", ids_to_delete)
            conn.commit()
            conn.close()
            
            log_action(self.username, "Deleted Reports", f"Deleted IDs: {ids_to_delete}")
            self.load_reports() # Refresh table