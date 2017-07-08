import sqlite3
import os

if not os.path.exists('database'):
    os.makedirs('../database')

conn = sqlite3.connect('../database/challenge.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        id TEXT NOT NULL PRIMARY KEY
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS URL (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        hits INTEGER NOT NULL,
        url TEXT NOT NULL,
        shortUrl TEXT NOT NULL,
        userId TEXT NOT NULL,
        FOREIGN KEY(userId) REFERENCES User(id) ON DELETE CASCADE
    )
""")

conn.commit()
conn.close()
