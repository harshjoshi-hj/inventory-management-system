import sqlite3

DB_NAME = "assets.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connect()
    cur = conn.cursor()
    
    # 1. Users Table (Admin/Manager/User)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT UNIQUE, 
            password_hash TEXT, 
            role TEXT
        )
    """)

    # 2. Assets / Subscriptions Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            item_name TEXT, 
            reference_no TEXT, 
            expiry_date DATE, 
            category TEXT, 
            department TEXT, 
            supplier TEXT
        )
    """)

    # 3. Audit Logs Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user TEXT, 
            action TEXT, 
            target TEXT, 
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 4. Reports Table (Support Queries)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            subject TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 5. Staff / Employee Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            username TEXT,
            email TEXT,
            phone TEXT,
            gender TEXT,
            dob DATE,
            created_by TEXT
        )
    """)

    # 6. Hardware / Physical Inventory Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS hardware (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            serial_no TEXT,
            model TEXT,
            status TEXT DEFAULT 'Available',
            assigned_to_id INTEGER,
            assigned_date DATE,
            FOREIGN KEY(assigned_to_id) REFERENCES staff(id)
        )
    """)
    
    conn.commit()
    conn.close()

# --- HELPER FUNCTIONS ---

def has_admin():
    """Checks if an admin account exists in the database."""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
        count = cur.fetchone()[0]
    except sqlite3.OperationalError:
        count = 0
    conn.close()
    return count > 0

def get_dashboard_stats():
    """Returns stats for BOTH Subscriptions and Hardware."""
    conn = connect()
    cur = conn.cursor()
    
    # 1. Subscriptions Stats
    cur.execute("SELECT COUNT(*) FROM assets")
    sub_total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM assets WHERE expiry_date < date('now')")
    sub_expired = cur.fetchone()[0]
    
    # 2. Hardware Stats
    cur.execute("SELECT COUNT(*) FROM hardware")
    hw_total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM hardware WHERE status='Assigned'")
    hw_assigned = cur.fetchone()[0]
    
    conn.close()
    return {
        "sub_total": sub_total, 
        "sub_expired": sub_expired,
        "hw_total": hw_total,
        "hw_assigned": hw_assigned
    }

def get_department_counts():
    """Returns dictionary of subscriptions per department for the chart."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT department, COUNT(*) FROM assets GROUP BY department")
    data = dict(cur.fetchall())
    conn.close()
    return data

def get_hardware_status_counts():
    """Returns data for the Pie Chart (Available vs Assigned)."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT status, COUNT(*) FROM hardware GROUP BY status")
    data = dict(cur.fetchall()) # e.g., {'Available': 10, 'Assigned': 5}
    conn.close()
    return data

def get_all_staff():
    """Fetches list of all staff for dropdown menus."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, username FROM staff")
    data = cur.fetchall()
    conn.close()
    return data