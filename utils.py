from database import connect

def log_action(username, role, action):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO logs (username, role, action) VALUES (?,?,?)",
        (username, role, action)
    )
    conn.commit()
    conn.close()