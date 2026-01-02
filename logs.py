from database import connect

def log_action(user, action, target=""):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO logs (user, action, target) VALUES (?, ?, ?)",
        (user, action, target)
    )
    conn.commit()
    conn.close()