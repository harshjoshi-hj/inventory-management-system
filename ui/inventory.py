import csv
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                             QLabel, QHBoxLayout, QPushButton, QFileDialog, QHeaderView,
                             QLineEdit, QComboBox, QFrame)
from PyQt6.QtCore import Qt
from database import connect

class InventoryPage(QWidget):
    def __init__(self, mode=None):
        super().__init__()
        self.mode = mode
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- HEADER ---
        header_layout = QHBoxLayout()
        # CHANGED: Titles
        title_text = "Subscription Records"
        if mode == "expired": title_text = "Expired Subscriptions"
        elif mode == "expiring": title_text = "Expiring Soon (30 Days)"
        
        title = QLabel(title_text)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(title)
        
        self.btn_export = QPushButton("Export to CSV")
        self.btn_export.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_export.setStyleSheet("background-color: #27ae60; color: white; padding: 8px 15px; border-radius: 5px; font-weight: bold;")
        self.btn_export.clicked.connect(self.export_to_csv)
        header_layout.addWidget(self.btn_export, alignment=Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(header_layout)

        # --- FILTER BAR ---
        filter_frame = QFrame()
        filter_frame.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #ddd;")
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(10, 10, 10, 10)

        self.search_input = QLineEdit()
        # CHANGED: Placeholder
        self.search_input.setPlaceholderText("Search Subscription Name...")
        self.search_input.setStyleSheet("padding: 6px; border: 1px solid #ccc; border-radius: 4px;")
        
        self.cat_filter = QComboBox()
        self.cat_filter.addItem("All Categories")
        # CHANGED: Example Categories relevant to subscriptions
        self.cat_filter.addItems(["Software", "Service", "License", "Maintenance", "Cloud"]) 
        self.cat_filter.setStyleSheet("padding: 6px; border: 1px solid #ccc; border-radius: 4px;")

        self.dept_filter = QComboBox()
        self.dept_filter.addItem("All Departments")
        self.dept_filter.addItems(["IT", "HR", "Admin", "Production", "Storage", "Shipping"])
        self.dept_filter.setStyleSheet("padding: 6px; border: 1px solid #ccc; border-radius: 4px;")

        btn_apply = QPushButton("Apply Filters")
        btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_apply.setStyleSheet("background-color: #3498db; color: white; padding: 6px 15px; border-radius: 4px; font-weight: bold;")
        btn_apply.clicked.connect(self.load_data)

        filter_layout.addWidget(QLabel("Search:"))
        filter_layout.addWidget(self.search_input, stretch=1)
        filter_layout.addWidget(QLabel("Category:"))
        filter_layout.addWidget(self.cat_filter)
        filter_layout.addWidget(QLabel("Dept:"))
        filter_layout.addWidget(self.dept_filter)
        filter_layout.addWidget(btn_apply)

        layout.addWidget(filter_frame)

        # --- TABLE ---
        self.table = QTableWidget()
        # CHANGED: Table Headers
        self.columns = ["Subscription Name", "Sub ID", "Expiry Date", "Category", "Department", "Vendor"]
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.setSortingEnabled(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("background-color: white; gridline-color: #f0f0f0; border: 1px solid #ddd;")
        layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        conn = connect()
        cur = conn.cursor()
        
        # We still query 'item_name' but display it as 'Subscription Name'
        query = "SELECT item_name, reference_no, expiry_date, category, department, supplier FROM assets WHERE 1=1"
        params = []

        if self.mode == "expired":
            query += " AND expiry_date < date('now')"
        elif self.mode == "expiring":
            query += " AND expiry_date BETWEEN date('now') AND date('now','+30 day')"

        search_text = self.search_input.text().strip()
        if search_text:
            query += " AND (item_name LIKE ? OR reference_no LIKE ?)"
            params.append(f"%{search_text}%")
            params.append(f"%{search_text}%")

        cat = self.cat_filter.currentText()
        if cat != "All Categories":
            query += " AND category = ?"
            params.append(cat)

        dept = self.dept_filter.currentText()
        if dept != "All Departments":
            query += " AND department = ?"
            params.append(dept)

        query += " ORDER BY expiry_date ASC"

        cur.execute(query, params)
        rows = cur.fetchall()
        
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        self.table.setSortingEnabled(True)
        conn.close()

    def export_to_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "subscriptions_export.csv", "CSV Files (*.csv)")
        if path:
            with open(path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.columns)
                for row in range(self.table.rowCount()):
                    row_data = [self.table.item(row, col).text() for col in range(self.table.columnCount())]
                    writer.writerow(row_data)