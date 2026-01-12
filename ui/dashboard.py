from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QStackedWidget, QFrame)
from PyQt6.QtCore import Qt
from ui.inventory import InventoryPage
from ui.add_item import AddItemPage
from ui.users import UsersPage
from ui.activity_logs import LogsPage
from ui.reports import ReportsPage
from ui.staff import StaffPage
from ui.allocation import AllocationPage
import database
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from logs import log_action

class DashboardWindow(QMainWindow):
    def __init__(self, username, role):
        super().__init__()
        self.username = username
        self.role = role
        self.setWindowTitle("LS Cable Subscription & Asset Management")
        self.setMinimumSize(1200, 800)

        # Main Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QHBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # ================= SIDEBAR =================
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(240)
        self.sidebar.setStyleSheet("background-color: #2c3e50; border: none;")
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        logo = QLabel("LS Cable")
        logo.setStyleSheet("color: white; font-size: 22px; font-weight: bold; margin: 25px 0;")
        self.sidebar_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)

        # ================= CONTENT STACK =================
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #f8f9fa;")

        # Initialize Pages
        self.home_page = self.create_home_page()
        self.inventory_page = InventoryPage()
        self.add_item_page = AddItemPage(username)
        self.expiring_page = InventoryPage(mode="expiring")
        self.expired_page = InventoryPage(mode="expired")
        self.users_page = UsersPage(username)
        self.logs_page = LogsPage()
        self.reports_page = ReportsPage(username, role)
        self.staff_page = StaffPage(username)
        self.alloc_page = AllocationPage(username)

        # Add all to stack
        self.stack.addWidget(self.home_page)      # 0
        self.stack.addWidget(self.inventory_page) # 1
        self.stack.addWidget(self.add_item_page)  # 2
        self.stack.addWidget(self.expiring_page)  # 3
        self.stack.addWidget(self.expired_page)   # 4
        self.stack.addWidget(self.users_page)     # 5
        self.stack.addWidget(self.logs_page)      # 6
        self.stack.addWidget(self.reports_page)   # 7
        self.stack.addWidget(self.staff_page)     # 8
        self.stack.addWidget(self.alloc_page)     # 9

        # ================= NAVIGATION BUTTONS =================
        self.sidebar_layout.addWidget(self.create_nav_btn("Dashboard", lambda: self.stack.setCurrentWidget(self.home_page)))
        
        # Subscription Section
        self.sidebar_layout.addWidget(self.create_nav_btn("All Subscriptions", lambda: self.stack.setCurrentWidget(self.inventory_page)))
        self.sidebar_layout.addWidget(self.create_nav_btn("Add Subscription", lambda: self.stack.setCurrentWidget(self.add_item_page)))
        
        # Staff & Asset Section
        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.HLine)
        line1.setStyleSheet("background-color: #34495e; margin: 10px 20px;")
        self.sidebar_layout.addWidget(line1)

        self.sidebar_layout.addWidget(self.create_nav_btn("Staff Directory", lambda: self.stack.setCurrentWidget(self.staff_page)))
        self.sidebar_layout.addWidget(self.create_nav_btn("Hardware & Assets", lambda: self.stack.setCurrentWidget(self.alloc_page)))

        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setStyleSheet("background-color: #34495e; margin: 10px 20px;")
        self.sidebar_layout.addWidget(line2)

        # Expiry Monitoring
        self.sidebar_layout.addWidget(self.create_nav_btn("Expiring (30 Days)", lambda: self.stack.setCurrentWidget(self.expiring_page)))
        self.sidebar_layout.addWidget(self.create_nav_btn("Expired Subs", lambda: self.stack.setCurrentWidget(self.expired_page)))
        
        # Admin Features
        if self.role == "admin":
            line3 = QFrame()
            line3.setFrameShape(QFrame.Shape.HLine)
            line3.setStyleSheet("background-color: #34495e; margin: 10px 20px;")
            self.sidebar_layout.addWidget(line3)
            
            self.sidebar_layout.addWidget(self.create_nav_btn("User Management", lambda: self.stack.setCurrentWidget(self.users_page)))
            self.sidebar_layout.addWidget(self.create_nav_btn("Audit Logs", lambda: self.stack.setCurrentWidget(self.logs_page)))

        # Support Section
        self.sidebar_layout.addWidget(self.create_nav_btn("Support / Reports", lambda: self.stack.setCurrentWidget(self.reports_page)))

        self.sidebar_layout.addStretch()

        # Logout
        self.btn_logout = QPushButton("Logout")
        self.btn_logout.setStyleSheet("background-color: #e74c3c; color: white; padding: 15px; border: none; font-weight: bold;")
        self.btn_logout.clicked.connect(self.handle_logout)
        self.sidebar_layout.addWidget(self.btn_logout)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.stack)

        self.stack.setCurrentWidget(self.home_page)

    # --- HELPER METHODS ---

    def create_nav_btn(self, text, callback):
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent; color: white; text-align: left;
                padding: 15px 25px; border: none; font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background-color: #34495e; }
        """)
        btn.clicked.connect(callback)
        return btn

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Fetch Data
        stats = database.get_dashboard_stats()
        
        # 1. Welcome Message
        welcome = QLabel(f"Dashboard Overview - {self.username}")
        welcome.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(welcome)

        # 2. Metric Cards (Row of 4)
        card_layout = QHBoxLayout()
        card_layout.setSpacing(20)
        
        # Subscription Cards
        card_layout.addWidget(self.create_card("Total Subscriptions", str(stats['sub_total']), "#2980b9")) # Blue
        card_layout.addWidget(self.create_card("Expired Subs", str(stats['sub_expired']), "#e74c3c"))     # Red
        
        # Hardware Cards
        card_layout.addWidget(self.create_card("Total Hardware", str(stats['hw_total']), "#8e44ad"))      # Purple
        card_layout.addWidget(self.create_card("Assigned Items", str(stats['hw_assigned']), "#27ae60"))   # Green
        
        layout.addLayout(card_layout)

        # 3. Charts Area (Side by Side)
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)

        # --- LEFT: Bar Chart (Subscriptions per Dept) ---
        chart_frame1 = QFrame()
        chart_frame1.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #ddd;")
        vbox1 = QVBoxLayout(chart_frame1)
        
        dept_data = database.get_department_counts()
        fig1 = Figure(figsize=(4, 3), dpi=100)
        ax1 = fig1.add_subplot(111)
        if dept_data:
            ax1.bar(dept_data.keys(), dept_data.values(), color='#3498db')
            ax1.set_xticklabels(dept_data.keys(), rotation=15, ha="right")
        else:
            ax1.text(0.5, 0.5, 'No Subscriptions', ha='center')
        ax1.set_title("Subscriptions by Dept", fontsize=10)
        
        canvas1 = FigureCanvas(fig1)
        vbox1.addWidget(canvas1)
        charts_layout.addWidget(chart_frame1)

        # --- RIGHT: Pie Chart (Hardware Availability) ---
        chart_frame2 = QFrame()
        chart_frame2.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #ddd;")
        vbox2 = QVBoxLayout(chart_frame2)
        
        hw_data = database.get_hardware_status_counts() # {'Available': 5, 'Assigned': 2}
        fig2 = Figure(figsize=(4, 3), dpi=100)
        ax2 = fig2.add_subplot(111)
        
        if hw_data:
            labels = hw_data.keys()
            values = hw_data.values()
            # Dynamic colors based on labels
            colors = []
            if 'Available' in labels: colors.append('#2ecc71')
            if 'Assigned' in labels: colors.append('#e74c3c')
            
            # Fallback if specific colors miss
            if len(colors) < len(labels): colors = ['#2ecc71', '#e74c3c']

            ax2.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        else:
            ax2.text(0.5, 0.5, 'No Hardware Data', ha='center')
        ax2.set_title("Hardware Status", fontsize=10)
        
        canvas2 = FigureCanvas(fig2)
        vbox2.addWidget(canvas2)
        charts_layout.addWidget(chart_frame2)

        layout.addLayout(charts_layout)
        
        return page

    def create_card(self, title, value, color):
        card = QFrame()
        card.setFixedSize(280, 130)
        card.setStyleSheet(f"background-color: white; border-radius: 10px; border-left: 6px solid {color};")
        vbox = QVBoxLayout(card)
        val_label = QLabel(value)
        val_label.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {color}; border: none;")
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #7f8c8d; font-size: 14px; border: none;")
        vbox.addWidget(val_label)
        vbox.addWidget(title_label)
        return card

    def handle_logout(self):
        log_action(self.username, "Logout", "System Exit")
        self.close()
        from main import MainApp
        self.app_instance = MainApp()