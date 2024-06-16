import sqlite3

def setup_database():
    try:
        connection = sqlite3.connect('log_aggregator.db')
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                date TEXT,
                request TEXT,
                status INTEGER,
                size INTEGER
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)

        connection.commit()
        cursor.close()
        connection.close()
    except sqlite3.Error as err:
        print(f"Error setting up database: {err}")
        exit(1)

def drop_database():
    try:
        conn = sqlite3.connect('log_aggregator.db')
        conn.execute("DROP TABLE IF EXISTS logs")
        conn.execute("DROP TABLE IF EXISTS users")
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error dropping database: {e}")