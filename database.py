import sqlite3

DB_NAME = "expenses.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_mode TEXT,
            note TEXT
        )"""
    )
    conn.commit()
    conn.close()

def add_expense(date, category, amount, payment_mode, note):
    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses (date, category, amount, payment_mode, note) VALUES (?, ?, ?, ?, ?)",
        (date, category, amount, payment_mode, note),
    )
    conn.commit()
    conn.close()

def get_expenses():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, date, category, amount, payment_mode, note FROM expenses ORDER BY date DESC"
    ).fetchall()
    conn.close()
    return rows

def delete_expense(expense_id):
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()