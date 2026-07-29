import sqlite3
from datetime import datetime
def init_db():

    conn = sqlite3.connect("scan_history.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        url TEXT,
        result TEXT,
        risk_score INTEGER,
        scan_time TEXT
    )
    """)

    conn.commit()
    conn.close()
def save_scan(username, url, result, risk_score):

    conn = sqlite3.connect("scan_history.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO scans
    (
        username,
        url,
        result,
        risk_score,
        scan_time
    )
    VALUES (?, ?, ?, ?, datetime('now'))
    """,
    (
        username,
        url,
        result,
        risk_score
    ))

    conn.commit()
    conn.close()
def get_history(username):

    conn = sqlite3.connect("scan_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
        id,
        url,
        result,
        risk_score,
        scan_time
        FROM scans
        WHERE username=?
        ORDER BY id DESC
    """, (username,))

    data = cursor.fetchall()

    conn.close()

    return data
def get_stats():

    conn = sqlite3.connect("scan_history.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scans")
    total_scans = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM scans WHERE result LIKE '%LEGITIMATE%'"
    )
    safe_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM scans WHERE result NOT LIKE '%LEGITIMATE%'"
    )
    phishing_count = cursor.fetchone()[0]

    conn.close()

    return total_scans, safe_count, phishing_count