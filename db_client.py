import sqlite3
import short_url

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
        shortUrl TEXT NOT NULL,
        userId TEXT NOT NULL,
        FOREIGN KEY(userId) REFERENCES User(id) ON DELETE CASCADE
    )
""")

# Save (commit) the changes
conn.commit()
conn.close()

def get_user_stats(user_id): #TODO: finish this method by adding the top urls by user
    conn = sqlite3.connect('database/challenge.db')
    conn.execute('pragma foreign_keys=ON') #Turns on foreign key constraints
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM User WHERE id = ?
    """, (user_id,))
    data = cursor.fetchone()
    conn.close()

    if data is None:
        return False, None

    else:
        stats = {
            'id': data[0],
            'hits': data[1],
            'urlCount': data[2]
        }
        return True, stats

def get_url_stats(url_id):
    conn = sqlite3.connect('database/challenge.db')
    conn.execute('pragma foreign_keys=ON') #Turns on foreign key constraints
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM URL WHERE id = ?
    """, (url_id,))
    data = cursor.fetchone()
    conn.close()

    if data is None:
        return False, None

    else:
        stats = {
            'id': data[0],
            'hits': data[1],
            'url': data[2],
            'shortUrl': data[3]
        }
        return True, stats

def create_new_url(url, partial_short_url, user_id):
    conn = sqlite3.connect('database/challenge.db')
    conn.execute('pragma foreign_keys=ON') #Turns on foreign key constraints
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO URL (hits, url, shortUrl, userId) VALUES (?, ?, ?, ?)
        """, (0, url, partial_short_url, user_id))

        url_id = cursor.lastrowid
        shortened_url = str(partial_short_url + '/' + str(short_url.encode_url(url_id)))

        cursor.execute("""
            UPDATE URL
            SET shortUrl=?
            WHERE id=?
            """, (shortened_url, url_id))

        conn.commit()
        conn.close()
        resp, stats = get_url_stats(url_id) #Will always return the correct URL

        return True, stats

    except IntegrityError as err:
        print('Error. Insert URL failed due to violation of FK constraints.')
        conn.rollback()
        conn.close()

        return False, None

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
