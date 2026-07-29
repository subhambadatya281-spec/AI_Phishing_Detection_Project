import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
def create_users_table():

    conn = sqlite3.connect("scan_history.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

def register_user(username, password):

    try:
        conn = sqlite3.connect("scan_history.db")
        cur = conn.cursor()

        hashed_password = generate_password_hash(password)

        cur.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username, hashed_password)
        )

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:
        return False
def validate_user(username, password):

    conn = sqlite3.connect("scan_history.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    user = cur.fetchone()

    conn.close()
    if user and check_password_hash(user[2], password):
        return user

    return None