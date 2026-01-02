Inventory Management System (Desktop Application)

A secure, role-based Inventory & Asset Management System built using Python, Tkinter, and SQLite, designed for industrial and enterprise use.

This application supports admin and user roles, complete audit logging, expiry tracking, and a clean desktop interface suitable for deployment as a Windows EXE installer.

⸻

🚀 Features

🔐 Authentication & Roles
	•	Secure login system
	•	First-run Admin Setup Wizard
	•	Role-based access:
	•	Admin: Full control (users, inventory, logs)
	•	User: Add/edit inventory (no delete access)

⸻

📦 Inventory Management
	•	Add inventory / asset records
	•	Edit existing records
	•	Delete records (admin only)
	•	Track:
	•	Item name
	•	Reference / Serial number
	•	Category
	•	Department / Location
	•	Supplier / Vendor
	•	Expiry date

⸻

⏰ Expiry Monitoring
	•	View expired items
	•	View items expiring within next 30 days
	•	Centralized inventory dashboard

⸻

👥 User Management (Admin)
	•	Create users
	•	Assign roles (admin / user)
	•	Update user credentials
	•	Remove users
	•	Full traceability of user actions

⸻

🧾 Audit & Logs
	•	Every action is logged:
	•	Login / Logout
	•	Add / Edit / Delete inventory
	•	User creation & updates
	•	Timestamped records stored securely in database

⸻

🖥️ Desktop UI
	•	Clean sidebar-based navigation
	•	Readable fonts & consistent layout
	•	Optimized for Windows desktop use
	•	No internet dependency

⸻

🛠️ Technology Stack
	•	Python 3.10+
	•	Tkinter (GUI)
	•	SQLite (embedded database)
	•	SHA-256 password hashing
	•	Modular architecture (UI / Auth / DB / Logic separated)

⸻

📁 Project Structure

ims/
│
├── main.py                # Application entry point
├── database.py            # Database initialization & helpers
├── auth.py                # Authentication & user management
├── logs.py                # Audit logging
│
├── ui/
│   ├── login.py           # Login screen
│   ├── setup_admin.py     # First-run admin setup
│   ├── dashboard.py       # Main dashboard
│   ├── inventory.py       # Inventory views
│   ├── add_item.py        # Add inventory form
│   ├── users.py           # User management (admin)
│   └── activity_logs.py   # Logs viewer
│
└── assets.db              # SQLite database (auto-generated)

⸻

▶️ How to Run (Development)

Prerequisites
	•	Python 3.10 or later
	•	Tkinter (bundled with standard Python on Windows/macOS)

Steps

python3 main.py

On first launch:
	•	You will be prompted to create an admin account
	•	After setup, the normal login screen appears

⸻

📦 Windows EXE Build (Production)

This application is designed to be packaged using PyInstaller:

pip install pyinstaller
pyinstaller --onefile --windowed main.py

The resulting .exe can be distributed and installed on Windows systems.

⸻

🔐 Security Notes
	•	Passwords are never stored in plain text
	•	SHA-256 hashing is used
	•	SQLite database is local and offline
	•	No external network dependencies

⸻

📈 Suitable For
	•	Manufacturing companies
	•	Industrial inventory tracking
	•	Asset compliance systems
	•	License & expiry monitoring
	•	Internal enterprise tools

⸻

🔧 Future Enhancements (Planned)
	•	Audit export (CSV / PDF)
	•	Backup & restore
	•	License key enforcement
	•	Installer wizard
	•	Permissions matrix UI
	•	Dark mode UI

⸻

👨‍💻 Credits

Designed and Developed by Harsh

⸻

If you want, next I can:
	•	✨ polish UI further (enterprise look)
	•	📄 add export to CSV/PDF
	•	🔑 add license & activation system
	•	📦 prepare a commercial-ready installer flow
