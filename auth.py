import hashlib
from database import connect

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def create_user(username, password, role):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
    """, (username, hash_password(password), role))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT role FROM users
        WHERE username=? AND password_hash=?
    """, (username, hash_password(password)))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"role": row[0]}
    return None