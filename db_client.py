import sqlite3
from sqlite3 import IntegrityError

conn = sqlite3.connect('database/challenge.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        id TEXT NOT NULL PRIMARY KEY,
        hits INTEGER NOT NULL,
        urlCount INTEGER NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS URL (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        hits INTEGER NOT NULL,
        url TEXT NOT NULL,
        sortUrl TEXT NOT NULL,
        userId TEXT NOT NULL,
        FOREIGN KEY(userId) REFERENCES User(id) ON DELETE CASCADE
    )
""")

# Save (commit) the changes
conn.commit()
conn.close()

def get_user_stats(user_id):
    pass

def create_new_url():
    pass

def create_new_user(user_id):
    conn = sqlite3.connect('database/challenge.db')
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO User (id, hits, urlCount) VALUES (?, ?, ?)
        """, (user_id, 0, 0))
        conn.commit()
        conn.close()
        return True

    except IntegrityError as err:
        print('Error. User already registered.')
        conn.rollback()
        conn.close()
        return False
