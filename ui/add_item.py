from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, 
                             QPushButton, QLabel, QFrame, QGraphicsDropShadowEffect, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from database import connect
from logs import log_action

class AddItemPage(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(50, 50, 50, 50)

        # Card
        self.card = QFrame()
        self.card.setFixedWidth(500)
        self.card.setStyleSheet("QFrame { background-color: white; border-radius: 15px; border: 1px solid #e0e0e0; }")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 5)
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)

        # CHANGED: Title
        title = QLabel("Add New Subscription")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("border: none; font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        card_layout.addWidget(title)

        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.inputs = {}
        # CHANGED: Field Names (Logic stays same, labels change)
        # Note: 'Supplier' in DB -> Mapped to 'Vendor' in UI
        # Note: 'Item Name' in DB -> Mapped to 'Subscription Name' in UI
        self.field_map = {
            "Subscription Name": "Item Name",
            "Subscription ID": "Reference No",
            "Expiry (YYYY-MM-DD)": "Expiry (YYYY-MM-DD)",
            "Category": "Category",
            "Department": "Department",
            "Vendor": "Supplier"
        }

        for label_text in self.field_map.keys():
            lbl = QLabel(label_text)
            lbl.setStyleSheet("border: none; font-size: 14px; font-weight: 600; color: #555;")
            
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Enter {label_text}...")
            line_edit.setStyleSheet("""
                QLineEdit {
                    padding: 10px; border: 1px solid #ccc; border-radius: 5px; font-size: 13px; background-color: #f9f9f9;
                }
                QLineEdit:focus { border: 1px solid #3498db; background-color: white; }
            """)
            form_layout.addRow(lbl, line_edit)
            self.inputs[label_text] = line_edit

        card_layout.addLayout(form_layout)

        save_btn = QPushButton("Save Subscription")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white; padding: 12px; font-size: 15px; font-weight: bold; border-radius: 8px; margin-top: 15px;
            }
            QPushButton:hover { background-color: #219150; }
        """)
        save_btn.clicked.connect(self.save_data)
        card_layout.addWidget(save_btn)

        main_layout.addWidget(self.card)

    def save_data(self):
        # We need to map the UI labels back to the DB sequence
        # DB order: item_name, reference_no, expiry_date, category, department, supplier
        
        db_values = []
        db_values.append(self.inputs["Subscription Name"].text())
        db_values.append(self.inputs["Subscription ID"].text())
        db_values.append(self.inputs["Expiry (YYYY-MM-DD)"].text())
        db_values.append(self.inputs["Category"].text())
        db_values.append(self.inputs["Department"].text())
        db_values.append(self.inputs["Vendor"].text()) # Vendor maps to Supplier column

        if "" in db_values:
            QMessageBox.warning(self, "Validation Error", "Please fill in all fields.")
            return

        conn = connect()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO assets (item_name, reference_no, expiry_date, category, department, supplier) VALUES (?,?,?,?,?,?)", 
                db_values
            )
            conn.commit()
            
            # CHANGED: Log Message
            item_name = db_values[0]
            log_action(self.username, "Added Subscription", f"{item_name}")

            QMessageBox.information(self, "Success", "Subscription added successfully!")
            for f in self.inputs:
                self.inputs[f].clear()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not save:\n{str(e)}")
        finally:
            conn.close()