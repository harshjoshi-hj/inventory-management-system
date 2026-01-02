import sqlite3

DB_NAME = "assets.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connect()
    cur = conn.cursor()

    # Users Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT,
        role TEXT
    )
    """)

    # Assets Table - Updated to match UI queries
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

    # Logs Table - Updated column names for consistency
    cur.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        action TEXT,
        target TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def has_admin():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    count = cur.fetchone()[0]
    conn.close()
    return count > 0