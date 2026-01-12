from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, 
                             QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QComboBox, QDialog, QDialogButtonBox)
from PyQt6.QtCore import Qt, QDate
from database import connect, get_all_staff
from logs import log_action

class AllocationPage(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # --- TOP: Add Hardware ---
        top_layout = QHBoxLayout()
        self.item_input = QLineEdit()
        self.item_input.setPlaceholderText("Item Name (e.g. MacBook Pro)")
        self.serial_input = QLineEdit()
        self.serial_input.setPlaceholderText("Serial Number")
        
        btn_add = QPushButton("Add to Stock")
        btn_add.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 8px;")
        btn_add.clicked.connect(self.add_hardware)
        
        top_layout.addWidget(self.item_input)
        top_layout.addWidget(self.serial_input)
        top_layout.addWidget(btn_add)
        
        layout.addWidget(QLabel("Hardware Inventory & Assignment", styleSheet="font-size: 22px; font-weight: bold;"))
        layout.addLayout(top_layout)

        # --- TABLE ---
        self.table = QTableWidget()
        self.columns = ["ID", "Item", "Serial", "Status", "Assigned To", "Action"]
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        self.load_data()

    def add_hardware(self):
        name = self.item_input.text()
        serial = self.serial_input.text()
        if not name: return
        
        conn = connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO hardware (item_name, serial_no) VALUES (?, ?)", (name, serial))
        conn.commit()
        conn.close()
        self.item_input.clear()
        self.serial_input.clear()
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        conn = connect()
        cur = conn.cursor()
        # Join with staff table to get names
        cur.execute("""
            SELECT h.id, h.item_name, h.serial_no, h.status, s.full_name 
            FROM hardware h 
            LEFT JOIN staff s ON h.assigned_to_id = s.id
        """)
        rows = cur.fetchall()
        self.table.setRowCount(len(rows))
        
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(row[1])))
            self.table.setItem(i, 2, QTableWidgetItem(str(row[2])))
            
            # Status Color
            status_item = QTableWidgetItem(str(row[3]))
            if row[3] == "Assigned":
                status_item.setForeground(Qt.GlobalColor.red)
            else:
                status_item.setForeground(Qt.GlobalColor.green)
            self.table.setItem(i, 3, status_item)
            
            # Assigned To
            assigned_name = row[4] if row[4] else "---"
            self.table.setItem(i, 4, QTableWidgetItem(assigned_name))
            
            # Action Button (Assign or Return)
            btn_action = QPushButton()
            if row[3] == "Available":
                btn_action.setText("Assign")
                btn_action.setStyleSheet("background-color: #27ae60; color: white;")
                btn_action.clicked.connect(lambda checked, r_id=row[0]: self.open_assign_popup(r_id))
            else:
                btn_action.setText("Return")
                btn_action.setStyleSheet("background-color: #e74c3c; color: white;")
                btn_action.clicked.connect(lambda checked, r_id=row[0]: self.return_item(r_id))
            
            self.table.setCellWidget(i, 5, btn_action)
            
        conn.close()

    def open_assign_popup(self, hardware_id):
        # Popup to select staff
        dialog = QDialog(self)
        dialog.setWindowTitle("Assign Item")
        layout = QVBoxLayout(dialog)
        
        label = QLabel("Select Staff Member:")
        combo = QComboBox()
        
        # Load Staff list
        staff_list = get_all_staff() # Returns [(1, 'John', 'jdoe'), ...]
        for s in staff_list:
            combo.addItem(f"{s[1]} ({s[2]})", s[0]) # Display Name, store ID
            
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(dialog.accept)
        btn_box.rejected.connect(dialog.reject)
        
        layout.addWidget(label)
        layout.addWidget(combo)
        layout.addWidget(btn_box)
        
        if dialog.exec():
            staff_id = combo.currentData()
            self.assign_item(hardware_id, staff_id)

    def assign_item(self, hardware_id, staff_id):
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            UPDATE hardware SET status='Assigned', assigned_to_id=?, assigned_date=date('now') 
            WHERE id=?
        """, (staff_id, hardware_id))
        conn.commit()
        conn.close()
        log_action(self.username, "Assigned Asset", f"Hardware ID {hardware_id} -> Staff {staff_id}")
        self.load_data()

    def return_item(self, hardware_id):
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            UPDATE hardware SET status='Available', assigned_to_id=NULL, assigned_date=NULL 
            WHERE id=?
        """, (hardware_id,))
        conn.commit()
        conn.close()
        log_action(self.username, "Returned Asset", f"Hardware ID {hardware_id}")
        self.load_data()